# Streetlight
- Asset ID: Claude_streetlight
- Base ID: streetlight
- Creator: Claude
- Category: decorations
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_D
- Scale family: full
- Intended uses: Street prop (game streetlight_dead) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The streetlight outside a row of houses, dark since the grid went down. Someone has prised off the access cover at its foot to strip the copper, and rust is creeping up from the base.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.4 m
- Depth (Y): 1.6 m
- Height (Z): 4.3 m
- Grid: 4 x 16 x 43 cells at 0.1 m (standard tier), 261 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y faces the street or the person using it.
- Pivot: Centre of the pole base at ground level (not the bounding-box centre). (pivot_voxel [2.0, 2.0, 0.0])
- Resolution rationale: 10 cm cells (the game's structural grid): large silhouettes such as walls, vehicles and trees read clearly without inflating the voxel count.

## Materials and colors
`black`, `charcoal`, `concrete`, `concrete_dark`, `galv`, `galv_dark`, `galv_hi`, `glass_dark`, `glass_deep`, `iron`, `rust_deep`, `soot`, `steel_dark`

## Details included
- Galvanised 0.2 m pole on a concrete footing with a bolted flange
- Curved arm reaching 1.4 m over the road (+Y) to a cobra-head lantern with a dark, unlit lens and a photocell
- Access cover missing at the foot, dark cavity
- Rust at the flange and the bottom of the pole

## Details excluded
- No lit or emissive lamp
- No banners or signs

## Construction and placement notes
- Collision suggestion: Cylinder r=0.12 m, h=4.2 m at the pivot; the arm is non-colliding.

## Outputs
- `models/decorations/Claude_streetlight/Claude_streetlight.vox` (editable master)
- `models/decorations/Claude_streetlight/model.json`
- `models/decorations/Claude_streetlight/Claude_streetlight.glb` (derived)
- `previews/decorations/Claude_streetlight/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/d2_street.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
