# Brute
- Asset ID: Claude_brute
- Base ID: brute
- Creator: Claude
- Category: characters
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_F
- Scale family: full
- Intended uses: Enemy archetype: slow, tough (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A huge man who worked the cutting floor of a meat-packing plant on the edge of town; he was still in his overalls and heavy leather apron when it happened. Slow now, heavy-footed, carrying his weight forward.

Condition: **n/a**.

## Silhouette
The widest and tallest figure: a heavy trapezoid of shoulders over a barrel body, small head pushed forward, a long apron, arms held wide.

## Dimensions and orientation
- Width (X): 0.95 m
- Depth (Y): 0.45 m
- Height (Z): 2.1 m
- Grid: 19 x 9 x 42 cells at 0.05 m (detail tier), 1,775 occupied voxels
- Front direction: +Y (library voxel)
- Front: The character faces +Y in a neutral standing display pose.
- Pivot: Between the feet at ground level. (pivot_voxel [np.float64(9.5), np.float64(4.5), 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`black`, `denim`, `denim_dark`, `hair_black`, `hair_brown`, `leather`, `leather_dark`, `leather_deep`, `navy_dark`, `skin1_shadow`, `skin2`, `skin2_shadow`, `wool`, `wool_dark`

## Details included
- 2.1 m tall, broad sloping trapezius and a short thick neck
- Heavy barrel chest and belly; arms hanging wide of the body
- Thick bare forearms below rolled thermal sleeves; big hands
- Faded denim bib overalls, straps over the shoulders
- Knee-length dark leather apron with a neck strap and waist ties, a front pocket, worn pale edges and a rubbed patch where he wipes his hands
- Shaved head, short beard, small deep-set eyes
- Wide stance in big work boots

## Details excluded
- No blood, stains of the trade or gore
- No tool or weapon (separate catalog models)

## Construction and placement notes
- Collision suggestion: Upright capsule about 0.45 m in radius and dimensions_m[2] tall, centred on the pivot; static reference figure, no rig.

## Outputs
- `models/characters/Claude_brute/Claude_brute.vox` (editable master)
- `models/characters/Claude_brute/model.json`
- `models/characters/Claude_brute/Claude_brute.glb` (derived)
- `previews/characters/Claude_brute/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/f1_characters.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
