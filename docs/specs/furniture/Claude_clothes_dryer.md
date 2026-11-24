# Almond Tumble Dryer
- Asset ID: Claude_clothes_dryer
- Base ID: clothes_dryer
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Utility appliance; game prop 'dryer' (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
An old almond tumble dryer, much older than the washer beside it. It was dented when it was dragged in through the back door, the lint was never cleaned out properly, and the foil vent hose still trails out of the back where it was meant to go to the window.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.75 m
- Depth (Y): 0.85 m
- Height (Z): 0.85 m
- Grid: 15 x 17 x 17 cells at 0.05 m (detail tier), 1,101 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [6.5, 9.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`almond`, `almond_dark`, `ash`, `ash_light`, `charcoal`, `cream`, `cream_hi`, `cream_mid`, `cream_shadow`, `foil`, `galv`, `galv_dark`, `iron_edge`, `steel_light`

## Details included
- Big flat almond door with a recessed pull, no glass (unlike the washer)
- Backsplash console with a timer dial and a heat knob
- Lint filter pulled up on the top, grey fluff caught at the door's lower seam and on the floor
- Dent in the left side panel
- Ribbed foil vent hose from the back, sagging to the floor

## Details excluded
- No brand
- No readable dial markings

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.65 x 0.6 m

## Outputs
- `models/furniture/Claude_clothes_dryer/Claude_clothes_dryer.vox` (editable master)
- `models/furniture/Claude_clothes_dryer/model.json`
- `models/furniture/Claude_clothes_dryer/Claude_clothes_dryer.glb` (derived)
- `previews/furniture/Claude_clothes_dryer/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a4_bath_utility.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
