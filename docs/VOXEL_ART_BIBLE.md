# SirenVoxelLibrary — Voxel Art Bible
**Version 1.0 · Draft foundation · 2026-11-23**

This is the shared visual standard for a curated library of real editable voxel objects. Its first use case is **Sirens Went Quiet**, but it must remain usable in other games. It is a creative and technical *guide*, not permission to generate unrequested models.

## 1. Artistic thesis

**Everyday objects at the edge of abandonment.** A believable modern world, slightly exaggerated for clarity, warm human traces amid cold silence.

- **Hand-made, not sterile:** subtly imperfect silhouettes, sensible asymmetry, meaningful wear, occasional personal detail. Not random damage or noise.
- **Readable at play distance:** recognizable outline before the viewer notices texture, seams or labels. Important gameplay features should remain visible in a small isometric view.
- **Stylized rather than photorealistic:** softened proportions, controlled blockiness, surfaces organized into deliberate masses. Do not chase photorealistic detail or tiny pixel noise.
- **Quiet horror, not fantasy:** contemporary domestic and practical objects, believable materials, modest unsettling atmosphere. Avoid glowing magical effects, sci-fi ornamentation and whimsical toy proportions unless separately requested.
- **Cohesive, not identical:** objects differ in age, material and condition while sharing value range, proportions, voxel rhythm and level of detail.

**Design test:** Could five different objects sit in the same small suburban house without looking like assets from five different packs?

## 2. Voxel style rules

1. Start from the **silhouette**. Block the main volume, then secondary shapes, then useful details. Decorative detail must not obscure the function.
2. Use **large readable masses** over countless single-cell details. A feature thinner than a voxel cannot be expressed reliably; simplify or switch resolution deliberately.
3. Support **intentional asymmetry**: a loose drawer, worn corner, slightly crooked pipe, collapsed branch. Do not distort function or create accidental floating pieces.
4. Show **construction logic**: tabletop has legs or brackets; stove has a door and chimney outlet; water tank has believable supports and a drain.
5. Wear is **localized** where objects would be touched or exposed. No uniform confetti of differently colored voxels across every surface.
6. Silhouette, material, lighting and modest wear should sell the model even **without** decals or elaborate shaders.
7. No generic white/gray block placeholders as deliverables. Functional and good-looking from first review.
8. Avoid recognizable trademarks, copied game art or third-party asset designs. Use original shapes and unbranded details.
9. Objects intended to be stationary must touch their support plane. No accidental disconnected voxels; separately floating pieces need a documented reason.
10. Keep axis orientation, dimensions and pivot consistent across models, even if individual generation tools use other conventions.

## 3. Scale and coordinate contract

**Real-world scale** is mandatory. Store dimensions in **metres**, not arbitrary scene units. In Godot, 1 world unit = 1 metre.

- Library voxel source convention: **X = right, Y = front, Z = up**.
- A model's **front** is +Y in library voxel coordinates.
- Conversion to Godot (Y-up, front -Z): source voxel (X,Y,Z) becomes Godot (X,Z,-Y), after cell-size conversion and pivot offset.
- The **ground pivot** is the horizontal centre of the intended footprint at the object's bottom support plane, unless the spec explicitly requests a wall/ceiling attachment pivot.
- Native `.vox` tools may not preserve a logical pivot. Record the source-space pivot in metadata and apply it in the exporter; never assume it is present in the file.
- Models should stand on Z=0 with no hidden underground offset. In metadata, dimensions and pivot must describe actual occupancy, not just an arbitrary canvas.
- Review proportions against a **1.75 m reference person**, not only as an isolated rendered object.

This coordinate mapping is the **library contract**, not a guarantee about the axis conventions used by third-party import tools. Verify every exporter once with an asymmetric orientation test model.

## 4. Resolution: deliberately variable

**Do not force all assets onto the Sirens Went Quiet runtime's 0.1 m grid.** Library models may have their own voxel size and be imported as static 3D meshes. Whether an object becomes part of the runtime destructible grid is a separate decision.

| Resolution tier | Typical cell size | Suitable use |
|---|---:|---|
| **Coarse** | 0.20 m | Large trees, big outdoor silhouettes, bulky structures, background objects |
| **Standard** | 0.10 m | Normal furniture, workshop equipment, household appliances, most props |
| **Detail** | 0.05 m | Small focal props or a model whose silhouette demonstrably needs finer features |

Choose **the coarsest tier that preserves the object's silhouette and function**. Detail tier is opt-in and must be justified in `model.json`; do not upscale everything for cosmetic texture. Components with distinct resolution tiers should normally be separate models, not a single untracked mixed grid. Never imply that reducing voxel count automatically produces proportional GPU savings.

