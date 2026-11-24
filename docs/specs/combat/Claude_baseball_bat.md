# Baseball Bat
- Asset ID: Claude_baseball_bat
- Base ID: baseball_bat
- Creator: Claude
- Category: combat
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_C
- Scale family: full
- Intended uses: Melee weapon (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A youth-league ash bat from a garage shelf. Someone re-wrapped the handle with black electrical tape for a better grip; the barrel is scuffed grey and chipped on one side from striking concrete and fence posts.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.075 m
- Depth (Y): 0.775 m
- Height (Z): 0.075 m
- Grid: 6 x 62 x 6 cells at 0.0125 m (micro tier), 864 occupied voxels
- Front direction: +Y (library voxel)
- Front: Working end / muzzle points +Y, top side up; lowest point on z = 0.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [3.0, 31.0, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it. Overridden from 2.5 cm to 1.25 cm: at 2.5 cm the bat is 3 cells thick and its taper from barrel to handle, the knob and the taped grip collapse into a stick.

## Materials and colors
`black`, `charcoal`, `pine_aged`, `pine_dark`, `pine_hi`, `pine_light`, `pine_mid`, `wgrey`

## Details included
- Clear taper from a thick barrel through a long thin handle to a knob
- Handle spiral-wrapped in black tape, with the last wrap lifting
- Scuffed, darkened hitting zone with grey scrapes and a chipped dent
- Rounded barrel end

## Details excluded
- No brand stamp or lettering
- No nails, blood or gore

## Attachment points
- `grip`: voxel [2, 8, 2], [np.float64(-0.0062), np.float64(-0.2812), np.float64(0.0312)] m from the pivot. Both hands on the taped handle above the knob.

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.075 x 0.775 m

## Outputs
- `models/combat/Claude_baseball_bat/Claude_baseball_bat.vox` (editable master)
- `models/combat/Claude_baseball_bat/model.json`
- `models/combat/Claude_baseball_bat/Claude_baseball_bat.glb` (derived)
- `previews/combat/Claude_baseball_bat/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/c1_combat.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
