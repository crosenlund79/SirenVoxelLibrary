# Backpack
- Asset ID: Claude_backpack
- Base ID: backpack
- Creator: Claude
- Category: survival
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Tool item 'backpack' (+50% loot) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
An olive canvas pack, the same as the one the player carries: a foam sleeping mat strapped beneath it, a bottle in the side pocket, and the base scuffed grey from being dropped on gravel.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.425 m
- Depth (Y): 0.25 m
- Height (Z): 0.55 m
- Grid: 17 x 10 x 22 cells at 0.025 m (fine tier), 1,159 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the outer face (pockets); the shoulder straps are on -Y.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [8.5, 4.5, 0.0])
- Resolution rationale: 2.5 cm cells: a handheld or small gear item whose handles, straps and blades would be 2-4x too thick at 5 cm.

## Materials and colors
`bottle`, `bottle_cap`, `charcoal`, `iron`, `khaki_dark`, `olive`, `olive_dark`, `olive_hi`, `steel_light`, `teal`, `teal_dark`, `teal_deep`

## Details included
- Rounded canvas body with a top lid flap and two buckled straps
- Front pocket with a zip line
- Side mesh pocket with a water bottle
- Rolled foam mat strapped under the base
- Padded shoulder straps on the back

## Details excluded
- No patches, logos or text
- No hanging gear clutter

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.375 x 0.175 m

## Outputs
- `models/survival/Claude_backpack/Claude_backpack.vox` (editable master)
- `models/survival/Claude_backpack/model.json`
- `models/survival/Claude_backpack/Claude_backpack.glb` (derived)
- `previews/survival/Claude_backpack/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b2_survival_gear.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