Suggested *initial* budget, subject to visual review: aim for fewer than ~10,000 occupied voxels on normal furniture and ~20,000 on featured objects. These are guidelines, not renderer guarantees; record the actual count. Avoid very large voxel domains containing mostly empty space.

## 5. Materials, color, and value

Use restrained, readable colors. The palette below is a **starting family of anchor colors**, not a mandate that every object use every swatch:

| Material / role | Anchor sRGB hex |
|---|---|
| Near-black shadow | `#252A2B` |
| Deep charcoal metal | `#363C3D` |
| Worn steel | `#687072` |
| Pale metal highlight | `#ADB4B2` |
| Weathered concrete | `#90918A` |
| Warm plaster | `#CCC5B6` |
| Warm pale wood | `#BC9670` |
| Aged pine | `#967455` |
| Dark stained wood | `#5E4839` |
| Muted forest green | `#566C60` |
| Olive canvas | `#777B55` |
| Dusty brick red | `#9A594B` |
| Rust / orange accent | `#B36E44` |
| Cold blue-gray | `#687A82` |
| Soft cream fabric | `#D7CDB9` |
| Desaturated blue fabric | `#697D8B` |

**Material rules:**
- Differentiate wood, painted metal, concrete, glass and cloth through value blocks, joins, grain direction and silhouette—not pure hue alone.
- Most of an object's surface should remain relatively quiet; reserve contrast for edges, openings, functional controls and important damage.
- Use distinct light/mid/shadow variants of major materials, not arbitrary one-voxel dithering everywhere.
- Prefer a shared palette family with small per-object variation; strong high-saturation accents should be rare and purposeful.
- Avoid painting baked dramatic directional lighting into every face; use restrained local occlusion, leaving the Godot renderer free to light the asset.
- Transparency/glass in `.vox` and exported `.glb` may behave differently. Use an explicit separate material or opaque stylization if transparency cannot be reliably exported.

Record material names or palette role mappings in the per-model metadata. A separate palette file can be introduced once the pilot proves the colors; do not invent a complex universal material engine yet.

## 6. Shapes by category

**Furniture:** familiar proportions first; comfortable, slightly worn rather than cartoonishly oversized. Legs, cushions, handles and shelves should remain recognizable at medium zoom. Mostly static 3D assets.

**Survival and workshop equipment:** prioritize function: support structures, pipes, valves, handles, burners, shelves and working clearance. Add wear where heat, water and hands would create it.

**Vegetation:** organic branch masses and asymmetric growth; avoid perfectly repetitive spirals. Dead trees should still read as a tree from the game camera. Prefer coarse resolution for large silhouettes.

**Vehicles:** preserve distinctive vehicle body masses, recognizable wheels and windows; save fine detail for intentional focal areas. Avoid logos.

**Architectural parts:** favor agreed construction dimensions, surface alignment, robust snapping and clear distinction between visual detail and game collision. Structural gameplay voxels are governed by the receiving game's rules.

**Character-scale props:** align grips, seats, doors and work surfaces to believable human proportions, then exaggerate sparingly for readability.

## 7. Game-readability and review angles

At minimum review each candidate in:
1. Three-quarter/isometric hero view.
2. Front and side orthographic views.
3. A small-scale scene with the 1.75 m figure and at least one other approved or candidate asset.

Prefer **1600×900** group/contact-sheet previews and **transparent or neutral backgrounds** for asset hero thumbnails; the exact thumbnail framing can adapt to tall trees versus compact furniture. Keep light direction and camera elevation consistent within a batch.

Ask: Is it recognizable at thumbnail size? Is the upper silhouette useful in an overhead/three-quarter game camera? Are all dark pieces collapsing into one mass? Does it sit squarely on the floor? Is the voxel density visually appropriate?

## 8. Relationship to Sirens Went Quiet

**Voxel art is not automatically destructive.** Static models may be exported as optimized conventional meshes and be movable, placeable or destroyable through ordinary game-object state. Only structures or selected props requiring per-cell destruction need conversion into the game's custom voxel grid.

- Model source should be independent of Godot scene logic.
- Keep real-world dimensions and attachment points in metadata.
- The game decides collision simplification, damage behavior, placement grid, and material gameplay properties.
- A `.glb` alone does not carry editable voxels or integrate with the custom voxel engine.
- No automatic import into the game repository. The user explicitly selects the models and their use.

## 9. Visual anti-patterns

Reject or revise: random voxel noise; gray cubes without purpose; inconsistent furniture sizes; voxel counts inflated for invisible interior fill; unsupported floating details; tiny features invisible at game zoom; baked-overly-bright outlines; mirrored-perfect dead vegetation; branding/copyrighted silhouettes; untested exports; screenshots without actual source files.

**Success:** a model looks good, belongs to the same world as the others, remains editable, and arrives with enough metadata that another project can use it correctly.
