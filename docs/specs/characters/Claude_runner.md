# Runner
- Asset ID: Claude_runner
- Base ID: runner
- Creator: Claude
- Category: characters
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_F
- Scale family: full
- Intended uses: Enemy archetype: fast, fragile (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
Out on a morning run when the sirens stopped, and still running in a way: the same light kit, torn now, worn for weeks. Lean to the point of gauntness, always tipped forward as if the next step has already started.

Condition: **n/a**.

## Silhouette
The leanest, most forward-tilted figure of the set: narrow shoulders, stick-thin limbs and a long stride-ready stance.

## Dimensions and orientation
- Width (X): 0.55 m
- Depth (Y): 0.6 m
- Height (Z): 1.75 m
- Grid: 11 x 12 x 35 cells at 0.05 m (detail tier), 594 occupied voxels
- Front direction: +Y (library voxel)
- Front: The character faces +Y in a neutral standing display pose.
- Pivot: Between the feet at ground level. (pivot_voxel [np.float64(5.5), np.float64(6.0), 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`charcoal`, `hair_black`, `navy`, `navy_dark`, `paint_white_shadow`, `porcelain_deep`, `porcelain_mid`, `skin1_shadow`, `skin2`, `skin2_shadow`

## Details included
- Whole body tipped forward from the ankles; head low and ahead of the chest
- Staggered stance: left foot forward, right heel lifted behind
- Thin bare arms bent slightly at the elbow, hands loosely closed
- Faded running tee with a ragged hem, the left sleeve torn away and a rip at the side
- Dark running shorts with a frayed leg
- Worn pale running shoes
- Close-cropped dark hair, gaunt face

## Details excluded
- No gore
- No weapon
- No logos or stripes on the shoes or kit

## Construction and placement notes
- Collision suggestion: Upright capsule about 0.3 m in radius and dimensions_m[2] tall, centred on the pivot; static reference figure, no rig.

## Outputs
- `models/characters/Claude_runner/Claude_runner.vox` (editable master)
- `models/characters/Claude_runner/model.json`
- `models/characters/Claude_runner/Claude_runner.glb` (derived)
- `previews/characters/Claude_runner/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/f1_characters.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
