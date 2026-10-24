#!/usr/bin/env python3
"""Patch PD2 (32-bit) Diablo Clone and Rathma exclusive drop rolls.

Tier 0: 1/30; Tier 1: 1/20; Tier 2: 1/10.
Patch targets checked against the supplied ProjectDiablo(7).dll build.
Leaves all reward selection and other drop rolls untouched.
"""
from __future__ import annotations
import hashlib
from pathlib import Path
import struct
import sys

SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name('ProjectDiablo(7).dll')
DST = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).with_name('ProjectDiablo_uber_T0-30_T1-20_T2-10.dll')
b = bytearray(SRC.read_bytes())

def u16(offset): return struct.unpack_from('<H', b, offset)[0]
def u32(offset): return struct.unpack_from('<I', b, offset)[0]
def put16(offset, value): struct.pack_into('<H', b, offset, value)
def put32(offset, value): struct.pack_into('<I', b, offset, value)
def align(n, x): return (n + x - 1) // x * x

def checked_patch(offset, expected, replacement):
    assert bytes(b[offset:offset+len(expected)]) == expected, f"Unexpected source bytes at {offset:08X}"
    assert len(expected) == len(replacement)
    b[offset:offset+len(replacement)] = replacement

pe = u32(0x3c)
assert b[pe:pe+4] == b'PE\0\0' and u16(pe+4) == 0x14c, 'Requires PE32 (x86)'
numsections = u16(pe+6)
opt = pe+24
assert u16(opt) == 0x10b, 'Requires PE32 optional header'
sec_align = u32(opt+32)
file_align = u32(opt+36)
imagebase = u32(opt+28)
sect_table = opt+u16(pe+20)
assert numsections == 5 and imagebase == 0x10000000
first_raw = u32(sect_table+20)
assert sect_table+40*(numsections+1) <= first_raw, 'No room for section header'
last_sec = sect_table+40*(numsections-1)
old_end_rva = u32(opt+56)
end_raw = max(u32(sect_table+40*i+20)+u32(sect_table+40*i+16) for i in range(numsections))
assert len(b) == end_raw, 'Unexpected file overlay; refusing to append a section'
new_rva = align(old_end_rva, sec_align)
new_offset = align(len(b), file_align)
new_va = imagebase + new_rva

# Mini-thunks. The original RNG result in EAX is saved and restored.
# Both call sites already clear EDX immediately before the original divisor.
# DClone tier: byte ptr [[EDI]+0x2629]
# Rathma tier:  dword ptr [EBP-0x30] (read earlier from byte ptr [[ESI]+0x2629])
# Shared: ECX = 30 - 10*min(tier, 2) and return with EAX intact.
code = bytearray()
def rel32_instr(opcode, src_va, target_va):
    displacement = target_va - (src_va + 5)
    assert -(1<<31) <= displacement < (1<<31)
    return bytes([opcode]) + struct.pack('<i', displacement)

dclone_va = new_va + len(code)
code += bytes.fromhex('50 8B 0F 0F B6 89 29 26 00 00')
dclone_jump_at = len(code)
code += b'\xE9\x00\x00\x00\x00'

rathma_va = new_va + len(code)
code += bytes.fromhex('50 8B 4D D0')
rathma_jump_at = len(code)
code += b'\xE9\x00\x00\x00\x00'

shared_va = new_va + len(code)
code += bytes.fromhex('83 F9 02 76 05 B9 02 00 00 00 6B C9 F6 83 C1 1E 58 C3')
code[dclone_jump_at:dclone_jump_at+5] = rel32_instr(0xe9, new_va+dclone_jump_at, shared_va)
code[rathma_jump_at:rathma_jump_at+5] = rel32_instr(0xe9, new_va+rathma_jump_at, shared_va)

# Existing .text maps RVA = file offset + 0xC00 on this build.
# Keep both original uniform-RNG calls and existing DIV/CMP/JAEs unchanged.
assert u32(sect_table+12) == 0x1000 and u32(sect_table+20) == 0x400
file_for_rva = lambda rva: rva - 0xc00

# Disable the old tier > 0 eligibility gates; the rare roll must run on tier 0.
checked_patch(file_for_rva(0x376576), bytes.fromhex('0F 86 93 00 00 00'), b'\x90'*6)
checked_patch(file_for_rva(0x376BE0), bytes.fromhex('76 68'), b'\x90'*2)

# Swap 5-byte MOV ECX,200 for 5-byte CALL thunk. Keep the original DIV ECX.
checked_patch(file_for_rva(0x376586), bytes.fromhex('B9 C8 00 00 00'), rel32_instr(0xe8, imagebase+0x376586, dclone_va))
checked_patch(file_for_rva(0x376BEC), bytes.fromhex('B9 C8 00 00 00'), rel32_instr(0xe8, imagebase+0x376BEC, rathma_va))

# Append an explicitly executable/readable section, without modifying any original
# section layout or relocating references. All added transfers use relative offsets.
assert all(x == 0 for x in b[sect_table+40*numsections:sect_table+40*(numsections+1)])
assert new_offset == len(b)
b += code
rawsize = align(len(code), file_align)
b += b'\x00'*(rawsize-len(code))
new_section = sect_table+40*numsections
b[new_section:new_section+40] = struct.pack('<8sIIIIIIHHI',
    b'.uber\0\0\0',len(code),new_rva,rawsize,new_offset,0,0,0,0,0x60000020)
put16(pe+6, numsections+1)
put32(opt+56, align(new_rva+len(code), sec_align))  # SizeOfImage
put32(opt+4, u32(opt+4)+rawsize)  # SizeOfCode
# Original PE checksum is 0, so retain it (no Authenticode signature).

# Self-check the actual embedded machine-code entrypoints and PE metadata.
assert b[new_offset:new_offset+len(code)] == code
assert u16(pe+6) == 6 and u32(opt+56) == old_end_rva+0x1000
assert b[file_for_rva(0x376576):file_for_rva(0x376576)+6] == b'\x90'*6
assert b[file_for_rva(0x376BE0):file_for_rva(0x376BE0)+2] == b'\x90'*2
for tier in (0,1,2):
    assert 30-10*min(tier,2) == {0:30,1:20,2:10}[tier]

DST.write_bytes(b)
print(f'Source:  {SRC.name}  ({SRC.stat().st_size} bytes)')
print(f'SHA256 source:  {hashlib.sha256(SRC.read_bytes()).hexdigest()}')
print(f'Patched: {DST.name}  ({len(b)} bytes)')
print(f'SHA256 patched: {hashlib.sha256(b).hexdigest()}')
print(f'New executable section RVA 0x{new_rva:X}, bytes {len(code)}')
print(f'  DClone helper RVA 0x{dclone_va-imagebase:X}')
print(f'  Rathma helper RVA 0x{rathma_va-imagebase:X}')
print(f'  Shared helper RVA 0x{shared_va-imagebase:X}')
print('T0: 1/30; T1: 1/20; T2: 1/10 (both bosses)')
