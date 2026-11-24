# Pickaxe
- Asset ID: Claude_pickaxe
- Base ID: pickaxe
- Creator: Claude
- Category: survival
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Mining tool (quarry) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A pick from the landscaping company's yard, taken to dig through the frozen verge and later to quarry stone. The head is rusted where it lay in the wet, the point and chisel are scraped bright, and the haft is grey from weather.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.5 m
- Depth (Y): 0.85 m
- Height (Z): 0.075 m
- Grid: 20 x 34 x 3 cells at 0.025 m (fine tier), 244 occupied voxels
- Front direction: +Y (library voxel)
- Front: Lies on its side as it would rest on a bench: handle along Y, working end at +Y, lowest point on z = 0. Rotate to the hand for a held pose. The point faces -X (camera side), the chisel +X.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [10.0, 17.0, 0.0])
- Resolution rationale: 2.5 cm cells: a handheld or small gear item whose handles, straps and blades would be 2-4x too thick at 5 cm.

## Materials and colors
`iron`, `iron_edge`, `pine_aged`, `rust_dark`, `rust_deep`, `steel`, `steel_light`, `wgrey_hi`, `wgrey_mid`, `wgrey_warm`

## Details included
- Curved head: long point on one side, chisel on the other
- Rust on the arms, bright steel at the point and chisel edge
- Weathered ash haft with a swelled butt and a darker grip
- Splintered overstrike zone under the head

## Details excluded
- No fantasy double-axe head
- No brand

## Attachment points
- `grip`: voxel [9, 4, 1], [np.float64(-0.0125), np.float64(-0.3125), np.float64(0.0375)] m from the pivot. Main hand near the butt swell; the other hand slides up the haft.

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.5 x 0.85 m

## Outputs
- `models/survival/Claude_pickaxe/Claude_pickaxe.vox` (editable master)
- `models/survival/Claude_pickaxe/model.json`
- `models/survival/Claude_pickaxe/Claude_pickaxe.glb` (derived)
- `previews/survival/Claude_pickaxe/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b1_storage_tools.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
