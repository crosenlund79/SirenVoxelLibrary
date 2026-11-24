# Mailbox
- Asset ID: Claude_mailbox
- Base ID: mailbox
- Creator: Claude
- Category: decorations
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_D
- Scale family: full
- Intended uses: Yard prop (game mailbox) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A roadside mailbox on a post the mower has clipped too many times. Its red flag is still up for a letter nobody collected, and the box has filled with undelivered mail until the door no longer shuts.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.4 m
- Depth (Y): 0.55 m
- Height (Z): 1.3 m
- Grid: 8 x 11 x 26 cells at 0.05 m (detail tier), 340 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y faces the street or the person using it.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [4.0, 5.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`galv`, `galv_dark`, `galv_hi`, `grass`, `grass_hi`, `label_cream`, `paper`, `rust_deep`, `signal_red`, `signal_red_dark`, `steel_dark`, `steel_light`, `wgrey`, `wgrey_dark`, `wgrey_mid`, `wgrey_wet`

## Details included
- Galvanised tunnel-top box on a mounting board and a weathered 4x4 post
- Post leaning slightly toward the road verge (-X)
- Red flag raised on the +X side
- Door hanging open a crack with paper showing
- Rust run under the door, unmown grass around the foot of the post

## Details excluded
- No house number text
- No newspaper box

## Construction and placement notes
- Collision suggestion: Box 0.1 x 0.1 x 1.0 m (post) plus box 0.3 x 0.5 x 0.25 m on top.
- Placement footprint: 0.1 x 0.1 m

## Outputs
- `models/decorations/Claude_mailbox/Claude_mailbox.vox` (editable master)
- `models/decorations/Claude_mailbox/model.json`
- `models/decorations/Claude_mailbox/Claude_mailbox.glb` (derived)
- `previews/decorations/Claude_mailbox/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/d2_street.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
