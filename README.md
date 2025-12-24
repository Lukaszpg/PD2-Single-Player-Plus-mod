
# Project Diablo 2 Single Player+

Discord: https://discord.gg/CwN2s6AHSZ

Newest release download: https://github.com/Lukaszpg/PD2-Single-player-mod/releases/tag/v12.0.0

## Known bugs

* Eternal Coin does not have a name in the inventory

## About this mod

Project Diablo 2 team did amazing job and stunned me and the other veteran D2 players with their high quality work. However, not everyone has the time to farm 24/7. This mod is for players that enjoy slaying plethora of monsters in Diablo 2, but don't have that much time to play in the way the Diablo 2 game and PD2 mod were designed, with abyssmal drop rates and item scarcity. If you have Infinity by day 3 of the PD2 ladder, then this mod is not for you.

## Multiplayer

The mod works fully in local TCP/IP. Players connecting need to have **identical** version of the vanilla PD2, it's DLLs and this mod.

## How to install

Head to [launcher repository](https://github.com/Lukaszpg/pd2-single-player-plus-launcher) and follow the instructions. This works right now only on Windows OS. If you have other operating system, please follow manual installation istructions below: 

a) With PlugY:

1. Copy your Diablo 2 game with Project Diablo 2 mod installed to a new directory.
2. Install PD2 Plugy for SP by BetweenWalls: https://github.com/BetweenWalls/PD2-PlugY#pd2-plugy. WARNING - The materials tab introduced in S11 tab will not work with Plugy! 2a. If you already have Plugy installed and played previous versions of this mod, please remove the contents of shared stash and create a new character.
3. Head to "Releases" and download most recent version of this mod.
4. Paste the downloaded "pd2data.mpq" file to ProjectD2 folder at your client directory, that you've created at step one.
5. Create a shortcut to "Plugy.exe" from your ProjectD2 folder. Add "-3dfx -plugy" run parameter to your Plugy.exe shortcut.
6. Use the recommended loot filter from "Releases" (just paste the downloaded loot.filter file to your D2 client ProjectD2 folder) or adjust your personal loot filter, using new items codes on the bottom of this page (loot filter knowledge required).
7. Launch the game through the PlugY shortcut created in step 6.
8. Head to Akara and look for an item with Alkor's quest potion graphics. If it's there, mod was installed successfully. GLHF!

b) Without PlugY:

1. Copy your Diablo 2 game with Project Diablo 2 mod installed to a new directory.
2. Create shortcut for PD2 Launcher from the new directory.
3. Head to "Releases" and download most recent version of this mod.
4. Paste the downloaded "pd2data.mpq" file to ProjectD2 folder at your client directory, that you've created at step 1.
5. Use the recommended loot filter from "Releases" (just paste the downloaded loot.filter file to your D2 client ProjectD2 folder) or adjust your personal loot filter, using new items codes on the bottom of this page (loot filter knowledge required).
6. IMPORTANT Launch PD2 Launcher through the shortcut created in step 2, head to options and click "Disable Updates". Close options. Click Play.
7. Head to Akara and look for an item with Alkor's quest potion graphics. If it's there, mod was installed successfully. GLHF!

## Troubleshooting

1. I have launched the mod through PlugY exe, but it's not working with an error pictured below.

