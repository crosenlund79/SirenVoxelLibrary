# Window Frame
- Asset ID: Claude_window_frame
- Base ID: window_frame
- Creator: Claude
- Category: construction
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Window opening module (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A six-over-six sash window salvaged whole, frame and all, from a house that burned. One cracked pane was replaced with cardboard and tape; the sill paint has weathered through where rain sat on it.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.0 m
- Depth (Y): 0.25 m
- Height (Z): 1.2 m
- Grid: 20 x 5 x 24 cells at 0.05 m (detail tier), 1,118 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the outside face; the module fills its full span.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [10.0, 2.5, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`card`, `card_dark`, `card_hi`, `cream`, `cream_mid`, `cream_shadow`, `glass`, `glass_dark`, `label_cream`, `wgrey_hi`

## Details included
- Painted frame and head, sill projecting 5 cm beyond the outside face
- Upper sash outside, lower sash inside (offset one cell), meeting rails overlap
- Sash bars dividing each sash into 3 x 2 lites, glass set back behind the bars
- One lower lite replaced with taped cardboard
- Weathered sill and lower rail

## Details excluded
- Glass is opaque (glass palette roles)
- No curtains

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.0 x 0.25 m

## Outputs
- `models/construction/Claude_window_frame/Claude_window_frame.vox` (editable master)
- `models/construction/Claude_window_frame/model.json`
- `models/construction/Claude_window_frame/Claude_window_frame.glb` (derived)
- `previews/construction/Claude_window_frame/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b3_construction.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
