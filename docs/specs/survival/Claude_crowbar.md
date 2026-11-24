# Crowbar
- Asset ID: Claude_crowbar
- Base ID: crowbar
- Creator: Claude
- Category: survival
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Tool item 'crowbar'; melee (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A wrecking bar from a builder's van, used to pry open sheds, car boots and boarded doors. The dusty-red paint survives only along the middle of the bar; the hook and the pry end are rubbed back to dark steel.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.1 m
- Depth (Y): 0.6875 m
- Height (Z): 0.025 m
- Grid: 8 x 55 x 2 cells at 0.0125 m (micro tier), 244 occupied voxels
- Front direction: +Y (library voxel)
- Front: Lies on its side as it would rest on a bench: handle along Y, working end at +Y, lowest point on z = 0. Rotate to the hand for a held pose. The gooseneck lies flat with its claw pointing back toward the bar.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [4.0, 27.5, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it. A 2.5 cm hex bar is one cell at 2.5 cm, too thin to show the gooseneck's taper, the split claw or the flattened pry end; at 1.25 cm the bar is 2x2 cells and the hook is a smooth 8-cell curve. Matches the other small hand tools of the family.

## Materials and colors
`red`, `red_dark`, `steel`, `steel_dark`, `steel_light`

## Details included
- 2x2-cell bar with a gooseneck hook ending in a split nail claw
- Flattened chisel pry end
- Paint worn off at the fulcrum of the hook, the claw and the pry end
- One coherent chipped zone where it was hammered on

## Details excluded
- No hex facets (below cell size)
- No text or brand

## Attachment points
- `grip`: voxel [7, 16, 1], [np.float64(0.0438), np.float64(-0.1375), np.float64(0.0188)] m from the pivot. Main hand on the bar about a third of the way from the pry end.

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.1 x 0.6875 m

## Outputs
- `models/survival/Claude_crowbar/Claude_crowbar.vox` (editable master)
- `models/survival/Claude_crowbar/model.json`
- `models/survival/Claude_crowbar/Claude_crowbar.glb` (derived)
- `previews/survival/Claude_crowbar/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b1_storage_tools.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
