# Wardrobe
- Asset ID: Claude_wardrobe
- Base ID: wardrobe
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Clothes storage; lootable; game prop 'wardrobe' (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A white flat-pack wardrobe in the back bedroom. The far door was left open after someone grabbed clothes for a few days - there are gaps on the rail - and the old suitcase on top was not the one they took. Years of shoes kicking the near door shut left grey marks along its foot.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.6 m
- Depth (Y): 1.3 m
- Height (Z): 2.0 m
- Grid: 32 x 26 x 40 cells at 0.05 m (detail tier), 5,455 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [15.5, 6.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`ash`, `ash_dark`, `bluegrey`, `brass`, `card`, `concrete`, `cream_mid`, `denim_dark`, `green_dark`, `khaki_dark`, `leather`, `leather_dark`, `leather_deep`, `leather_hi`, `mauve_dark`, `paint_white`, `paint_white_shadow`, `porcelain_deep`, `porcelain_mid`, `porcelain_shadow`, `red_dark`, `slate_dark`, `steel`, `steel_dark`, `steel_light`, `terra_dark`

## Details included
- Shaker-style doors on a recessed plinth under a plain cornice
- Far (+X) door open: hanging rail with clothes and gaps, a shelf above
- Leather suitcase with straps lying on top
- Grey kick marks at the foot of the closed near (-X) door

## Details excluded
- No mirror
- No loose shoes on the floor

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.55 x 0.6 m

## Outputs
- `models/furniture/Claude_wardrobe/Claude_wardrobe.vox` (editable master)
- `models/furniture/Claude_wardrobe/model.json`
- `models/furniture/Claude_wardrobe/Claude_wardrobe.glb` (derived)
- `previews/furniture/Claude_wardrobe/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a2_bedroom_office.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
