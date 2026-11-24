# Three-Seat Sofa
- Asset ID: Claude_sofa
- Base ID: sofa
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Living-room furniture; cover; game prop 'sofa' (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A slate-blue three-seater from a family living room. The middle cushion has sagged from years of the same person sitting there, the right cushion was pulled forward and never pushed back, and a mustard throw still lies folded over the left arm.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 2.3 m
- Depth (Y): 1.0 m
- Height (Z): 0.85 m
- Grid: 46 x 20 x 17 cells at 0.05 m (detail tier), 3,733 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [np.float64(23.5), np.float64(10.0), 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`mustard`, `mustard_dark`, `mustard_deep`, `slate`, `slate_dark`, `slate_deep`, `slate_hi`, `wood_stain`

## Details included
- Three seat and three back cushions with seams
- Rolled arms with hand-rubbed fronts
- Low dark wooden feet
- Folded knitted throw draped over the left arm

## Details excluded
- No pattern noise in the fabric
- No scatter cushions pile

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 2.25 x 0.9 m

## Outputs
- `models/furniture/Claude_sofa/Claude_sofa.vox` (editable master)
- `models/furniture/Claude_sofa/model.json`
- `models/furniture/Claude_sofa/Claude_sofa.glb` (derived)
- `previews/furniture/Claude_sofa/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a1_living.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
