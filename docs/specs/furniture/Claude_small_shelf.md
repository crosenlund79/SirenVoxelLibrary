# Small Shelf
- Asset ID: Claude_small_shelf
- Base ID: small_shelf
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Small standing shelf for dishes/jars (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A cheap pine shelf, painted blue-grey years ago, that stood in the corner of the kitchen holding the everyday plates and the jam jars. Its joints have worked loose and the top half has racked over to one side.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.9 m
- Depth (Y): 0.35 m
- Height (Z): 1.25 m
- Grid: 18 x 7 x 25 cells at 0.05 m (detail tier), 785 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [8.5, 3.5, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`bluegrey`, `bluegrey_dark`, `bluegrey_hi`, `brass_dark`, `card_dark`, `glass_hi`, `label_cream`, `pine_aged`, `porcelain`, `porcelain_hi`, `porcelain_mid`, `porcelain_shadow`, `red_dark`, `sawdust`, `steel_light`, `teal_dark`

## Details included
- Four posts and four boards; the posts jog one cell sideways above the middle shelf where the joints have worked loose
- Painted blue-grey, chipped to pine on the front edges
- Two plates standing at the back, a short stack in front, a crock and lidded jars

## Details excluded
- No full dinner service; a few everyday things

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.85 x 0.35 m

## Outputs
- `models/furniture/Claude_small_shelf/Claude_small_shelf.vox` (editable master)
- `models/furniture/Claude_small_shelf/model.json`
- `models/furniture/Claude_small_shelf/Claude_small_shelf.glb` (derived)
- `previews/furniture/Claude_small_shelf/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a1_living_room.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
