# Grass Clump
- Asset ID: Claude_grass_clump
- Base ID: grass_clump
- Creator: Claude
- Category: vegetation
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_D
- Scale family: full
- Intended uses: Ground dressing (game grass tufts) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A tussock of rough grass that has seeded itself in a crack at the edge of a lawn nobody mows any more, with a broad-leaved weed and one tall seed stalk pushing through it.

Condition: **living**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.65 m
- Depth (Y): 0.475 m
- Height (Z): 0.45 m
- Grid: 26 x 19 x 18 cells at 0.025 m (fine tier), 538 occupied voxels
- Front direction: +Y (library voxel)
- Front: No functional front; character details face the default camera (-X/+Y).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [13.0, 9.5, 0.0])
- Resolution rationale: 2.5 cm cells: a handheld or small gear item whose handles, straps and blades would be 2-4x too thick at 5 cm. Blades need 2.5 cm cells; at 5 cm the clump is a dozen thick sticks.

## Materials and colors
`dead_leaf`, `dead_leaf_dark`, `grass`, `grass_dry`, `grass_hi`, `leaf`, `leaf_dark`, `leaf_hi`, `leaf_mid`, `soil_dark`, `twig`

## Details included
- 24 hand-placed blades arching outward from one crown, green bodies with straw-dry tips
- Last year's dead blades flopped over at the sides
- A broad-leaved weed rosette and one tall seed stalk
- Dense dark root crown

## Details excluded
- No flowers
- No soil disc (sits on any ground)

## Construction and placement notes
- Collision suggestion: None (walk-through dressing).
- Placement footprint: 0.2 x 0.175 m

## Outputs
- `models/vegetation/Claude_grass_clump/Claude_grass_clump.vox` (editable master)
- `models/vegetation/Claude_grass_clump/model.json`
- `models/vegetation/Claude_grass_clump/Claude_grass_clump.glb` (derived)
- `previews/vegetation/Claude_grass_clump/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/d1_vegetation.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
