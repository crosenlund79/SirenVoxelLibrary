# Small Desk
- Asset ID: Claude_small_desk
- Base ID: small_desk
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Desk / work surface (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A teenager's homework desk under the bedroom window. The laptop was shut and left; the top pedestal drawer was pulled out by someone hunting for papers, and the last mug of tea is still on the corner.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.25 m
- Depth (Y): 0.85 m
- Height (Z): 0.8 m
- Grid: 25 x 17 x 16 cells at 0.05 m (detail tier), 1,069 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [12.5, 6.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`label_blue`, `paint_white`, `paint_white_shadow`, `paper`, `pine_light`, `pine_mid`, `porcelain`, `porcelain_deep`, `steel`, `steel_light`

## Details included
- Oak top on a white three-drawer pedestal and two square legs
- Modesty panel at the back
- Top drawer pulled out with loose papers
- Closed silver laptop and a mug on the top

## Details excluded
- No chair (Claude_desk_chair)
- No lamp or screen

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.25 x 0.6 m

## Outputs
- `models/furniture/Claude_small_desk/Claude_small_desk.vox` (editable master)
- `models/furniture/Claude_small_desk/model.json`
- `models/furniture/Claude_small_desk/Claude_small_desk.glb` (derived)
- `previews/furniture/Claude_small_desk/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a2_bedroom_office.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
