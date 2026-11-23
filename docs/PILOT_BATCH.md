# Pilot Batch 001 — Five Proposed Models
**Status: shared briefs, not yet generated.** This document alone does not authorize generation; a direct user instruction may commission one creator's batch. The two creators use these **same five briefs** but build independently under `GPT_` and `Claude_` names.

## Why these five?

These models test the library's visual rules across **furniture**, **functional survival devices**, **fire/metalwork**, **soft domestic objects**, and **organic vegetation**. Review them together, at the same physical scale, before producing a large catalog.

**Rival pair IDs:** for base `workbench_worn`, names are `GPT_workbench_worn` and `Claude_workbench_worn`; this same rule applies to all five. Their canonical VOX source filenames also carry the prefix. See `docs/RIVAL_WORKFLOW.md`.

All models use the standard library orientation: X right, +Y front, Z up; dimensions in metres; bottom-centre pivot unless noted. Dimensions are **starting targets**, not final commitments.

### 1. Workbench — `workbench_worn`
**Category:** furniture / workshop · **target size:** W 1.7 × D 0.7 × H 0.9 m · **suggested cells:** 0.1 m (standard).

- A rugged, believable modern home workshop table, not an ancient fantasy crafting altar.
- Broad worn pine top, dark steel or thick timber legs, cross brace, shallow tool shelf, a couple of recognizable unbranded tools.
- Slightly asymmetric: an uneven drawer front or scuff on one edge; stable silhouette, no unsupported floating tools.
- Optional hanging vice or clamp must read from the game camera and not force detail tier without good reason.
- **Test:** wood + metal material readability, function, compact interior placement.
- **Avoid:** overstuffing with miniature bolts, unreadable tool confetti, giant glowing crafting indicators.

### 2. Rain Collector — `rain_collector_basic`
**Category:** survival · **target footprint:** 1.0 × 1.0 m, H about 1.6 m · **suggested cells:** 0.1 m.

- Improvised but plausible domestic rainwater tank in a small timber support frame.
- Barrel/tank, practical inlet, outlet tap, overflow pipe and some brackets; roof gutter attachment may be indicated but does not need a separate roof mesh.
- Muted green/blue-gray container, aged wood or steel support, small rust points at joins.
- Make the inlet and outlet position visible. No assumed working plumbing simulation.
- **Test:** pipe legibility, coherent material contrast, outdoor placement and readable silhouette.
- **Avoid:** intricate plumbing too thin to render or a magical-looking liquid container.

### 3. Wood Stove — `wood_stove_compact`
**Category:** survival · **target size:** W 0.8 × D 0.65 × H 1.0 m for body; chimney connection documented separately · **suggested cells:** 0.1 m, detail tier only if essential.

- Compact freestanding cast-iron stove with hinged door, air vents, handles, short legs, flue outlet and simple firebox suggestion.
- Use distinct dark steel, worn edges, minimal warm ember accent *inside* the opening.
- Clearly indicate front orientation for interaction and attachment position for a later pipe.
- **Test:** legible functional details with low-saturation metal; recognizable front at 3/4 view.
- **Avoid:** bright glowing fantasy furnace; transparent shader requirements in the base version.

### 4. Single Bed — `single_bed_unmade`
**Category:** furniture · **target size:** W 1.05 × D 2.0 × H 0.75 m including headboard · **suggested cells:** 0.1 m.

- Modern, ordinary household bed, used and slightly unmade.
- Low bed frame, readable mattress, textured but *quiet* cream or slate-blue sheet, casually displaced blanket, one imperfect pillow.
- Proportions should work with a 1.75 m human reference. The bed should feel usable rather than miniature.
- Front (+Y) is the accessible foot of the bed; note this explicitly in metadata/spec.
- **Test:** cloth-versus-wood shape language, large quiet surfaces, believable scale.
- **Avoid:** noise-based blanket pattern, excessive pillow layers and toy-like thickness.

### 5. Dead Pine — `pine_dead_small`
**Category:** vegetation · **target size:** roughly 2.0–2.5 m canopy diameter, 4.5 m tall · **suggested cells:** 0.2 m (coarse).

- A dead or dying pine, asymmetrical and wind-shaped, with recognizable pine branching and several broken ends.
- Trunk slightly irregular, branches layered in purposeful masses, sparse desaturated needles if necessary.
- Should feel lonely and slightly unsettling by the fog boundary, without becoming a supernatural monster.
- Base must appear rooted. No geometric spiral or perfectly mirrored branches.
- **Test:** organic silhouette at coarse resolution; scene scale; manageable voxel count.
- **Avoid:** uniform Christmas-tree triangles, identical branch repetition, hundreds of single-cell twigs.

## Candidate review layout

For each model, show:
- hero 3/4 render, front and side;
- 1.75 m reference-person scale render;
- actual `.vox` source and `model.json`;
- dimensions, cell size, occupied voxel count, and any exported GLB validation results.

Make one **five-model contact sheet per creator**, named `GPT_pilot_001.png` and `Claude_pilot_001.png` respectively, using consistent camera and lighting, with each object's name and scale. When both sets exist, optionally make a labeled side-by-side sheet with the same render settings. Use separate framing for the 4.5 m pine so it stays legible.

## Success threshold before expanding

Do not proceed from 5 to 50 models merely because generation worked. Evaluate the group for:
1. A coherent visual family across all categories.
2. Readable forms at the approximate Sirens Went Quiet camera angle.
3. Sensible voxel resolution/complexity per object.
4. Real editable source and reproducible previews.
5. At least one successful **independent** game import/conversion pilot, but only after the user separately approves integration.

If the art is promising but not cohesive, adjust the art bible and regenerate only the weak models. The user has final approval authority.
