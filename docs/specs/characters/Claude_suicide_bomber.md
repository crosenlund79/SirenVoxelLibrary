# Suicide Bomber
- Asset ID: Claude_suicide_bomber
- Base ID: suicide_bomber
- Creator: Claude
- Category: characters
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_F
- Scale family: full
- Intended uses: Enemy archetype: targets walls, telegraphed (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
Someone who strapped a scavenged hazard rig over their hoodie and walked toward the walls people had built. The kit is improvised and fictional: striped canisters on a back frame and a dead warning beacon, meant to be seen coming.

Condition: **n/a**.

## Silhouette
Bulky vested torso, a hooded head, two frame rails and canisters showing behind the shoulders and a beacon mast rising above the hood.

## Dimensions and orientation
- Width (X): 0.75 m
- Depth (Y): 0.55 m
- Height (Z): 1.9 m
- Grid: 15 x 11 x 38 cells at 0.05 m (detail tier), 1,269 occupied voxels
- Front direction: +Y (library voxel)
- Front: The character faces +Y in a neutral standing display pose.
- Pivot: Between the feet at ground level. (pivot_voxel [np.float64(7.5), np.float64(7.0), 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`algae_dark`, `black`, `card_dark`, `charcoal`, `concrete_dark`, `concrete_deep`, `concrete_hi`, `denim`, `denim_dark`, `hair_black`, `hazard_yellow_dark`, `khaki`, `khaki_dark`, `lamp_red`, `navy_dark`, `olive_dark`, `signal_red_dark`, `skin1_shadow`, `skin2_shadow`, `steel`, `steel_dark`

## Details included
- Hood up, face in shadow, head slightly lowered
- Bulky padded vest over the hoodie with generic packets and pouches and two plain wire runs (one dark red, one black) on the surface
- Steel back frame with two hazard-striped canisters and an unlit warning beacon on a short mast above the head (the gameplay telegraph)
- Jeans and worn trainers; arms held out from the body by the vest

## Details excluded
- Fictional hazard rig only: no realistic explosive, detonator, switch, timer or wiring detail; nothing instructional
- No insignia, slogans or text
- Nothing in the hands

## Construction and placement notes
- Collision suggestion: Upright capsule about 0.3 m in radius and dimensions_m[2] tall, centred on the pivot; static reference figure, no rig.

## Outputs
- `models/characters/Claude_suicide_bomber/Claude_suicide_bomber.vox` (editable master)
- `models/characters/Claude_suicide_bomber/model.json`
- `models/characters/Claude_suicide_bomber/Claude_suicide_bomber.glb` (derived)
- `previews/characters/Claude_suicide_bomber/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/f1_characters.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
