# Flat Television
- Asset ID: Claude_television
- Base ID: television
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Dead TV on a stand; living-room dressing (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The living-room television, switched off at the wall when the power went. Someone knocked it reaching for the cabinet - a hairline crack now runs across the near top corner - and dust has settled along its top edge since.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.1 m
- Depth (Y): 0.2 m
- Height (Z): 0.7 m
- Grid: 22 x 4 x 14 cells at 0.05 m (detail tier), 382 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [11.0, 2.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`charcoal`, `glass_dark`, `iron_edge`, `screen`, `screen_sheen`, `steel`, `steel_dark`, `water_dark`

## Details included
- Unbranded flat panel on a centre foot
- Dark screen with a soft window sheen
- Hairline crack across the near top corner
- Dust along the top edge
- Thicker electronics box on the back

## Details excluded
- No logo, no lit screen, no buttons or text

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.4 x 0.2 m

## Outputs
- `models/furniture/Claude_television/Claude_television.vox` (editable master)
- `models/furniture/Claude_television/model.json`
- `models/furniture/Claude_television/Claude_television.glb` (derived)
- `previews/furniture/Claude_television/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a1_living_room.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
