# Laundry Basket
- Asset ID: Claude_laundry_basket
- Base ID: laundry_basket
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Utility dressing (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The family's laundry basket, still holding the last unwashed load: jeans, a towel, a mauve shirt with one sleeve flopped over the rim, and the other mustard sock from the pair caught in the washer.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.55 m
- Depth (Y): 0.5 m
- Height (Z): 0.5 m
- Grid: 11 x 10 x 10 cells at 0.05 m (detail tier), 522 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [5.5, 4.5, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`bottle`, `bottle_hi`, `cream`, `cream_hi`, `cream_mid`, `cream_shadow`, `denim`, `denim_dark`, `mauve`, `mauve_dark`, `mauve_hi`, `mustard`

## Details included
- Pale blue perforated plastic basket, slightly tapered, with hand-hole grips
- Clothes heaped over the rim in a few large garment masses
- One sleeve hanging over the front rim; the stray mustard sock on top

## Details excluded
- No pattern prints on the clothes

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.55 x 0.45 m

## Outputs
- `models/furniture/Claude_laundry_basket/Claude_laundry_basket.vox` (editable master)
- `models/furniture/Claude_laundry_basket/model.json`
- `models/furniture/Claude_laundry_basket/Claude_laundry_basket.glb` (derived)
- `previews/furniture/Claude_laundry_basket/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a4_bath_utility.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
