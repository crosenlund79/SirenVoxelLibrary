# Rock
- Asset ID: Claude_rock
- Base ID: rock
- Creator: Claude
- Category: vegetation
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_D
- Scale family: full
- Intended uses: Ground dressing (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A lump of granite turned up when the estate was built and left at the edge of a verge as a marker. Decades of weather have rounded its edges and lichen has taken the top; an old frost split left one flat face.

Condition: **n/a**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.75 m
- Depth (Y): 0.5 m
- Height (Z): 0.45 m
- Grid: 15 x 10 x 9 cells at 0.05 m (detail tier), 472 occupied voxels
- Front direction: +Y (library voxel)
- Front: No functional front; character details face the default camera (-X/+Y).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [7.5, 5.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`concrete`, `concrete_hi`, `gravel`, `lichen`, `moss`, `moss_dark`, `stone`, `stone_dark`

## Details included
- Two overlapping rounded masses, broad at the foot
- One flat fracture face on the camera side, paler than the weathered skin
- Coherent lichen patch on the crown, moss on the damp north (-Y) foot

## Details excluded
- No granite speckle (confetti)

## Construction and placement notes
- Collision suggestion: Box 0.7 x 0.55 x 0.44 m.
- Placement footprint: 0.75 x 0.5 m

## Outputs
- `models/vegetation/Claude_rock/Claude_rock.vox` (editable master)
- `models/vegetation/Claude_rock/model.json`
- `models/vegetation/Claude_rock/Claude_rock.glb` (derived)
- `previews/vegetation/Claude_rock/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/d1_vegetation.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
