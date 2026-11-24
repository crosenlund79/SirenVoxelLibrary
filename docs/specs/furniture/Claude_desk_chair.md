# Desk Chair
- Asset ID: Claude_desk_chair
- Base ID: desk_chair
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Office chair (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The cheap swivel chair from the same bedroom desk. The tilt lock broke long ago so the backrest lolls backwards, and the front corner of the seat has torn through to the foam from years of being dragged against the desk drawer.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.55 m
- Depth (Y): 0.65 m
- Height (Z): 0.95 m
- Grid: 11 x 13 x 19 cells at 0.05 m (detail tier), 372 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [5.5, 7.5, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`almond`, `almond_dark`, `black`, `charcoal`, `denim`, `denim_dark`, `denim_hi`, `iron_edge`, `steel_light`

## Details included
- Five-star base with castors and a gas lift
- Padded seat on a dark seat pan
- Torn front corner showing foam
- Backrest leaning back on a broken tilt

## Details excluded
- No armrests

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.65 x 0.65 m

## Outputs
- `models/furniture/Claude_desk_chair/Claude_desk_chair.vox` (editable master)
- `models/furniture/Claude_desk_chair/model.json`
- `models/furniture/Claude_desk_chair/Claude_desk_chair.glb` (derived)
- `previews/furniture/Claude_desk_chair/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a2_bedroom_office.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
