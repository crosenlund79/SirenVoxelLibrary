# Mirrored Medicine Cabinet
- Asset ID: Claude_medicine_cabinet
- Base ID: medicine_cabinet
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Lootable medical storage (wall) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The bathroom cabinet was the first thing searched. Someone swept the shelves into a bag and left the right door hanging open; only an amber pill bottle and a plastic bottle that rolled to the back were left. Damp has started to lift the mirror silver along its bottom edge.

Condition: **abandoned**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.7 m
- Depth (Y): 0.45 m
- Height (Z): 0.75 m
- Grid: 14 x 9 x 15 cells at 0.05 m (detail tier), 638 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y faces into the room; the back (y = 0) is flat for the wall.
- Pivot: Bottom centre of the back face (the cabinet body, not the open door). Hang with the back on the wall; bottom at about 1.20 m (over a 0.85 m vanity). (pivot_voxel [6.5, 0.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`chrome`, `glass`, `glass_hi`, `label_red`, `mirror`, `ochre`, `paint_white`, `paint_white_shadow`, `porcelain_hi`, `rust_deep`, `steel_light`

## Details included
- Painted steel cabinet with two mirror doors; the left door is closed
- Right door swung open 90 degrees, its painted back toward the shelves
- Two glass shelves, one amber pill bottle standing, one white bottle on its side
- Mirror silver lifting along the bottom edge; rust starting on the bottom front lip

## Details excluded
- No reflections painted as pictures
- No readable labels

## Mounting
{"type": "wall", "recommended_bottom_height_m": 1.2}

## Construction and placement notes
- Collision suggestion: Box 0.65 x 0.20 x 0.75 m for the body; the open door adds a 0.05 x 0.30 m leaf at the right end.

## Outputs
- `models/furniture/Claude_medicine_cabinet/Claude_medicine_cabinet.vox` (editable master)
- `models/furniture/Claude_medicine_cabinet/model.json`
- `models/furniture/Claude_medicine_cabinet/Claude_medicine_cabinet.glb` (derived)
- `previews/furniture/Claude_medicine_cabinet/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a4_bath_utility.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
