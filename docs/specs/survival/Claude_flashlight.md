# Flashlight
- Asset ID: Claude_flashlight
- Base ID: flashlight
- Creator: Claude
- Category: survival
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Tool item 'flashlight' (clinic access) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The big rubber flashlight from the hall cupboard, the one that always worked in power cuts. Its lanyard is still looped from the last time someone carried it down to check the basement.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.0875 m
- Depth (Y): 0.3125 m
- Height (Z): 0.0875 m
- Grid: 7 x 25 x 7 cells at 0.0125 m (micro tier), 435 occupied voxels
- Front direction: +Y (library voxel)
- Front: Lies on its side as it would rest on a table: lens points +Y, switch up, lowest point on z = 0.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [3.5, 14.5, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it.

## Materials and colors
`black`, `charcoal`, `glass_hi`, `iron_edge`, `mirror`, `mustard_dark`, `mustard_deep`, `ochre_dark`, `olive`, `steel_dark`, `steel_light`

## Details included
- Ribbed black rubber grip between a mustard-yellow tail cap and head
- Flared head with a bright bezel and a pale, unlit lens
- Rubber switch cover on top
- Paracord lanyard loop lying behind it

## Details excluded
- No emissive lens or light beam
- No brand marks

## Attachment points
- `grip`: voxel [3, 11, 3], [np.float64(0.0), np.float64(-0.0375), np.float64(0.0438)] m from the pivot. Main hand around the ribbed rubber grip, thumb on the switch.

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.0875 x 0.2625 m

## Outputs
- `models/survival/Claude_flashlight/Claude_flashlight.vox` (editable master)
- `models/survival/Claude_flashlight/model.json`
- `models/survival/Claude_flashlight/Claude_flashlight.glb` (derived)
- `previews/survival/Claude_flashlight/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b2_survival_gear.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
