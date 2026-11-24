# Cooking Pot
- Asset ID: Claude_cooking_pot
- Base ID: cooking_pot
- Creator: Claude
- Category: survival
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Cooking on stoves/campfires (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A thin aluminium stockpot that has cooked every meal over the backyard fire since the outage. The bottom is black with soot, a dent on one side from being dropped, and the lid sits slightly crooked.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.35 m
- Depth (Y): 0.3 m
- Height (Z): 0.275 m
- Grid: 14 x 12 x 11 cells at 0.025 m (fine tier), 650 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the working / interaction side.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [7.0, 6.0, 0.0])
- Resolution rationale: 2.5 cm cells: a handheld or small gear item whose handles, straps and blades would be 2-4x too thick at 5 cm.

## Materials and colors
`black`, `charcoal`, `galv`, `galv_dark`, `galv_hi`, `iron`, `iron_dark`, `soot`, `steel_dark`

## Details included
- 30 cm stockpot with a rolled rim and riveted ear handles
- Soot climbing irregularly from the bottom
- A dent on the camera side
- Lid with a black knob, slightly askew

## Details excluded
- No food or steam
- No brand stamp

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.3 x 0.3 m

## Outputs
- `models/survival/Claude_cooking_pot/Claude_cooking_pot.vox` (editable master)
- `models/survival/Claude_cooking_pot/model.json`
- `models/survival/Claude_cooking_pot/Claude_cooking_pot.glb` (derived)
- `previews/survival/Claude_cooking_pot/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b2_survival_gear.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
