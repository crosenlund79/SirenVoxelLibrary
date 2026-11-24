# Worn Workbench
- Asset ID: Claude_workbench_worn
- Base ID: workbench_worn
- Creator: Claude
- Category: furniture
- Status: Candidate (revision 1), awaiting user review
- Intended uses: garage / shed / workshop interiors (e.g. Sirens Went Quiet); not authorization to integrate
- Brief approved by: user (shared brief `docs/PILOT_BATCH.md` §1, Claude batch commissioned 2026-11-23)

## Function and story
A home-built garage bench, made from construction pine years ago and used ever since. The front edge of the top is polished pale where forearms rest; there is a grimy work zone beside the vise; a drawer has dropped on a broken runner and is left half open; a mug was forgotten at the back; the saw hangs where it always hangs; the shelf has become storage (toolbox, a tin of olive paint, offcuts too good to throw away).

## Silhouette
- Primary: broad 10 cm laminated top on four 10 × 10 cm legs with a low shelf; overhang shadow line between top and apron.
- Secondary (break the box): painted cast-iron vise overhanging the front-left corner (user's right hand), hand saw hanging on the left end, an offcut poking out past the right end of the shelf, low back-stop board.
- Asymmetry: off-centre T-handle on the vise, sagging drawer, chipped front edge, offcut overhang.
- Must read at thumbnail: top + legs + shelf, vise, red toolbox.

## Dimensions and orientation
- Width (X): 1.70 m body (1.80 m including offcut overhang)
- Depth (Y): 0.70 m body (0.90 m including vise)
- Height (Z): 0.90 m working surface (1.10 m to the top of the vise)
- Front direction: +Y (library voxel) = working side
- Floor pivot: bottom centre of the 1.70 × 0.70 m body footprint, `pivot_voxel` [17, 7, 0]
- Cell size: **0.05 m (detail tier)** — see rationale below.

### Resolution rationale
The brief suggests 0.10 m. A 0.10 m block-out read as a toy: the top, shelf, apron and drawer front all became 10 cm slabs (2–4× real timber), the vise was a single block and the brief's "couple of recognizable tools" collapsed into single cubes. At 0.05 m the members match real construction timber (10 cm top, 10 × 10 cm legs, 5 cm shelf boards) and the vise jaws, T-handle, saw, hammer and drawer read at the three-quarter camera. 2,439 occupied voxels — a quarter of the 10k furniture budget.

## Materials and colours
Shared Claude pilot palette (`tools/claude/voxkit.py`).
- Top: `pine_light` / `pine_mid` planks, `pine_hi` forearm-polished front arris, `pine_aged` end grain and lower lamination.
- Frame: `pine_dark` legs, aprons and rails; `wood_stain` grime at the feet and on the back/brace.
- Vise: `bluegrey` paint, `steel_light` jaw plates, `steel_hi` handle, `charcoal` base, chipped `steel_dark`, one `rust_dark` spot.
- Accents: `red` toolbox (`red_hi` lid, `red_dark` seam), `olive` paint tin, `cream` enamel mug with `blue_dark` rim, `sawdust` hammer handle.

## Details included (descending importance)
1. Thick plank top with overhang, 10 × 10 cm legs, aprons, low shelf on rails, back diagonal brace.
2. Bench vise with jaw gap, slide, screw boss and slid-over T-handle, bolted to the top.
3. Hand saw with D-handle hanging from a nail on the left-end apron.
4. Drawer pulled out 10 cm and sagging 5 cm on one side, with a steel pull.
5. Claw hammer and enamel mug on the top; toolbox, paint tin and offcuts on the shelf.
6. Wear: polished front edge, grime zone beside the vise, two chips knocked out of the front edge, rubbed leg corners, paint drip on the tin.

## Details excluded
No logos or labels; no bolts/screws smaller than a cell; no scattered tool confetti; no glowing crafting indicators; no random speckle (wear is localized to where hands and feet would make it).

## Variant and state requirements
Default state only. No damage variants.

## Construction and placement notes
- Stands on four legs at z = 0; everything else is supported (single 6-connected piece).
- Wall-placeable: the back (−Y) is flat apart from the back-stop board.
- Collision suggestion: box 1.70 × 0.70 × 0.90 m at the pivot, optional small box for the vise.

## Required outputs
- `models/furniture/Claude_workbench_worn/Claude_workbench_worn.vox` (editable source)
- `models/furniture/Claude_workbench_worn/model.json`
- `models/furniture/Claude_workbench_worn/Claude_workbench_worn.glb` (derived)
- `previews/furniture/Claude_workbench_worn/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/workbench_worn.py`

## Acceptance checks
- [x] Recognizable silhouette at thumbnail size (contact sheet `previews/batches/Claude_pilot_001.png`)
- [x] Physically believable scale next to the 1.75 m figure (`scale.png`)
- [x] Geometry is one connected piece; nothing floats
- [x] Front +Y, floor pivot, ground contact verified by `tools/claude/validate.py`
- [x] No unexplained voxel noise; 2,439 voxels
- [x] Source parses (own parser, py-vox-io, Goxel 0.11) and previews are rendered from it
- [x] Preview images are actual renders of the voxel source
- [ ] MagicaVoxel GUI open — unverified (not available in the build environment)
- [ ] Godot import — unverified (not available in the build environment)
- [ ] **User has reviewed and explicitly approved this revision**
