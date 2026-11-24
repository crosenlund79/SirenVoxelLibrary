# Tree Stump
- Asset ID: Claude_tree_stump
- Base ID: tree_stump
- Creator: Claude
- Category: vegetation
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_D
- Scale family: full
- Intended uses: Forest/logging dressing (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A street tree felled by the council a season before the sirens stopped; the stump was never ground out. The cut has weathered but still shows its rings, the felling hinge and a drying crack, and a sucker is trying to regrow.

Condition: **dead**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.75 m
- Depth (Y): 0.7 m
- Height (Z): 0.5 m
- Grid: 15 x 14 x 10 cells at 0.05 m (detail tier), 477 occupied voxels
- Front direction: +Y (library voxel)
- Front: No functional front; character details face the default camera (-X/+Y).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [7.5, 6.5, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`bark`, `bark_dark`, `bark_mid`, `leaf`, `leaf_hi`, `leaf_mid`, `moss`, `moss_dark`, `pine_aged`, `pine_dark`, `pine_light`, `pine_mid`, `twig`, `wood_deep`, `wood_stain`

## Details included
- Round 0.5 m stump with five root buttresses gripping the ground
- Saw-cut top with growth rings, dark pith and pale sapwood
- Felling step: the back cut stands one cell above the notch, with torn hinge fibres
- Radial drying crack
- Moss on the shaded north (-Y) foot
- A green sucker shoot on the camera side

## Details excluded
- No chainsaw marks finer than a cell
- No mushrooms (confetti)

## Construction and placement notes
- Collision suggestion: Cylinder r=0.3 m, h=0.5 m.
- Placement footprint: 0.55 x 0.55 m

## Outputs
- `models/vegetation/Claude_tree_stump/Claude_tree_stump.vox` (editable master)
- `models/vegetation/Claude_tree_stump/model.json`
- `models/vegetation/Claude_tree_stump/Claude_tree_stump.glb` (derived)
- `previews/vegetation/Claude_tree_stump/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/d1_vegetation.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
