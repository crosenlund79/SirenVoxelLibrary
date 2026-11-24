# Snack Package
- Asset ID: Claude_snack_package
- Base ID: snack_package
- Creator: Claude
- Category: consumables
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_C
- Scale family: full
- Intended uses: Inventory item snacks (hunger +12) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A sealed bag of crisps from a petrol-station shelf, still puffed with air. It is untouched; only the film has crinkled where it was packed in the box.

Condition: **new**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.15 m
- Depth (Y): 0.0875 m
- Height (Z): 0.2125 m
- Grid: 12 x 7 x 17 cells at 0.0125 m (micro tier), 531 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the label / opening side.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [6.0, 3.5, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it.

## Materials and colors
`label_cream`, `terra`, `terra_dark`, `terra_hi`

## Details included
- Pillow-shaped body bulging between flat crimped seals
- Serrated crimp teeth along the top and bottom edges
- Muted paprika film with a plain cream front panel
- Darker crinkle folds fanning from the crimps
- Vertical fin seal on the back

## Details excluded
- No text, logo, mascot or food photograph

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.15 x 0.0875 m

## Outputs
- `models/consumables/Claude_snack_package/Claude_snack_package.vox` (editable master)
- `models/consumables/Claude_snack_package/model.json`
- `models/consumables/Claude_snack_package/Claude_snack_package.glb` (derived)
- `previews/consumables/Claude_snack_package/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/c2_consumables.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
