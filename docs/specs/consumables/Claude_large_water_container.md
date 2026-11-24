# Large Water Container
- Asset ID: Claude_large_water_container
- Base ID: large_water_container
- Creator: Claude
- Category: consumables
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_C
- Scale family: full
- Intended uses: Bulk water storage (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A 20-litre camping water container that used to live in a car boot for summer trips. It has been refilled from the rain barrel many times; the base is scuffed and grey with grime and the spigot cap is a slightly different blue.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.275 m
- Depth (Y): 0.275 m
- Height (Z): 0.45 m
- Grid: 11 x 11 x 18 cells at 0.025 m (fine tier), 819 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the label / opening side.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [5.5, 5.5, 0.0])
- Resolution rationale: 2.5 cm cells: a handheld or small gear item whose handles, straps and blades would be 2-4x too thick at 5 cm.

## Materials and colors
`blue_dark`, `bluegrey`, `bluegrey_deep`, `bottle`, `bottle_cap`, `charcoal`, `label_blue`, `navy`

## Details included
- Rounded block body with a moulded carry handle bridging the top
- Fill cap on the top, screw cap with a spigot tap low on the front
- Moulded horizontal stacking groove around the body
- Scuffed, grimy base and front corners

## Details excluded
- No brand, volume markings or text

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.275 x 0.275 m

## Outputs
- `models/consumables/Claude_large_water_container/Claude_large_water_container.vox` (editable master)
- `models/consumables/Claude_large_water_container/model.json`
- `models/consumables/Claude_large_water_container/Claude_large_water_container.glb` (derived)
- `previews/consumables/Claude_large_water_container/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/c2_consumables.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
