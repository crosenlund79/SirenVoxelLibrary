# Claw Hammer
- Asset ID: Claude_hammer
- Base ID: hammer
- Creator: Claude
- Category: survival
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Tool item 'hammer' (needed to build) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The everyday claw hammer from a kitchen drawer, now the one that builds every barricade. Years of the same hand have darkened the hickory grip; the face is polished bright and the black paint has worn off the claw from pulling nails.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.15 m
- Depth (Y): 0.3875 m
- Height (Z): 0.0375 m
- Grid: 12 x 31 x 3 cells at 0.0125 m (micro tier), 276 occupied voxels
- Front direction: +Y (library voxel)
- Front: Lies on its side as it would rest on a bench: handle along Y, working end at +Y, lowest point on z = 0. Rotate to the hand for a held pose. The claw faces -X (camera side), the striking face +X.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [6.0, 15.5, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it.

## Materials and colors
`charcoal`, `pine_aged`, `pine_hi`, `pine_mid`, `sawdust`, `steel`, `steel_dark`, `steel_hi`

## Details included
- Hickory handle with a slight butt swell and a hand-darkened grip
- Black-painted head with a polished round striking face
- Curved split claw worn to bare steel on the inside
- Handle end grain and wedge visible in the top of the eye

## Details excluded
- No brand stamp or sticker
- No fibreglass/rubber handle

## Attachment points
- `grip`: voxel [6, 6, 1], [np.float64(0.0062), np.float64(-0.1125), np.float64(0.0188)] m from the pivot. Main hand around the darkened lower handle, about 8 cm from the butt.

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.15 x 0.3875 m

## Outputs
- `models/survival/Claude_hammer/Claude_hammer.vox` (editable master)
- `models/survival/Claude_hammer/model.json`
- `models/survival/Claude_hammer/Claude_hammer.glb` (derived)
- `previews/survival/Claude_hammer/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b1_storage_tools.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
