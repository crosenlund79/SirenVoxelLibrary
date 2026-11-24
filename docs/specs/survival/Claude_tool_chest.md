# Tool Chest
- Asset ID: Claude_tool_chest
- Base ID: tool_chest
- Creator: Claude
- Category: survival
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Tool storage (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A mechanic's rolling chest from the auto shop on the corner, dragged home for the generator tools. The top drawer was left open with a few spanners in it; a greasy shop rag still hangs over the side handle.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.875 m
- Depth (Y): 0.5 m
- Height (Z): 0.475 m
- Grid: 35 x 20 x 19 cells at 0.025 m (fine tier), 2,542 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the working / interaction side.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [19.0, 7.0, 0.0])
- Resolution rationale: 2.5 cm cells: a handheld or small gear item whose handles, straps and blades would be 2-4x too thick at 5 cm. At 5 cm a 0.47 m chest is nine cells tall: its drawers, pulls and casters would be single cells. At 2.5 cm the four drawers, full-width pulls, swivel casters and the open drawer's contents read; the voxel count stays modest.

## Materials and colors
`black`, `blue`, `blue_dark`, `blue_deep`, `blue_hi`, `blue_mid`, `charcoal`, `chrome`, `iron`, `red`, `red_dark`, `red_deep`, `red_hi`, `soot`, `steel`, `steel_dark`, `steel_hi`, `steel_light`

## Details included
- Four drawers with full-width aluminium pulls, the top one pulled open
- Spanners and a socket in the open drawer
- Ribbed rubber mat on the top
- Four swivel casters
- Tube side handle with a greasy rag draped over it
- Paint scuffed at the top corners and the kick line

## Details excluded
- No brand badge or sticker
- No full tool set (loose tools are their own models)

## Construction and placement notes
- Collision suggestion: Box 0.8 x 0.36 x 0.475 m on the body; handle, rag and open drawer are overhangs.
- Placement footprint: 0.8 x 0.35 m

## Outputs
- `models/survival/Claude_tool_chest/Claude_tool_chest.vox` (editable master)
- `models/survival/Claude_tool_chest/model.json`
- `models/survival/Claude_tool_chest/Claude_tool_chest.glb` (derived)
- `previews/survival/Claude_tool_chest/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b1_storage_tools.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
