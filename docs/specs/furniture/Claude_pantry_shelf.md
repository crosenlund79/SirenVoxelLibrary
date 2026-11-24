# Pantry Shelving
- Asset ID: Claude_pantry_shelf
- Base ID: pantry_shelf
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Food storage; scavenging target (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
Plain pine shelving in a walk-in pantry, stripped by whoever came first. They took what they could carry: a few cans rolled to the back, two jars nobody wanted, a flour sack that split when it was dragged and spilled down to the floor, and the cardboard tray the tins came in.

Condition: **abandoned**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.15 m
- Depth (Y): 0.65 m
- Height (Z): 1.8 m
- Grid: 23 x 13 x 36 cells at 0.05 m (detail tier), 1,620 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [11.5, 5.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`blue_dark`, `blue_mid`, `brass_dark`, `card`, `card_dark`, `card_hi`, `cream`, `cream_mid`, `cream_shadow`, `foil`, `glass_hi`, `label_green`, `label_red`, `mustard_dark`, `paper`, `pine_aged`, `pine_dark`, `pine_hi`, `pine_light`, `pine_mid`, `porcelain_hi`, `red_dark`

## Details included
- Five pine shelves on four square posts with back stop rails
- Split flour sack slumped on the bottom shelf, flour spilled over the edge into a drift on the floor
- Empty cardboard tray on the middle shelf
- Three cans (one fallen on its side) and two jars, pushed to the back
- Pale clean patches on the boards where stock stood for years

## Details excluded
- No readable labels or brands
- Mostly empty on purpose

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.15 x 0.5 m

## Outputs
- `models/furniture/Claude_pantry_shelf/Claude_pantry_shelf.vox` (editable master)
- `models/furniture/Claude_pantry_shelf/model.json`
- `models/furniture/Claude_pantry_shelf/Claude_pantry_shelf.glb` (derived)
- `previews/furniture/Claude_pantry_shelf/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a3_kitchen.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
