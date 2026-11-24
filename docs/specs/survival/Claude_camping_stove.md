# Camping Stove
- Asset ID: Claude_camping_stove
- Base ID: camping_stove
- Creator: Claude
- Category: survival
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Cooking without grid power (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The family's green two-burner camp stove, lid propped up as a windshield on the back step. It runs off a small propane bottle on a rubber hose; one burner is crusted from a pot that boiled over.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.5 m
- Depth (Y): 0.275 m
- Height (Z): 0.325 m
- Grid: 20 x 11 x 13 cells at 0.025 m (fine tier), 752 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the working / interaction side.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [13.0, 5.0, 0.0])
- Resolution rationale: 2.5 cm cells: a handheld or small gear item whose handles, straps and blades would be 2-4x too thick at 5 cm.

## Materials and colors
`black`, `brass`, `brass_dark`, `card_deep`, `galv`, `galv_dark`, `green`, `green_dark`, `green_hi`, `iron`, `iron_edge`, `label_blue`, `steel`, `steel_dark`, `steel_light`

## Details included
- Green enamelled case, the lid up with its two side flaps folded forward
- Two burners under a wire grate, front control knobs
- Small propane bottle with a brass regulator and a hose to the side inlet
- Boil-over crust around the left burner

## Details excluded
- No flames
- No brand or warning labels

## Construction and placement notes
- Collision suggestion: Box 0.35 x 0.25 x 0.08 m for the case; lid, flaps and bottle as separate boxes if needed.
- Placement footprint: 0.35 x 0.25 m

## Outputs
- `models/survival/Claude_camping_stove/Claude_camping_stove.vox` (editable master)
- `models/survival/Claude_camping_stove/model.json`
- `models/survival/Claude_camping_stove/Claude_camping_stove.glb` (derived)
- `previews/survival/Claude_camping_stove/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b2_survival_gear.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
