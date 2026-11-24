# Small Dead Pine
- Asset ID: Claude_pine_dead_small
- Base ID: pine_dead_small
- Creator: Claude
- Category: vegetation
- Status: Candidate (revision 1), awaiting user review
- Intended uses: clearing edges, fog boundaries, roadside (e.g. Sirens Went Quiet); not authorization to integrate
- Brief approved by: user (shared brief `docs/PILOT_BATCH.md` §5, Claude batch commissioned 2026-11-23)

## Function and story
A young pine that died standing at the edge of a clearing. It leans away from the prevailing wind with an old kink in the trunk; the leader snapped near 4 m and a branch just below the break has turned skyward as a crooked new top. The lowest whorls are broken stubs, the windward side is stripped short, the lee side still carries the longest drooping limbs and a few clinging tufts of rust-brown needles, and the bark has sloughed off the windward face in a pale strip. Lonely and slightly wrong, not monstrous.

## Silhouette
- Pine logic: branches in whorls (a ring every ~0.4 m), near-horizontal limbs drooping at the tip, length decreasing upward.
- Wind shaping: long limbs on the lee (+X) side, snapped stubs on the windward (−X) side.
- Character beats: drooping dead lower limb toward the camera, snapped pale top beside the turned-up leader, root flares gripping the ground.
- Every limb is hand-placed in a whorl table (no random generator, no spirals, no mirrored branches).

## Dimensions and orientation
- Crown: 2.20 m (X) × 1.90 m (Y)
- Height (Z): 4.40 m
- Front direction: vegetation has no functional front; character details are arranged toward the default camera (−X / +Y).
- Floor pivot: **trunk base centre** at ground level, `pivot_voxel` [7, 10, 0] (not the bounding-box centre — the crown leans toward +X).
- Cell size: **0.10 m (standard tier)** — rationale below.

### Resolution rationale
The tree is designed in metres and voxelised at a chosen cell size, so the same design was compared at 0.20, 0.10 and 0.05 m (`previews/batches/Claude_pilot_001_resolution_study.png`).
- **0.20 m (suggested):** 165 voxels; every branch is as thick as the trunk and the tree becomes a blobby column with no pine branching — fails the silhouette test.
- **0.05 m:** more delicate, but it becomes many single-cell twigs (which the brief warns against and which would shimmer at distance).
- **0.10 m (chosen):** the coarsest tier that keeps whorled pine branching, broken ends and the snapped leader readable (trunk 2 cells, limbs 1 cell). 400 occupied voxels.

The 0.05 m version would match the voxel rhythm of the other four candidates. Because the design is metric, it is a one-parameter rebuild (`build(cell=0.05)`) if preferred.

## Materials and colours
- Bark: `bark_dark` (base), `bark_mid`, `bark`, `bark_hi`; `bark_deep` roots; `lichen` on the shaded −Y face of the lower trunk.
- Dead wood: `snag` stripped windward strip and low broken stubs, `snag_light` bleached top, `break_fresh` snapped leader end.
- Needles (sparse, desaturated): `needle_rust`, `needle_dry`, one `needle_olive` tuft on the new leader; `needle_dark` undersides.

## Details included
1. Leaning, tapering trunk with an old kink and root flares.
2. Eight hand-placed whorls: stubs low, longest limbs mid-height on the lee side, short limbs at the top.
3. Snapped leader with a crooked replacement top.
4. A long dead lower limb drooping toward the viewer.
5. Seven clinging needle tufts plus one on the new leader; a side twig or two on long limbs only.

## Details excluded
No uniform Christmas-tree cone, no identical branch repetition, no mirrored or spiral layout, no hundreds of single-cell twigs, no soil mound (so it sits on any terrain), no glowing or monstrous features.

## Variant and state requirements
Default state only.

## Construction and placement notes
- Roots and trunk base on z = 0; single 6-connected piece.
- Collision suggestion: capsule r = 0.12 m, h = 4.4 m at the pivot (trunk only); branches non-colliding.

## Required outputs
- `models/vegetation/Claude_pine_dead_small/Claude_pine_dead_small.vox`, `model.json`, `.glb`
- `previews/vegetation/Claude_pine_dead_small/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/pine_dead_small.py`

## Acceptance checks
- [x] Reads as a dead pine from the three-quarter camera; organic, asymmetric silhouette
- [x] Scene scale verified next to the 1.75 m figure
- [x] One connected piece, rooted at z = 0
- [x] Trunk-base pivot documented and verified
- [x] Manageable count: 400 voxels
- [x] Source parses (own parser, py-vox-io, Goxel 0.11); previews rendered from it
- [ ] MagicaVoxel GUI open — unverified
- [ ] Godot import — unverified
- [ ] **User has reviewed and explicitly approved this revision**
