# Hatchet
- Asset ID: Claude_hatchet
- Base ID: hatchet
- Creator: Claude
- Category: survival
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Tool / melee (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A camping hatchet that became the household's firewood axe. Missed swings chewed the handle under the head, so someone wrapped the grip in black tape; the head was left out in the rain and has rusted around the eye and poll.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.2 m
- Depth (Y): 0.4375 m
- Height (Z): 0.0375 m
- Grid: 16 x 35 x 3 cells at 0.0125 m (micro tier), 357 occupied voxels
- Front direction: +Y (library voxel)
- Front: Lies on its side as it would rest on a bench: handle along Y, working end at +Y, lowest point on z = 0. Rotate to the hand for a held pose. The bit faces -X (camera side), the poll +X.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [8.0, 17.5, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it.

## Materials and colors
`black`, `charcoal`, `pine_aged`, `pine_dark`, `pine_hi`, `pine_light`, `pine_mid`, `rust_dark`, `rust_deep`, `steel`, `steel_dark`, `steel_hi`

## Details included
- Bearded steel head with a bright sharpened edge
- Rust gathered around the eye and the poll, not over the whole head
- Ash handle with a flared knob, black tape wrapped over the grip
- Overstrike bruising on the handle just under the head

## Details excluded
- No leather sheath
- No brand stamp

## Attachment points
- `grip`: voxel [11, 6, 1], [np.float64(0.0438), np.float64(-0.1375), np.float64(0.0188)] m from the pivot. Main hand on the taped grip just above the knob.

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.2 x 0.4375 m

## Outputs
- `models/survival/Claude_hatchet/Claude_hatchet.vox` (editable master)
- `models/survival/Claude_hatchet/model.json`
- `models/survival/Claude_hatchet/Claude_hatchet.glb` (derived)
- `previews/survival/Claude_hatchet/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b1_storage_tools.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
