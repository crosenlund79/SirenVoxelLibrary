# Compact Wood Stove
- Asset ID: Claude_wood_stove_compact
- Base ID: wood_stove_compact
- Creator: Claude
- Category: survival
- Status: Candidate (revision 1), awaiting user review
- Intended uses: heating / cooking point in cabins and houses (e.g. Sirens Went Quiet); not authorization to integrate
- Brief approved by: user (shared brief `docs/PILOT_BATCH.md` §3, Claude batch commissioned 2026-11-23)

## Function and story
A squat cast-iron box stove in daily use. The round cooking lid is polished by pots, the iron above the door has heat-bronzed and carries a soot streak, a low bed of embers glows behind smoked glass, and damp has raised rust only where the feet meet a cold floor. Heavy, useful, not decorative.

## Silhouette
- Primary: box body inset between an overhanging plinth plate and top plate (5 cm lips give the classic cast-stove profile and strong shadow lines), on four short splayed feet.
- Functional reads at three-quarter view: raised door with window and ember glow, coil-spring latch handle, hinge knuckles, ash-pan slider slots, raised cooking lid, flanged flue socket.
- Sides: recessed cast panels so the stove does not collapse into one dark mass.

## Dimensions and orientation
- Width (X): 0.80 m (plates)
- Depth (Y): 0.65 m plates; 0.75 m including latch handle and slider lever
- Height (Z): 0.85 m top plate, 0.90 m cooking lid, **1.00 m** top of flue collar
- Front direction: +Y (library voxel) = loading door / interaction side
- Floor pivot: bottom centre of the 0.80 × 0.65 m plate footprint, `pivot_voxel` [8, 6.5, 0]
- Cell size: **0.05 m (detail tier)** — the brief allows detail tier "only if essential"; rationale below.

### Resolution rationale
Every functional feature the brief lists is 2–5 cm in reality: hinge knuckles, latch handle, air-slider slots, 15 cm feet and the plate lips that define a cast stove's silhouette. At 0.10 m the 0.8 m body is only 8 cells wide and each feature becomes a whole 10 cm cube — a generic furnace block. The firebox is a genuine hollow cavity (visible through the flue collar), so the stove is 1,263 occupied voxels.

## Chimney connection (documented separately, as requested)
`model.json → attachments.flue_outlet`: centre of the open top of the 15 cm collar at voxel [8, 3, 20], i.e. **0.00 m X, −0.175 m Y (toward the back), 1.00 m up** from the floor pivot. A vertical 15 cm pipe attaches here. The collar is set toward the rear so the cooking lid stays usable.

## Materials and colours
- Cast iron: `iron` body, `iron_edge` catch-light on plate edges, door edge and collar rim, `iron_dark` panel recesses and feet, `iron_deep` lid notch, `iron_warm` heat-bronzed band, `soot` streak, throat and window top.
- Hardware: `steel_hi` coil-spring handle, `steel_dark` hinge knuckles and flange bolts, `steel` slider lever.
- Fire (the only warm accent, inside the window): `ember_dark`, `ember`, one `ember_hot`, `coal`.
- Damp: `rust_deep` at the feet and plinth edge only.

## Details included
1. Plinth / top plates overhanging a box body; chamfered plate corners; splayed feet.
2. Raised door with smoked, opaque window and a low ember bed; hinge knuckles; coil-spring latch.
3. Ash-pan door with two air slots and a slider lever.
4. Raised round cooking lid with lift notch; recessed cast side panels.
5. Flue socket for a 15 cm pipe: square flange with four bolt heads, rounded hollow socket above it, opening into a hollow firebox.

## Details excluded
No bright glowing furnace, no flames above the ember bed, no transparency requirement (glass is opaque by design), no logos or ornate casting, no kettle or props baked onto the stove.

## Variant and state requirements
Default "lit, low fire" state only. An unlit variant (embers → `ash`/`coal`) is a trivial palette change if requested.

## Construction and placement notes
- Stands on four feet at z = 0; single 6-connected piece; hollow firebox.
- Leave clearance to walls in-game; chimney pipe attaches at `flue_outlet`.
- Collision suggestion: box 0.80 × 0.65 × 0.90 m at the pivot plus a 0.2 m cylinder for the collar.

## Required outputs
- `models/survival/Claude_wood_stove_compact/Claude_wood_stove_compact.vox`, `model.json`, `.glb`
- `previews/survival/Claude_wood_stove_compact/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/wood_stove_compact.py`

## Acceptance checks
- [x] Recognizable silhouette and front at three-quarter view and thumbnail size
- [x] Physically believable scale next to the 1.75 m figure
- [x] One connected piece; nothing floats
- [x] Front +Y, floor pivot, ground contact, flue attachment recorded
- [x] No unexplained voxel noise; 1,263 voxels
- [x] Source parses (own parser, py-vox-io, Goxel 0.11); previews rendered from it
- [ ] MagicaVoxel GUI open — unverified
- [ ] Godot import — unverified
- [ ] **User has reviewed and explicitly approved this revision**
