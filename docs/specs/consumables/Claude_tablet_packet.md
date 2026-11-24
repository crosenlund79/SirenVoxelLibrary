# Tablet Packet
- Asset ID: Claude_tablet_packet
- Base ID: tablet_packet
- Creator: Claude
- Category: consumables
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_C
- Scale family: full
- Intended uses: Medicine pickup (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A small carton of tablets found in a coat pocket. The end flap is open and the blister strip has slid half out; two tablets are already gone.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.2 m
- Depth (Y): 0.0875 m
- Height (Z): 0.075 m
- Grid: 16 x 7 x 6 cells at 0.0125 m (micro tier), 219 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the label / opening side.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [8.0, 3.5, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it.

## Materials and colors
`bottle_hi`, `foil`, `label_blue`, `paper`, `porcelain_hi`, `porcelain_mid`, `steel_dark`

## Details included
- White card carton lying flat with a muted blue band
- Open end flap standing up
- Blister strip sliding out, foil side down
- Grid of tablets in clear blisters; one empty blister and one torn-out cell

## Details excluded
- No text, dosage or brand
- No loose tablets

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.2 x 0.0875 m

## Outputs
- `models/consumables/Claude_tablet_packet/Claude_tablet_packet.vox` (editable master)
- `models/consumables/Claude_tablet_packet/model.json`
- `models/consumables/Claude_tablet_packet/Claude_tablet_packet.glb` (derived)
- `previews/consumables/Claude_tablet_packet/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/c2_consumables.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
