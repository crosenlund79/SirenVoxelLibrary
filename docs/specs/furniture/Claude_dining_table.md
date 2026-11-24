# Family Oak Dining Table
- Asset ID: Claude_dining_table
- Base ID: dining_table
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Dining-room furniture; a work and eating surface in the defended house; cover/obstacle; set dressing for kitchen and dining scenes. (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
An everyday family table, well used and looked after: forearm-polished places along the front, a faint mug ring nobody sanded out and a stretcher polished by restless feet. Left clean when the family went; plates and candles are separate models.

Condition: **used**.

## Silhouette
Broad flat top with breadboard ends over a plain apron and four square legs; the H-stretcher reads through the legs from the three-quarter camera.

## Dimensions and orientation
- Width (X): 1.6 m
- Depth (Y): 0.9 m
- Height (Z): 0.75 m
- Grid: 32 x 18 x 15 cells at 0.05 m (detail tier), 1,048 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the long side with the polished places; the table is symmetric enough to be placed either way round.
- Pivot: Bottom centre of the 1.60 x 0.90 m footprint. (pivot_voxel [np.float64(16.0), np.float64(9.0), 0.0])
- Resolution rationale: 0.05 m matches the other household furniture (pilot bed and workbench), so tables, chairs and beds share one voxel rhythm in a room. A 5 cm top, 10 cm legs and apron are real joinery sizes; at 0.10 m the top would be a 10 cm slab and the stretcher would disappear.

## Materials and colors
`pine_aged`, `pine_hi`, `pine_light`, `pine_mid`

## Details included
- Three top boards in alternating oak tones; breadboard ends with darker cross grain
- Two forearm-polished places on the front arris, a faint mug ring
- H-stretcher with a polished centre rail
- Floor grime on the feet, one scuffed leg

## Details excluded
- No crockery or clutter baked onto the top (use Claude_crockery_set)
- No random speckle noise; wear only where hands, mugs and feet go

## Construction and placement notes
- Collision suggestion: Box 1.60 x 0.90 x 0.75 m at the pivot (or four leg boxes + top slab).
- Placement footprint: 1.6 x 0.9 m

## Outputs
- `models/furniture/Claude_dining_table/Claude_dining_table.vox` (editable master)
- `models/furniture/Claude_dining_table/model.json`
- `models/furniture/Claude_dining_table/Claude_dining_table.glb` (derived)
- `previews/furniture/Claude_dining_table/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/dining_table.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
