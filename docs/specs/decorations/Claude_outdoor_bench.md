# Outdoor Bench
- Asset ID: Claude_outdoor_bench
- Base ID: outdoor_bench
- Creator: Claude
- Category: decorations
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_D
- Scale family: full
- Intended uses: Park/street prop (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A memorial park bench facing the pond path. The slats have silvered and split, one back slat broke in the middle and sags, and the little brass plaque is the only part someone still polished.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.55 m
- Depth (Y): 0.6 m
- Height (Z): 0.85 m
- Grid: 31 x 12 x 17 cells at 0.05 m (detail tier), 496 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y faces the street or the person using it.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [15.5, 6.5, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`brass`, `brass_hi`, `break_fresh`, `iron`, `iron_dark`, `iron_edge`, `rust_deep`, `wgrey`, `wgrey_hi`, `wgrey_mid`, `wgrey_warm`, `wgrey_wet`

## Details included
- Cast-iron ends with legs, scrolled arms and a reclined back support
- Four seat and two back slats of silvered timber with darker wet ends
- Broken lower back slat sagging in the middle
- Small brass memorial plaque (plain block, no text)
- Rust bleeding from the end fixings

## Details excluded
- No readable plaque text
- No litter

## Construction and placement notes
- Collision suggestion: Box 1.55 x 0.6 x 0.45 m (seat) plus a back plane.
- Placement footprint: 1.35 x 0.55 m

## Outputs
- `models/decorations/Claude_outdoor_bench/Claude_outdoor_bench.vox` (editable master)
- `models/decorations/Claude_outdoor_bench/model.json`
- `models/decorations/Claude_outdoor_bench/Claude_outdoor_bench.glb` (derived)
- `previews/decorations/Claude_outdoor_bench/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/d2_street.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
