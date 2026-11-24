# Bookshelf
- Asset ID: Claude_bookshelf
- Base ID: bookshelf
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Storage furniture; game prop 'bookshelf' (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The family bookcase, oak veneer over chipboard. When people left they took a few favourites and a run of the children's books, so the rows lean into the gaps; the holiday photo and the box of old cables stayed behind.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.25 m
- Depth (Y): 0.4 m
- Height (Z): 1.85 m
- Grid: 25 x 8 x 37 cells at 0.05 m (detail tier), 3,687 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [12.5, 4.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`blue_dark`, `blue_deep`, `blue_mid`, `bluegrey_dark`, `bluegrey_deep`, `bluegrey_hi`, `card`, `card_dark`, `card_hi`, `cream_mid`, `cream_shadow`, `green_dark`, `green_deep`, `maroon`, `mauve_dark`, `mauve_deep`, `mustard_dark`, `mustard_deep`, `olive`, `olive_dark`, `pine_aged`, `pine_dark`, `pine_hi`, `pine_light`, `pine_mid`, `red_dark`, `red_deep`, `sage`, `sage_dark`, `sage_deep`, `slate_dark`, `teal_dark`, `teal_deep`, `terra_dark`, `terra_deep`, `wood_deep`, `wood_stain`, `wool`, `wool_dark`

## Details included
- Five shelves in an oak-veneer carcass on a recessed plinth
- Books in muted colours, standing, leaning into gaps and lying in a short stack
- A small lidded box and a framed photo
- Veneer lifting on the near front edge

## Details excluded
- No readable titles or text
- No ornaments clutter

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.25 x 0.4 m

## Outputs
- `models/furniture/Claude_bookshelf/Claude_bookshelf.vox` (editable master)
- `models/furniture/Claude_bookshelf/model.json`
- `models/furniture/Claude_bookshelf/Claude_bookshelf.glb` (derived)
- `previews/furniture/Claude_bookshelf/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a1_living_room.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
