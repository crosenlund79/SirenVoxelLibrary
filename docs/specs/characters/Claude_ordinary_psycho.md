# Ordinary Psycho
- Asset ID: Claude_ordinary_psycho
- Base ID: ordinary_psycho
- Creator: Claude
- Category: characters
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_F
- Scale family: full
- Intended uses: Enemy archetype (current) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
An office worker who walked out of the building the day the sirens stopped and never went home: the same pale shirt, the tie still knotted, one shoe lost somewhere along the way. Whatever happened to them happened on the inside.

Condition: **n/a**.

## Silhouette
Forward-bowed figure: rounded upper back, head below the shoulder-line plane and ahead of the chest, arms dangling in front of the thighs, one bent trailing leg.

## Dimensions and orientation
- Width (X): 0.55 m
- Depth (Y): 0.5 m
- Height (Z): 1.8 m
- Grid: 11 x 10 x 36 cells at 0.05 m (detail tier), 864 occupied voxels
- Front direction: +Y (library voxel)
- Front: The character faces +Y in a neutral standing display pose.
- Pivot: Between the feet at ground level. (pivot_voxel [np.float64(5.5), np.float64(4.0), 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`ash_dark`, `black`, `blue`, `blue_hi`, `cream_deep`, `iron_dark`, `maroon`, `maroon_dark`, `porcelain_deep`, `porcelain_mid`, `skin_pallid`, `stone_dark`, `wgrey_dark`, `wgrey_deep`, `wool_dark`

## Details included
- Hunched upper back, neck and head jutting forward and down
- Long arms hanging forward, left shoulder dropped
- Limping left leg: knee bent, heel lifted, shoe lost (sock foot)
- Pale office shirt half untucked, loosened tie hanging away from the chest
- Warm grey suit trousers torn at the left knee
- Grime at the shirt hem, cuffs and dragged trouser hems; one restrained dried spill down the right chest
- Pallid skin, thinning greying hair, slack mouth

## Details excluded
- Not a zombie: no wounds, exposed bone or rotting flesh
- No gore beyond restrained stains
- No weapon

## Construction and placement notes
- Collision suggestion: Upright capsule about 0.3 m in radius and dimensions_m[2] tall, centred on the pivot; static reference figure, no rig.

## Outputs
- `models/characters/Claude_ordinary_psycho/Claude_ordinary_psycho.vox` (editable master)
- `models/characters/Claude_ordinary_psycho/model.json`
- `models/characters/Claude_ordinary_psycho/Claude_ordinary_psycho.glb` (derived)
- `previews/characters/Claude_ordinary_psycho/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/f1_characters.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
