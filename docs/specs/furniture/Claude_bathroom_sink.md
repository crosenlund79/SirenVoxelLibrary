# Bathroom Vanity
- Asset ID: Claude_bathroom_sink
- Base ID: bathroom_sink
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Vanity; game prop 'vanity' (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A teal-painted vanity from the family bathroom, past its best before anything happened: the top hinge of the right door pulled out of the damp chipboard and the door hangs open on the bottom one. A toothbrush is still in its cup, and the tap has left a brown drip stain down to the plug.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.7 m
- Depth (Y): 0.75 m
- Height (Z): 1.0 m
- Grid: 14 x 15 x 20 cells at 0.05 m (detail tier), 1,089 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [6.0, 5.5, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`black`, `brass`, `brass_dark`, `card`, `card_dark`, `chrome`, `glass_hi`, `label_blue`, `paper`, `pine_mid`, `porcelain`, `porcelain_hi`, `porcelain_mid`, `rust_deep`, `steel_light`, `teal`, `teal_dark`, `teal_deep`, `teal_hi`

## Details included
- Ceramic one-piece top with an oval basin, plug and a brown drip stain
- Chrome mixer tap with a lever
- Toothbrush in a glass cup on the back corner
- Teal shaker doors with brass knobs; the right door hangs open and sags
- Inside: chrome U-bend, a toilet roll and a bleach bottle on its side
- Paint chipped to bare wood along the bottom rail

## Details excluded
- No mirror (see Claude_medicine_cabinet)
- No brand on the bottle

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.6 x 0.55 m

## Outputs
- `models/furniture/Claude_bathroom_sink/Claude_bathroom_sink.vox` (editable master)
- `models/furniture/Claude_bathroom_sink/model.json`
- `models/furniture/Claude_bathroom_sink/Claude_bathroom_sink.glb` (derived)
- `previews/furniture/Claude_bathroom_sink/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a4_bath_utility.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
