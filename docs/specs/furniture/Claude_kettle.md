# Enamel Stovetop Kettle
- Asset ID: Claude_kettle
- Base ID: kettle
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Boiling water on a stove (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A cream enamel kettle that lived on the back burner. Years of being banged onto the grate chipped the enamel round the base and the lid, and the flames left the bottom sooted black. Somebody boiled water in it for days after the power went.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.275 m
- Depth (Y): 0.2 m
- Height (Z): 0.275 m
- Grid: 22 x 16 x 22 cells at 0.0125 m (micro tier), 1,180 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [11.0, 8.0, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it.

## Materials and colors
`black`, `char`, `charcoal`, `cream`, `cream_hi`, `cream_shadow`, `iron`, `iron_dark`, `iron_edge`, `soot`, `steel_dark`

## Details included
- Round-bellied cream enamel body with a lid seam and a black knob
- Dark curved spout rising from the lower belly
- Black handle arching over the lid on two posts
- Soot on the base licking up the sides; enamel chips at the base, the lid rim and the spout root

## Details excluded
- No whistle cap text
- No steam

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.275 x 0.2 m

## Outputs
- `models/furniture/Claude_kettle/Claude_kettle.vox` (editable master)
- `models/furniture/Claude_kettle/model.json`
- `models/furniture/Claude_kettle/Claude_kettle.glb` (derived)
- `previews/furniture/Claude_kettle/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a3_kitchen.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
