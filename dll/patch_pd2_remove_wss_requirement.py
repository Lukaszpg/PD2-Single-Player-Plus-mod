#!/usr/bin/env python3
"""Remove WSS/CWSS eligibility check from the automatic second cube transmute.

Target: ProjectDiablo(7).dll build supplied October 24, 2026.
Also accepts the separate tier-dependent Uber-drop patch derived from that build.

Only 3 bytes change: at RVA 0x367303, replace the WSS validator setup
    lea ecx, [ebp-4Ch]   (8D 4D B4)
with
    jmp 0x36730F       (EB 0A)
    nop                  (90)

This preserves the recipe function == 2 check and the recursive call, but
skips the now-unnecessary WSS/CWSS scan and validation entirely.

Important: no recursion limit is added. If an eligible recipe still matches
on subsequent invocation(s), additional transmutations can occur.
"""
from __future__ import annotations

import hashlib
import struct
import sys
from pathlib import Path

RVA = 0x367303
ORIGINAL = bytes.fromhex("8D 4D B4")
PATCHED = bytes.fromhex("EB 0A 90")

# Check the surrounding recipe/function branch and second-transmute call.
# These instruction bytes are the same in the base DLL and in the earlier
# tiered Uber-drop-rate patch.
WITNESSES = (
    (0x3672FC, bytes.fromhex("8A 47 01 3C 02 75 21")), # function == 2
    (0x367306, bytes.fromhex("E8 C5 D7 FF FF 84 C0 74 7E")), # validator+test
    (0x36730F, bytes.fromhex("FF 75 9C C7 86 FC 25 00 00 00 00 00 00 56 E8 8E FD FF FF")),
)


def read_u16(data: bytes, offset: int) -> int:
    return struct.unpack_from("<H", data, offset)[0]


def read_u32(data: bytes, offset: int) -> int:
    return struct.unpack_from("<I", data, offset)[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def file_offset_for_rva(data: bytes, rva: int) -> int:
    require(data[:2] == b"MZ", "Not an MZ executable")
    pe = read_u32(data, 0x3C)
    require(data[pe:pe+4] == b"PE\x00\x00", "Not a PE file")
    require(read_u16(data, pe+4) == 0x14C, "Expected a 32-bit x86 PE DLL")
    section_count = read_u16(data, pe+6)
    opt = pe+24
    require(read_u16(data, opt) == 0x10B, "Expected PE32 optional header")
    require(read_u32(data, opt+28) == 0x10000000,
            "Unexpected preferred image base; wrong DLL build?")
    sec_table = opt + read_u16(data, pe+20)
    for i in range(section_count):
        base = sec_table+i*40
        virtual_size = read_u32(data, base+8)
        virtual_address = read_u32(data, base+12)
        raw_size = read_u32(data, base+16)
        raw_pointer = read_u32(data, base+20)
        if virtual_address <= rva < virtual_address + min(virtual_size, raw_size):
            file_offset = raw_pointer + (rva - virtual_address)
            require(file_offset < len(data), "RVA maps beyond file")
            return file_offset
    raise ValueError(f"RVA 0x{rva:X} is not file-backed in this DLL")


def patch(source: Path, output: Path) -> None:
    require(source.is_file(), f"Source DLL not found: {source}")
    require(source.resolve() != output.resolve(),
            "Refusing to overwrite the source DLL; choose a different output filename")
    require(not output.exists(),
            f"Output file already exists: {output} (refusing to overwrite)")

    original_data = source.read_bytes()
    for rva, witness in WITNESSES:
        ofs = file_offset_for_rva(original_data, rva)
        require(original_data[ofs:ofs+len(witness)] == witness,
                f"Unexpected instructions near RVA 0x{rva:X}; wrong build or modified DLL")
    ofs = file_offset_for_rva(original_data, RVA)
    old = original_data[ofs:ofs+len(ORIGINAL)]
    if old == PATCHED:
        raise ValueError("The WSS requirement is already removed in this DLL")
    require(old == ORIGINAL,
            f"Unexpected bytes at RVA 0x{RVA:X}: {old.hex(' ')}; refusing to patch")

    data = bytearray(original_data)
    data[ofs:ofs+len(PATCHED)] = PATCHED

    # Self-check: exactly the three intended bytes have changed.
    require(len(data) == len(original_data), "Output length changed unexpectedly")
    require(data[:ofs] == original_data[:ofs] and data[ofs+3:] == original_data[ofs+3:],
            "Unexpected unrelated modifications")
    require(bytes(data[ofs:ofs+3]) == PATCHED, "Patch verification failed")

    output.write_bytes(data)
    print("WSS/CWSS requirement removed from second cube transmute.")
    print("Recipe function == 2 check: preserved")
    print("Second transmute call:    preserved")
    print(f"Patch RVA:      0x{RVA:08X}")
    print(f"File offset:    0x{ofs:08X}")
    print(f"Original bytes: {ORIGINAL.hex(' ').upper()}")
    print(f"Patched bytes:  {PATCHED.hex(' ').upper()}")
    print(f"Input:  {source}")
    print(f"Output: {output}")
    print(f"Output SHA256: {hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: py -3 patch_pd2_remove_wss_requirement.py INPUT.dll OUTPUT.dll")
        sys.exit(2)
    try:
        patch(Path(sys.argv[1]), Path(sys.argv[2]))
    except (ValueError, OSError, struct.error) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
