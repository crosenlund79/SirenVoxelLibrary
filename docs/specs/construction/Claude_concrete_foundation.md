# Concrete Foundation
- Asset ID: Claude_concrete_foundation
- Base ID: concrete_foundation
- Creator: Claude
- Category: construction
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Concrete foundation module (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A slab section poured last month for a shed that never got built: floated top, a chamfered outside edge, two anchor bolts waiting for a sill plate, and the screed board the builder left on it when the sirens went quiet.

Condition: **new**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.0 m
- Depth (Y): 1.0 m
- Height (Z): 0.4 m
- Grid: 10 x 10 x 4 cells at 0.1 m (standard tier), 243 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the outside face; the module fills its full span.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [5.0, 5.0, 0.0])
- Resolution rationale: 10 cm cells (the game's structural grid): large silhouettes such as walls, vehicles and trees read clearly without inflating the voxel count.

## Materials and colors
`concrete`, `concrete_dark`, `concrete_hi`, `galv`, `pine_aged`, `pine_dark`

## Details included
- Poured slab with a chamfered top edge on the outside (+Y) face
- Two galvanised anchor bolts on the sill line
- Float-finished lighter top, damp foot
- The screed board still lying on it

## Details excluded
- No reinforcement visible
- No cracks (new)

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.0 x 1.0 m

## Outputs
- `models/construction/Claude_concrete_foundation/Claude_concrete_foundation.vox` (editable master)
- `models/construction/Claude_concrete_foundation/model.json`
- `models/construction/Claude_concrete_foundation/Claude_concrete_foundation.glb` (derived)
- `previews/construction/Claude_concrete_foundation/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b3_construction.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
