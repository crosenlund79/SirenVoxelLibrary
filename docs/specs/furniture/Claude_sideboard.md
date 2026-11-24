# Sideboard
- Asset ID: Claude_sideboard
- Base ID: sideboard
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Dining storage; lootable (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The good walnut sideboard in the dining room. Someone went through it for the candles and left the near drawer pulled out; the fruit bowl is still on top, and the wedding photo beside it was laid face-down and left that way.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.75 m
- Depth (Y): 0.75 m
- Height (Z): 0.9 m
- Grid: 35 x 15 x 18 cells at 0.05 m (detail tier), 1,882 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [17.5, 5.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`brass`, `brass_dark`, `card_dark`, `cream_mid`, `pine_aged`, `pine_dark`, `teal`, `teal_dark`, `wood_deep`, `wood_stain`

## Details included
- Three drawers over two frame-and-panel doors on short legs, brass pulls
- Near drawer pulled out, paper lining inside
- Stoneware fruit bowl on top
- Picture frame lying face-down, cardboard back showing

## Details excluded
- No fruit or crockery inside the bowl (separate pickups)

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.75 x 0.5 m

## Outputs
- `models/furniture/Claude_sideboard/Claude_sideboard.vox` (editable master)
- `models/furniture/Claude_sideboard/model.json`
- `models/furniture/Claude_sideboard/Claude_sideboard.glb` (derived)
- `previews/furniture/Claude_sideboard/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a1_living_room.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
