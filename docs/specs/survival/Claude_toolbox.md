# Toolbox
- Asset ID: Claude_toolbox
- Base ID: toolbox
- Creator: Claude
- Category: survival
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Tool storage pickup (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The household's blue-grey cantilever toolbox, left open on the floor with both trays fanned out. Whoever used it last grabbed what they needed and left the hammer, a screwdriver and a tape measure in the bottom.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.5 m
- Depth (Y): 0.25 m
- Height (Z): 0.2125 m
- Grid: 40 x 20 x 17 cells at 0.0125 m (micro tier), 2,707 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the working / interaction side.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [20.0, 10.0, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it.

## Materials and colors
`bluegrey`, `bluegrey_dark`, `bluegrey_deep`, `bluegrey_hi`, `card`, `card_hi`, `charcoal`, `copper`, `galv`, `iron`, `mustard`, `mustard_dark`, `mustard_deep`, `pine_aged`, `red_dark`, `rust_dark`, `sawdust`, `steel`, `steel_dark`, `steel_hi`, `steel_light`, `wood_stain`

## Details included
- Steel base box with two trays raised out on linkage arms at each end
- Fixed carry handle bridging the ends, black grip sleeve
- Hammer, screwdriver, spanner and tape measure in the base
- Screws, a pencil and pliers in the trays
- Chipped paint on the rims, a little rust at the bottom corners

## Details excluded
- No brand plate or sticker
- Distinct from the red box on the pilot workbench

## Construction and placement notes
- Collision suggestion: Box 0.48 x 0.15 x 0.14 m on the base; trays and handle are overhangs.
- Placement footprint: 0.475 x 0.125 m

## Outputs
- `models/survival/Claude_toolbox/Claude_toolbox.vox` (editable master)
- `models/survival/Claude_toolbox/model.json`
- `models/survival/Claude_toolbox/Claude_toolbox.glb` (derived)
- `previews/survival/Claude_toolbox/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b1_storage_tools.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
