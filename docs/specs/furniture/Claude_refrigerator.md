# Almond Fridge-Freezer
- Asset ID: Claude_refrigerator
- Base ID: refrigerator
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Fridge-freezer; lootable; game prop 'fridge' (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A twenty-year-old almond fridge-freezer that outlived two kitchens. A shopping note and a child's drawing are still held by magnets; the door seal on the opening side has come loose and hangs out, and damp under it has bloomed into rust along the bottom corner.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.85 m
- Depth (Y): 0.7 m
- Height (Z): 1.8 m
- Grid: 17 x 14 x 36 cells at 0.05 m (detail tier), 2,224 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [9.5, 6.5, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`almond`, `almond_dark`, `black`, `charcoal`, `cream`, `cream_deep`, `cream_mid`, `cream_shadow`, `iron_edge`, `leaf`, `mustard`, `mustard_dark`, `porcelain_hi`, `rust`, `rust_dark`, `rust_deep`, `signal_red_dark`, `steel`, `steel_dark`, `steel_light`, `teal_dark`, `terra`

## Details included
- Freezer door over a taller fridge door, dark seam between them
- Soft rounded top edge; slightly darker side panels; door gasket seam on the sides
- Steel bar handles on the opening (left) side
- Paper note and a child's drawing held by three magnets
- Loose rubber door seal hanging from the opening edge
- Rust bloom at the bottom front corner and on the kick grille

## Details excluded
- No brand badge
- No ice dispenser
- No readable writing on the note

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.75 x 0.65 m

## Outputs
- `models/furniture/Claude_refrigerator/Claude_refrigerator.vox` (editable master)
- `models/furniture/Claude_refrigerator/model.json`
- `models/furniture/Claude_refrigerator/Claude_refrigerator.glb` (derived)
- `previews/furniture/Claude_refrigerator/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a3_kitchen.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
