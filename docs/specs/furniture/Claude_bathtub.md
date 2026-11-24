# Bathtub
- Asset ID: Claude_bathtub
- Base ID: bathtub
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Bathroom fixture; water storage; game prop 'bathtub' (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
When the mains failed, the family filled the bath while the pressure lasted and used it as their water tank. A plank laid across the far end holds the saucepan they dipped with; the level has dropped well below the grey line where it first stood.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.75 m
- Depth (Y): 0.75 m
- Height (Z): 0.7 m
- Grid: 35 x 15 x 14 cells at 0.05 m (detail tier), 2,528 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the open front panel; the back and both ends go against walls.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [17.5, 7.5, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`charcoal`, `chrome`, `pine_aged`, `pine_light`, `pine_mid`, `porcelain`, `porcelain_hi`, `porcelain_mid`, `porcelain_shadow`, `steel_dark`, `steel_light`, `teal`, `teal_dark`, `teal_hi`, `water`, `water_hi`

## Details included
- Built-in enamel tub with a tiled-in front panel and a recessed plinth
- Sloped back at the head end, flat end under the taps
- Deck-mounted chrome mixer with two cross-head taps and an overflow plate
- Stored water (opaque) with a scum line well above the current level
- Pine plank across the tub carrying a steel saucepan used as a dipper

## Details excluded
- No bath toys or shower curtain
- No transparency

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.75 x 0.75 m

## Outputs
- `models/furniture/Claude_bathtub/Claude_bathtub.vox` (editable master)
- `models/furniture/Claude_bathtub/model.json`
- `models/furniture/Claude_bathtub/Claude_bathtub.glb` (derived)
- `previews/furniture/Claude_bathtub/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a4_bath_utility.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
