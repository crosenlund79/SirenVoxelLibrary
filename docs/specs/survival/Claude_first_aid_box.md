# Wall First-Aid Box
- Asset ID: Claude_first_aid_box
- Base ID: first_aid_box
- Creator: Claude
- Category: survival
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Wall-mounted medical supply (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The white first-aid box from the school corridor wall, its door hanging open after someone took the painkillers and most of the dressings in a hurry. A bandage roll, a bottle of iodine and a few gauze packs are left.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.375 m
- Depth (Y): 0.2375 m
- Height (Z): 0.225 m
- Grid: 30 x 19 x 18 cells at 0.0125 m (micro tier), 2,693 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y faces into the room; the back face is flat for the wall.
- Pivot: Bottom centre of the back (wall) face. (pivot_voxel [15.0, 0.0, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it.

## Materials and colors
`charcoal`, `cream`, `cream_hi`, `cream_shadow`, `label_blue`, `paint_white`, `paint_white_shadow`, `paper`, `porcelain`, `porcelain_mid`, `porcelain_shadow`, `rust_deep`, `signal_red_dark`, `steel`, `steel_light`

## Details included
- White steel box, flat back for the wall, door hinged on the right
- Door ajar showing its muted red cross
- Shelf with leftover supplies; the right side cleared out
- Thumb-greyed catch on the free edge

## Details excluded
- No text, brand or pharmacy marks
- No glowing or bright red

## Mounting
{"type": "wall", "recommended_bottom_height_m": 1.3}

## Construction and placement notes
- Collision suggestion: Box 0.375 x 0.11 x 0.225 m against the wall; the open door is an overhang.

## Outputs
- `models/survival/Claude_first_aid_box/Claude_first_aid_box.vox` (editable master)
- `models/survival/Claude_first_aid_box/model.json`
- `models/survival/Claude_first_aid_box/Claude_first_aid_box.glb` (derived)
- `previews/survival/Claude_first_aid_box/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b2_survival_gear.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
