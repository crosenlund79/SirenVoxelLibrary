# Abandoned Bicycle
- Asset ID: Claude_abandoned_bicycle
- Base ID: abandoned_bicycle
- Creator: Claude
- Category: decorations
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_D
- Scale family: full
- Intended uses: Street dressing (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A commuter's bike dropped on the pavement and never picked up. The front wheel folded when something drove over it; the chain has rusted and the saddle has split, but the rear rack still carries a frayed bungee.

Condition: **abandoned**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.625 m
- Depth (Y): 0.9 m
- Height (Z): 0.35 m
- Grid: 65 x 36 x 14 cells at 0.025 m (fine tier), 1,300 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y faces the street or the person using it.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [33.0, 19.0, 0.0])
- Resolution rationale: 2.5 cm cells: a handheld or small gear item whose handles, straps and blades would be 2-4x too thick at 5 cm. Tubes, spokes and the rack need 2.5 cm cells; at 5 cm the frame is a thick outline with no wheel structure.

## Materials and colors
`black`, `charcoal`, `cream_deep`, `leather_deep`, `rust_dark`, `rust_deep`, `safety_orange_dark`, `steel`, `steel_dark`, `steel_light`, `teal`, `teal_dark`

## Details included
- Diamond frame in faded teal lying flat on its right side
- Rear wheel true, front wheel buckled up out of plane
- Handlebar turned and standing up from the ground, left pedal raised
- Rusted chain, split saddle, rear rack with a bungee

## Details excluded
- No brand decals
- No lights or bell (sub-cell)

## Construction and placement notes
- Collision suggestion: Box 1.65 x 0.95 x 0.1 m (flat); trip hazard only.
- Placement footprint: 1.65 x 0.95 m

## Outputs
- `models/decorations/Claude_abandoned_bicycle/Claude_abandoned_bicycle.vox` (editable master)
- `models/decorations/Claude_abandoned_bicycle/model.json`
- `models/decorations/Claude_abandoned_bicycle/Claude_abandoned_bicycle.glb` (derived)
- `previews/decorations/Claude_abandoned_bicycle/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/d2_street.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
