# Utility Pole
- Asset ID: Claude_utility_pole
- Base ID: utility_pole
- Creator: Claude
- Category: decorations
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_D
- Scale family: full
- Intended uses: Street prop (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The wooden distribution pole at the corner, its line cut and left hanging after a storm or a looter. Years of stapled notices have left a ragged patch at eye height, and the newest one, a missing-person flyer, is still legible from across the street as a pale sheet.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 2.0 m
- Depth (Y): 0.7 m
- Height (Z): 4.8 m
- Grid: 20 x 7 x 48 cells at 0.1 m (standard tier), 578 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y faces the street or the person using it.
- Pivot: Centre of the pole base at ground level. (pivot_voxel [10.5, 2.5, 0.0])
- Resolution rationale: 10 cm cells (the game's structural grid): large silhouettes such as walls, vehicles and trees read clearly without inflating the voxel count.

## Materials and colors
`black`, `card_dark`, `copper`, `galv`, `galv_dark`, `galv_hi`, `glass`, `glass_hi`, `label_cream`, `paper`, `porcelain_shadow`, `rust_dark`, `rust_deep`, `steel_dark`, `wgrey_dark`, `wgrey_hi`, `wgrey_mid`, `wood_deep`, `wood_stain`

## Details included
- 0.3 m creosoted pole weathering from brown at the foot to grey at the top
- Crossarm with braces and four glass insulators
- Pole-top transformer can with bushings, straps and a rust run
- A cut line dangling from the outer insulator on the camera side
- Step bolts, a pale flyer over a ragged patch of old staples and paper

## Details excluded
- No readable flyer text
- No live wires to other poles

## Construction and placement notes
- Collision suggestion: Box 0.3 x 0.3 x 4.8 m at the pivot; crossarm and can non-colliding.

## Outputs
- `models/decorations/Claude_utility_pole/Claude_utility_pole.vox` (editable master)
- `models/decorations/Claude_utility_pole/model.json`
- `models/decorations/Claude_utility_pole/Claude_utility_pole.glb` (derived)
- `previews/decorations/Claude_utility_pole/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/d2_street.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
