# Healthy Pine
- Asset ID: Claude_healthy_pine
- Base ID: healthy_pine
- Creator: Claude
- Category: vegetation
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_D
- Scale family: full
- Intended uses: Forest/yard tree (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A self-sown pine at the back of a garden that nobody got round to taking down. It is thriving now: dense dark tiers, the windward side clipped short by winter storms, one low limb on the path side browning where road salt splashed it.

Condition: **living**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 2.7 m
- Depth (Y): 2.6 m
- Height (Z): 5.1 m
- Grid: 27 x 26 x 51 cells at 0.1 m (standard tier), 3,437 occupied voxels
- Front direction: +Y (library voxel)
- Front: No functional front; character details face the default camera (-X/+Y).
- Pivot: Trunk base centre at ground level; the crown is slightly lopsided toward the lee (+X) side. (pivot_voxel [12.0, 13.0, 0.0])
- Resolution rationale: 10 cm cells (the game's structural grid): large silhouettes such as walls, vehicles and trees read clearly without inflating the voxel count.

## Materials and colors
`bark`, `bark_dark`, `bark_deep`, `bark_mid`, `conifer`, `conifer_dark`, `conifer_deep`, `conifer_hi`, `conifer_mid`, `needle_dark`, `needle_dry`, `needle_olive`, `needle_rust`, `snag`

## Details included
- Eleven hand-authored whorls of drooping, slightly upturned limbs carrying layered needle pads
- Gaps between tiers so the layering reads from the game camera
- Short windward (-X) limbs, a top whorl that lost a limb
- Bare lower trunk with two old snapped stubs and gripping root flares
- One browning lower limb on the camera side

## Details excluded
- No pine cones (sub-cell)
- No random scatter of needle colours

## Construction and placement notes
- Collision suggestion: Capsule r=0.15 m, h=5.1 m at the pivot (trunk); foliage non-colliding.

## Outputs
- `models/vegetation/Claude_healthy_pine/Claude_healthy_pine.vox` (editable master)
- `models/vegetation/Claude_healthy_pine/model.json`
- `models/vegetation/Claude_healthy_pine/Claude_healthy_pine.glb` (derived)
- `previews/vegetation/Claude_healthy_pine/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/d1_vegetation.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