![image](https://github.com/user-attachments/assets/5147e3cc-6e4b-49cd-9a65-bee7476d7dfb)

**Solution:** Open PlugY.ini file in your ProjectD2 directory, look for `ActiveShiftClickLimit=1` and change it to `ActiveShiftClickLimit=0`. 
  
## New item codes

Below item codes are assigned to new items that this mod introduced.

* Mythic orb - mfo
* Divine orb - divo
* Exalted orb - exo
* Gheed's Curious Box - gcbx
* Charsi's Crafting Box - ccbx
* Eternal coin - ncoi

## Main mod changes and important recipes

### Drop rate changes

* Runes are 500% less likely to downgrade to lesser rune when game is calculating what rune to drop
* All PD2 vanilla items have drop rates increased between 50% and 5000% (eg. Lillit's mirror from 1:25m to 1:500k)
* Rathma and Uber Diablo drop their unique items at 1/20 rate regardless of tier of the fight
* This section is currently in progress and will soon be updated

### Rune downgrade

All runes can be in stacked or non-stacked form.

* Eld to Pul  + Key = 3x lower rune
* Um to Ber + Key = 1x lower rune
* Sur to Zod + 1x Eternal Coin = 1x lower rune

### Mythic Orb

* Base/Exceptional Normal/superior/magic/rare non-corrupted base item + Mythic Orb = Unique Item on that item base
* Magic/rare amulet + Mythic Orb = random amulet from set of Nokozan Relic/The Cat's Eye/The Mahim Oak Curio/Saracen's Chance/Crescent Moon/The Eye of Etlich/Atma's Scarab
* Magic/rare ring + Mythic Orb = random ring from set of Nagelring/Manald Heal/Raven Frost/Dwarf Star/Carrion Wind
* Magic Grand Charm + Mythic Orb = Gheed's Fortune unique charm

Ring/Amulets have to be cubed TWICE for final outcome.

### Divine Orb

* Elite Normal/superior/magic/rare non-corrupted base item + Divine Orb = Unique Item on that item base
* Magic/rare amulet + Divine Orb = random amulet from set of Metalgrid/Highlord's Wrath/Mara's Caleidoscope/Seraph's Hymn/The Rising Sun
* Magic/rare ring + Divine Orb = random ring from set of The Stone of Jordan/Bul Katho's Wedding Band/Nature's Peace/Constricting Loop/Wisp Projector
* 15 jewel fragments + Divine Orb = random Rainbow Facet

Ring/Amulets have to be cubed TWICE for final outcome.

### Exalted Orb

* Normal/superior/magic/rare non-corrupted base item + Exalted Orb = Set Item on that item base
* Magic/rare non-corrupted amulet/ring + Exalted Orb = Set Jewellery Item

### Cain's Wisdom

* Small Magic Charm + Twisted Essence of Suffering + Charged Essence of Hatred + Burning Essence of Terror + Festering Essence of Destruction = Cain's Wisdom (additional exp affix, 200-250% range)
* Cain's Wisdom + Demonic Cube = Re-rolled Cain's Wisdom
* Cain's Wisdom + Annihilus = Annihilus with +250% exp affix

### Exchange

* 2x Larzuk's Puzzle Piece + Eternal Coin = Larzuk's Puzzle Box
* Diablo Clone/Rathma/Lucion/Uber Tristram Key + Eternal Coin = Copy of said key
* Divine Orb + Coin = 2x Mythical Orb (works with up to 25 divine orbs per single recipe)
* 3x Exalted Orb + Coin = Mythical Orb (works with 3,6,9...48 Exalted Orbs)

### New Demonic Cube recipes

* Set Ring/Amulet + Demonic Cube + Eternal Coin = Re-rolled type of Set Ring/Amulet
* Rainbow Facet + Demonic Cube + Eternal Coin = Re-rolled type of Rainbow Facet (eg. Fire to Lightning)

### Lilith's Mirror

* Lilith's Mirror can now be used in the cube with non-corrupted unique/set armor/weapon/amulet/ring to create exact copy of it - transfers sockets and ethereal status. Mirrored items can't be mirrored again.
* Lilith's Mirror can now be used with magic/rare/unique jewel to create exact copy of it. Mirrored jewels can't be mirrored again.

### Gheed's Curious Box 

* Cube it **TWICE** to receive random stack of 50 perfect gems or 50 jewel fragments
* Drops in Hell and maps

### Charsi's Crafting Box

* Cube it **TWICE** to receive random 5 crafting infusions (13.2% chance) or 5 catalyst shards (7.6% chance)
* Drops in Hell and maps

### Crafting infusions changes

* Normal/magic/rare circlet, coronet, diadem and tiara are craftable with crafting infusions
* Arrows and bolts are craftable with crafting infusions
* Already crafted bases can be used to craft again with infusions

### Larzuk's Puzzle Piece & Box Socketing changes

* Larzuk's Puzzle Piece and Box can be used ro re-roll the number of sockets on an item, destroying the contents of the sockets

### Removing socket contents

* You can now remove any item socket contents while preserving said content using Larzuk's Mallus (item sold by Larzuk in any act for 250k gold)
* Larzuk’s Malus + Socketed Item = Used item with socket contents removed (preserves the contents)

### Uber Tristram mini-ubers portals

* Now only one of any key is required to open a portal to Uber Tristram mini-uber. Can be the same key



