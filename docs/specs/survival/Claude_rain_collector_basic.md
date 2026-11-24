# Basic Rain Collector
- Asset ID: Claude_rain_collector_basic
- Base ID: rain_collector_basic
- Creator: Claude
- Category: survival
- Status: Candidate (revision 1), awaiting user review
- Intended uses: outdoor water source beside a house or shed (e.g. Sirens Went Quiet); not authorization to integrate
- Brief approved by: user (shared brief `docs/PILOT_BATCH.md` §2, Claude batch commissioned 2026-11-23)

## Function and story
Built from what was lying around: a green plastic water butt on a stand of pallet boards and fence posts. One leg was cut short and levelled on a concrete block; a diagonal brace was added on the open side when the stand started to rack; a fresher post was bolted on at the back to carry the galvanised inlet pipe from the gutter; a canvas ratchet strap keeps the tank from blowing over. Improvised, but it works.

## Silhouette
- Primary: round tank (clean 16-cell circle) on a square timber stand.
- Functional reads: inlet pipe running in over the lid and dropping through a collar; brass tap with red lever overhanging the front edge; grey overflow running down the camera-facing side to a shoe at the ground.
- Asymmetry: concrete block under one leg, brace on one side, snapped deck board, back post taller than the rest.

## Dimensions and orientation
- Footprint: stand 1.00 × 0.90 m; overall 1.05 × 1.00 m including overflow (−X) and tap (+Y)
- Height (Z): 0.55 m deck, 1.45 m tank rim, **1.60 m** top of the inlet pipe
- Front direction: +Y = tap / service side
- Floor pivot: bottom centre of the timber stand footprint, `pivot_voxel` [11, 9, 0]
- Cell size: **0.05 m (detail tier)** — built first at the suggested 0.10 m and rejected (below).

### Resolution rationale
Built first at the suggested 0.10 m and reviewed: the 0.8 m tank is only 8 cells across, so its stair-stepped circle and lid broke into a lumpy block, and the tap, collar and brackets became stacked 10 cm cubes that read as a placeholder beside the rest of the batch (see `previews/batches/Claude_pilot_001_resolution_study.png`). At 0.05 m the tank is a clean pixel circle. The plumbing is kept deliberately chunky — the inlet pipe is 2 × 2 cells (10 cm) — so nothing is "too thin to render". 2,390 occupied voxels.

## Gutter connection
`model.json → attachments.gutter_inlet`: open rear end of the 10 cm inlet pipe at voxel [11, 0, 31], i.e. **0.00 m X, −0.45 m Y (back), 1.55 m up** from the floor pivot. A downpipe from the roof gutter connects here; no roof is modelled.

## Materials and colours
- Tank: `green` body, `green_dark` groove/base grime, `algae_dark` lowest band, `green_light` sun-faded crown, `green_dark` screw lid.
- Stand: silvered timber `wgrey`, `wgrey_hi`, `wgrey_mid`, `wgrey_warm`, `wgrey_dark`, `wgrey_deep`; `wgrey_wet` splash under the tap; the later post in fresher `pine_aged`.
- Metal: `galv` / `galv_hi` / `galv_dark` inlet pipe, collar and coupler; `brass` tap with `red` lever; `steel` buckle and clips.
- Other: `concrete` block, `concrete_hi` PVC overflow, `olive_dark` strap; `rust_dark` / `rust_deep` only at nails, buckle and bracket.

## Details included
1. Tank with tucked base, crisp rim, recessed moulded groove and screw lid.
2. Inlet pipe from the gutter with coupler, bracket on the post, elbow and collar into the lid.
3. Outlet tap overhanging the front edge (a can fits underneath).
4. Overflow from near the top, down the −X side to a shoe at the ground, clipped to the deck.
5. Stand: four posts, beams, rails, pallet deck, concrete-block leg, added brace, back post; ratchet strap.

## Details excluded
No water simulation or visible liquid, no magical container, no thin intricate plumbing, no roof/gutter mesh, no branding.

## Variant and state requirements
Default state only.

## Construction and placement notes
- Three posts and the concrete block stand on z = 0, plus the overflow shoe and the back post. Single 6-connected piece; the tank is a closed hollow shell.
- Place against a wall with the gutter above the −Y side; leave the +Y side open for the tap.
- Collision suggestion: cylinder r = 0.40 m, h = 1.45 m on a 1.0 × 0.9 × 0.55 m box.

## Required outputs
- `models/survival/Claude_rain_collector_basic/Claude_rain_collector_basic.vox`, `model.json`, `.glb`
- `previews/survival/Claude_rain_collector_basic/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/rain_collector_basic.py`

## Acceptance checks
- [x] Inlet and outlet positions visible; recognizable silhouette at thumbnail size
- [x] Believable outdoor scale next to the 1.75 m figure
- [x] One connected piece (tank rings are face-connected, not corner-touching)
- [x] Front +Y, floor pivot, ground contact verified; gutter attachment recorded
- [x] No unexplained voxel noise; 2,390 voxels
- [x] Source parses (own parser, py-vox-io, Goxel 0.11); previews rendered from it
- [ ] MagicaVoxel GUI open — unverified
- [ ] Godot import — unverified
- [ ] **User has reviewed and explicitly approved this revision**
