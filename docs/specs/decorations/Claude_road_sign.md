# Road Sign
- Asset ID: Claude_road_sign
- Base ID: road_sign
- Creator: Claude
- Category: decorations
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_D
- Scale family: full
- Intended uses: Street prop (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The stop sign at the end of the residential street. A reversing van clipped it and bent the post back; nobody came to straighten it, and the face is fading.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.65 m
- Depth (Y): 0.25 m
- Height (Z): 2.45 m
- Grid: 13 x 5 x 49 cells at 0.05 m (detail tier), 177 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y faces the street or the person using it.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [6.5, 4.5, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`galv`, `galv_hi`, `paint_white_shadow`, `rust_deep`, `signal_red`, `steel_dark`

## Details included
- Octagonal red face with a pale rim and a broken pale band suggesting a legend (blocks, not letters)
- Square galvanised post bent backward at 0.55 m, the sign tilting with it
- Scraped zinc at the bend, rust at the foot

## Details excluded
- No readable text
- No street-name blades

## Construction and placement notes
- Collision suggestion: Box 0.06 x 0.06 x 2.4 m (post); the sign face is non-colliding.

## Outputs
- `models/decorations/Claude_road_sign/Claude_road_sign.vox` (editable master)
- `models/decorations/Claude_road_sign/model.json`
- `models/decorations/Claude_road_sign/Claude_road_sign.glb` (derived)
- `previews/decorations/Claude_road_sign/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/d2_street.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
