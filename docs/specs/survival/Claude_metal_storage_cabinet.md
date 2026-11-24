# Metal Storage Cabinet
- Asset ID: Claude_metal_storage_cabinet
- Base ID: metal_storage_cabinet
- Creator: Claude
- Category: survival
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Secure storage (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
Bought for the garage to keep the chemicals and the good tools locked up. Someone tried to force it with a bar: the right-hand door is dented and the paint is scraped bright around the handle and hasp, but the padlock held.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.85 m
- Depth (Y): 0.5 m
- Height (Z): 1.85 m
- Grid: 17 x 10 x 37 cells at 0.05 m (detail tier), 2,014 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the working / interaction side.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [8.5, 4.5, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`brass`, `brass_dark`, `charcoal`, `chrome`, `rust_dark`, `rust_deep`, `steel`, `steel_dark`, `steel_hi`, `steel_light`

## Details included
- Two flush doors with a dark centre gap and a recessed plinth
- Pressed louvres top and bottom on both doors
- Lever handle and a welded hasp with a brass padlock
- Crowbar dent in the right-hand door, scrape marks around the handle
- Rust creeping up the bottom corners where the floor was wet

## Details excluded
- No hazard stickers or labels
- No interior shelves (doors closed)

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.85 x 0.45 m

## Outputs
- `models/survival/Claude_metal_storage_cabinet/Claude_metal_storage_cabinet.vox` (editable master)
- `models/survival/Claude_metal_storage_cabinet/model.json`
- `models/survival/Claude_metal_storage_cabinet/Claude_metal_storage_cabinet.glb` (derived)
- `previews/survival/Claude_metal_storage_cabinet/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b1_storage_tools.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
