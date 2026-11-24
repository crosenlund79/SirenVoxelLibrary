# Kitchen Wall Cabinet
- Asset ID: Claude_wall_cabinet
- Base ID: wall_cabinet
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Wall-mounted kitchen cabinet (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
Hung above the counter, it held the everyday plates and cups. The right-hand door was left standing open; most of the cups are gone, the plates were left because nobody needed plates any more.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.15 m
- Depth (Y): 0.8 m
- Height (Z): 0.75 m
- Grid: 23 x 16 x 15 cells at 0.05 m (detail tier), 1,141 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y faces into the room; the back (y = 0) is flat for the wall.
- Pivot: Bottom centre of the back face (the cabinet body, not the open door). Hang with the back on the wall; bottom at about 1.45 m (0.55 m over the 0.90 m worktop). (pivot_voxel [10.5, 0.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`charcoal`, `cream_deep`, `cream_shadow`, `glass_hi`, `paper`, `porcelain_hi`, `porcelain_mid`, `porcelain_shadow`, `sage`, `sage_dark`, `sage_hi`, `steel_dark`, `terra`, `terra_dark`

## Details included
- Sage shaker doors matching the base units; right door open 90 degrees
- Interior shelf with a short plate stack and two cups, one tipped
- Charcoal handles at the bottom of the doors (reachable from below)
- Flat back for the wall

## Details excluded
- No wall, no mounting rail modelled

## Mounting
{"type": "wall", "recommended_bottom_height_m": 1.45}

## Construction and placement notes
- Collision suggestion: Box 1.05 x 0.35 x 0.75 m for the body; the open door adds a 0.05 x 0.50 m leaf at the right end.

## Outputs
- `models/furniture/Claude_wall_cabinet/Claude_wall_cabinet.vox` (editable master)
- `models/furniture/Claude_wall_cabinet/model.json`
- `models/furniture/Claude_wall_cabinet/Claude_wall_cabinet.glb` (derived)
- `previews/furniture/Claude_wall_cabinet/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a3_kitchen.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
