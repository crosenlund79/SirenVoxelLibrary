# Shovel
- Asset ID: Claude_shovel
- Base ID: shovel
- Creator: Claude
- Category: survival
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Digging tool (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The garden shovel that dug the latrine and the graves behind the house. Dried clay is caked at the tip and in the corners of the blade; the paint has worn off the cutting edge and the ash shaft is dark where two hands always hold it.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.2 m
- Depth (Y): 1.15 m
- Height (Z): 0.075 m
- Grid: 8 x 46 x 3 cells at 0.025 m (fine tier), 294 occupied voxels
- Front direction: +Y (library voxel)
- Front: Lies on its side as it would rest on a bench: handle along Y, working end at +Y, lowest point on z = 0. Rotate to the hand for a held pose.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [4.0, 23.0, 0.0])
- Resolution rationale: 2.5 cm cells: a handheld or small gear item whose handles, straps and blades would be 2-4x too thick at 5 cm.

## Materials and colors
`card`, `card_dark`, `card_deep`, `green_dark`, `green_deep`, `iron`, `pine_aged`, `pine_hi`, `pine_light`, `pine_mid`, `steel`, `steel_dark`, `steel_light`

## Details included
- Round-point dished blade with turned steps for the boot
- Riveted socket on an ash shaft
- Wooden D-grip with a steel Y-ferrule
- Dried clay at the tip and in the step corners, bare steel at the edge

## Details excluded
- No fresh wet mud
- No brand sticker

## Attachment points
- `grip`: voxel [3, 0, 1], [np.float64(-0.0125), np.float64(-0.5625), np.float64(0.0375)] m from the pivot. Main hand on the D-grip crossbar; the other hand low on the shaft.

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.2 x 1.15 m

## Outputs
- `models/survival/Claude_shovel/Claude_shovel.vox` (editable master)
- `models/survival/Claude_shovel/model.json`
- `models/survival/Claude_shovel/Claude_shovel.glb` (derived)
- `previews/survival/Claude_shovel/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b1_storage_tools.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
