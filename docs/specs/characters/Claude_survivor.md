# Player Survivor
- Asset ID: Claude_survivor
- Base ID: survivor
- Creator: Claude
- Category: characters
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_F
- Scale family: full
- Intended uses: Player character reference (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
Someone who was ordinary before the sirens stopped: a dark work jacket, cargo trousers worn pale at the knees from kneeling, the orange beanie and scarf they were wearing that morning, and a pack they now never take off.

Condition: **n/a**.

## Silhouette
Rounded beanie head, sloped shoulders with a pack hump behind, bedroll under the pack, arms held slightly away, feet apart.

## Dimensions and orientation
- Width (X): 0.65 m
- Depth (Y): 0.5 m
- Height (Z): 1.75 m
- Grid: 13 x 10 x 35 cells at 0.05 m (detail tier), 1,006 occupied voxels
- Front direction: +Y (library voxel)
- Front: The character faces +Y in a neutral standing display pose.
- Pivot: Between the feet at ground level. (pivot_voxel [np.float64(6.5), np.float64(7.0), 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`black`, `brass_dark`, `card_deep`, `charcoal`, `galv_dark`, `hair_black`, `hair_brown`, `khaki`, `khaki_dark`, `leather`, `leather_dark`, `olive`, `olive_dark`, `rust`, `rust_dark`, `skin1`, `skin1_hi`, `skin1_shadow`, `slate`, `slate_dark`, `slate_deep`, `wool`, `wool_dark`

## Details included
- Orange knitted beanie with a rolled cuff and a matching scarf, tail hanging over the left chest (the one warm accent)
- Dark zipped jacket with ribbed hem and cuffs
- Brown leather backpack shoulder straps with a sternum strap
- Olive canvas backpack with a front pocket, top lid, grab loop and a rolled wool bedroll strapped underneath
- Metal bottle in the pack's left side pocket
- Cargo pocket on the left thigh; knees rubbed pale
- Leather work boots with scuffed toe caps

## Details excluded
- No weapon or tool in the hands (separate catalog models)
- No logos, patches or readable text

## Construction and placement notes
- Collision suggestion: Upright capsule about 0.3 m in radius and dimensions_m[2] tall, centred on the pivot; static reference figure, no rig.

## Outputs
- `models/characters/Claude_survivor/Claude_survivor.vox` (editable master)
- `models/characters/Claude_survivor/model.json`
- `models/characters/Claude_survivor/Claude_survivor.glb` (derived)
- `previews/characters/Claude_survivor/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/f1_characters.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
