# Unmade Single Bed
- Asset ID: Claude_single_bed_unmade
- Base ID: single_bed_unmade
- Creator: Claude
- Category: furniture
- Status: Candidate (revision 1), awaiting user review
- Intended uses: bedrooms, shelters (e.g. Sirens Went Quiet); not authorization to integrate
- Brief approved by: user (shared brief `docs/PILOT_BATCH.md` §4, Claude batch commissioned 2026-11-23)

## Function and story
An ordinary single bed, slept in and left in a hurry. The slate-blue duvet has been thrown back toward the foot — a soft rolled fold, the turned-over flap with its hem — and it is sliding off the near side in a long, uneven drape and tumbling over the low foot rail. The pillow is lopsided, stuffing pushed to one end with the hollow of a head beside it. A paperback lies face-down on the sheet. Comfortable, imperfect, recently abandoned.

## Silhouette
- Primary: low dark-stained frame, 20 cm mattress, slatted headboard rising at the back.
- Secondary: rolled duvet fold crossing the bed on a slight diagonal; long side drape; foot overhang; pillow.
- Asymmetry: drape on one side only, short tuck on the other; pillow off-centre and lopsided; uneven hems.
- The drape faces −X, toward the default three-quarter game camera.

## Dimensions and orientation
- Width (X): 1.05 m frame (1.10 m including the duvet drape)
- Depth (Y): 2.00 m
- Height (Z): 0.45 m sleeping surface, 0.75 m headboard posts
- **Front direction: +Y = the FOOT of the bed (the accessible end).** The headboard is at −Y.
- Floor pivot: bottom centre of the 1.05 × 2.00 m frame footprint, `pivot_voxel` [11.5, 20, 0]
- Cell size: **0.05 m (detail tier)** — rationale below.

### Resolution rationale
The brief explicitly says "avoid toy-like thickness". At 0.10 m the thinnest possible duvet is 10 cm, the pillow is a single 10 cm slab, and the headboard slats and rails double in thickness — the cloth-versus-wood test fails. At 0.05 m the duvet is a believable 5 cm layer that can fold, roll and drape, and the frame members are close to real. The mattress is a closed hollow shell (no invisible fill), giving 3,716 occupied voxels.

## Materials and colours
- Frame: `wood_stain` posts, rails, slats; `pine_dark` rubbed caps and top rail; `wood_deep` cleats and feet.
- Bedding: `cream` sheet top, `cream_mid` sheet sides and pillow base, `cream_hi` pillow, `cream_deep` mattress ticking.
- Duvet: `blue` top, `blue_mid` folds and drape, `blue_hi` crest of the roll, `blue_dark` fold valleys, `blue_seam` hems.
- Small accent: `ochre_dark` paperback with `paper` page edge and `wood_stain` spine.

## Details included
1. Frame: corner posts, side and foot rails, low footboard, slatted headboard with a hand-worn patch, hidden slats under the mattress (construction logic).
2. Mattress with fitted sheet wrapping the sides.
3. Duvet: rolled fold, turned-over flap with hem, side drape with fold valleys and uneven hem, overhang across the foot, short tuck on the far side.
4. One lopsided pillow with a head hollow and a flattened corner.
5. Face-down paperback.

## Details excluded
No noise-based blanket pattern, no extra pillows or throws, no toy-thick bedding, no patterned prints, no under-bed clutter.

## Variant and state requirements
Default "unmade" state only. A made-bed variant would be a separate proposal.

## Construction and placement notes
- Four legs on z = 0; the drape hangs to 5 cm above the floor (it never pierces the ground plane). Single 6-connected piece.
- Headboard side (−Y) goes against a wall; leave the −X side open to show the drape, or rotate the asset.
- Collision suggestion: box 1.05 × 2.00 × 0.50 m plus a thin box for the headboard.

## Required outputs
- `models/furniture/Claude_single_bed_unmade/Claude_single_bed_unmade.vox`, `model.json`, `.glb`
- `previews/furniture/Claude_single_bed_unmade/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/single_bed_unmade.py`

## Acceptance checks
- [x] Recognizable silhouette at thumbnail size
- [x] Usable, not miniature, next to the 1.75 m figure
- [x] One connected piece; nothing floats
- [x] Front (+Y = foot) documented; floor pivot and ground contact verified
- [x] Quiet large surfaces; no noise patterns; 3,716 voxels
- [x] Source parses (own parser, py-vox-io, Goxel 0.11); previews rendered from it
- [ ] MagicaVoxel GUI open — unverified
- [ ] Godot import — unverified
- [ ] **User has reviewed and explicitly approved this revision**
