# Concrete Seawall
- Asset ID: Claude_seawall
- Base ID: seawall
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map infrastructure piece (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A stretch of stepped concrete seawall below the beach promenade. Storm waves have stained the lower steps green and opened one expansion joint.

Condition: **worn**.

## Silhouette
Long, three-step concrete revetment, green-stained at the foot, pale coping on top.

## Dimensions and orientation
- Width (X): 10.0 m
- Depth (Y): 1.5 m
- Height (Z): 2.0 m
- Grid: 20 x 3 x 4 cells at 0.5 m (map tier), 180 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the stepped sea face (shown to the camera); the flat promenade side is -Y.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [10.0, 1.5, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled.

## Materials and colors
`algae`, `algae_dark`, `black`, `concrete`, `concrete_dark`, `concrete_deep`, `concrete_hi`

## Details included
- Three 0.5 m steps facing the sea with a pale coping on the promenade edge
- Algae and wet staining on the lowest step
- Expansion joint and a drain outfall in the bottom riser

## Details excluded
- No water, no railings

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 10.0 x 1.5 m

## Outputs
- `models/map/Claude_seawall/Claude_seawall.vox` (editable master)
- `models/map/Claude_seawall/model.json`
- `models/map/Claude_seawall/Claude_seawall.glb` (derived)
- `previews/map/Claude_seawall/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e2_map_infrastructure.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
