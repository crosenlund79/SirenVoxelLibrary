# Improvised Forge
- Asset ID: Claude_improvised_forge
- Base ID: improvised_forge
- Creator: Claude
- Category: survival
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Metalworking station (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
Built in the garage after the outage by a neighbour who used to weld: a car brake drum on a steel-pipe stand, a furnace blower on an extension lead and a sheet of scrap steel as a heat shield. A length of rail is the anvil.

Condition: **improvised**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.0 m
- Depth (Y): 0.65 m
- Height (Z): 1.1 m
- Grid: 20 x 13 x 22 cells at 0.05 m (detail tier), 1,012 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the working / interaction side.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [11.0, 7.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`beige`, `beige_dark`, `black`, `card`, `card_dark`, `card_deep`, `card_hi`, `char`, `charcoal`, `coal`, `galv`, `galv_dark`, `galv_hi`, `iron`, `iron_edge`, `iron_warm`, `rust_dark`, `rust_deep`, `soot`, `steel`, `steel_dark`

## Details included
- Brake drum firepot with a charcoal bed (unlit) in its own ash
- Tuyere pipe down through the table to a capped ash dump
- Salvaged squirrel-cage blower on the lower shelf, taped joint, cable
- Scorched scrap-steel heat shield at the back
- Rail-section anvil and long tongs on the table; charcoal sack below

## Details excluded
- No glowing coals or fire
- No fantasy anvil or bellows

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.9 x 0.6 m

## Outputs
- `models/survival/Claude_improvised_forge/Claude_improvised_forge.vox` (editable master)
- `models/survival/Claude_improvised_forge/model.json`
- `models/survival/Claude_improvised_forge/Claude_improvised_forge.glb` (derived)
- `previews/survival/Claude_improvised_forge/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b2_survival_gear.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
