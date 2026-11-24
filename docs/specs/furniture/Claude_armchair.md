# Armchair
- Asset ID: Claude_armchair
- Base ID: armchair
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Living-room furniture; game prop 'armchair' (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
Grandad's terracotta club chair by the window. Years of the same head have sun-faded the top of the back cushion, the seat cushion is pressed flat where he sat, and the seam on the near arm finally split under his hand, showing the yellowed foam.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.9 m
- Depth (Y): 0.9 m
- Height (Z): 0.9 m
- Grid: 18 x 18 x 18 cells at 0.05 m (detail tier), 1,692 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [9.0, 9.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`card_hi`, `terra`, `terra_dark`, `terra_hi`, `wood_deep`, `wood_stain`

## Details included
- Curved upholstered back with a separate back cushion, sun-faded at the top
- Seat cushion pressed into a shallow dish
- Split seam along the top of the near (-X) arm with foam showing
- Rolled arms; short dark wooden legs

## Details excluded
- No pattern noise in the fabric
- No antimacassar or loose cushions

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.9 x 0.9 m

## Outputs
- `models/furniture/Claude_armchair/Claude_armchair.vox` (editable master)
- `models/furniture/Claude_armchair/model.json`
- `models/furniture/Claude_armchair/Claude_armchair.glb` (derived)
- `previews/furniture/Claude_armchair/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a1_living_room.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
