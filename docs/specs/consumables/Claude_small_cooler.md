# Small Cooler
- Asset ID: Claude_small_cooler
- Base ID: small_cooler
- Creator: Claude
- Category: consumables
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_C
- Scale family: full
- Intended uses: Food storage (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A picnic cooler that went to every beach weekend for fifteen years. The teal has faded, the corners are scuffed pale, and now it keeps a few cans cool in a dark garage instead of drinks in the sun.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.45 m
- Depth (Y): 0.325 m
- Height (Z): 0.3 m
- Grid: 18 x 13 x 12 cells at 0.025 m (fine tier), 938 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the label / opening side.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [9.0, 6.5, 0.0])
- Resolution rationale: 2.5 cm cells: a handheld or small gear item whose handles, straps and blades would be 2-4x too thick at 5 cm.

## Materials and colors
`almond`, `almond_dark`, `charcoal`, `iron_edge`, `porcelain_mid`, `teal`, `teal_dark`, `teal_deep`, `teal_hi`

## Details included
- Faded teal body with chamfered corners and a moulded lid seat
- Pale lid with a front lip
- Swing handle folded back over the hinges
- Drain plug low on the front
- Scuffed corners and grimy base

## Details excluded
- No brand or text
- No ice or contents shown

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.45 x 0.325 m

## Outputs
- `models/consumables/Claude_small_cooler/Claude_small_cooler.vox` (editable master)
- `models/consumables/Claude_small_cooler/model.json`
- `models/consumables/Claude_small_cooler/Claude_small_cooler.glb` (derived)
- `previews/consumables/Claude_small_cooler/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/c2_consumables.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
