# Water Barrel
- Asset ID: Claude_water_barrel
- Base ID: water_barrel
- Creator: Claude
- Category: survival
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Water storage (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A 200-litre food drum scrounged from the bakery, set on two cinder blocks by the back door. Someone drilled in a brass garden tap; it drips, and the drum and the block beneath are green where it does. A tin mug lives on the lid.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.6 m
- Depth (Y): 0.7 m
- Height (Z): 1.1 m
- Grid: 12 x 14 x 22 cells at 0.05 m (detail tier), 1,175 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the working / interaction side.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [6.0, 6.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`algae`, `algae_dark`, `blue_dark`, `bluegrey`, `bluegrey_dark`, `bluegrey_deep`, `bluegrey_hi`, `brass`, `brass_dark`, `brass_hi`, `concrete`, `concrete_dark`, `concrete_hi`, `cream`, `cream_mid`, `teal_dark`

## Details included
- Blue-grey plastic drum with two moulded rolling grooves
- Tight-head top with chime and two screw bungs, sun-faded
- Retrofitted brass tap low on the front, algae streak under it
- Two cinder blocks laid on their sides, cores showing
- Enamel mug left on the lid

## Details excluded
- No hoses or pumps
- No hazard or food labels

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.6 x 0.6 m

## Outputs
- `models/survival/Claude_water_barrel/Claude_water_barrel.vox` (editable master)
- `models/survival/Claude_water_barrel/model.json`
- `models/survival/Claude_water_barrel/Claude_water_barrel.glb` (derived)
- `previews/survival/Claude_water_barrel/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b2_survival_gear.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
