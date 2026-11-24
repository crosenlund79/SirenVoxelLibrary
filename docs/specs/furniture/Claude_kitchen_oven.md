# Stove / Oven
- Asset ID: Claude_kitchen_oven
- Base ID: kitchen_oven
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Cooker; game prop 'stove' (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A plain white enamel gas range that cooked for a family for fifteen years. The front-left burner was the favourite: its drip pan is burnt brown and grease has run down the front below its knob. Nobody has lit it since the gas stopped.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.7 m
- Depth (Y): 0.65 m
- Height (Z): 1.0 m
- Grid: 14 x 13 x 20 cells at 0.05 m (detail tier), 1,212 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [7.0, 6.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`almond`, `almond_dark`, `charcoal`, `chrome`, `coal`, `glass_dark`, `glass_deep`, `iron`, `iron_dark`, `iron_edge`, `porcelain`, `porcelain_hi`, `porcelain_mid`, `porcelain_shadow`, `rust_deep`, `screen`

## Details included
- Four burners: cast-iron square grates over chrome drip pans and iron caps
- Backguard with a lit top edge
- Control strip with four knobs and a small clock window
- Oven door with a dark window and a chrome handle bar
- Storage drawer and recessed kick
- Grease burnt into the favourite burner and run down the front below its knob

## Details excluded
- No brand plate or readable dial text
- No flames or glow

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.7 x 0.6 m

## Outputs
- `models/furniture/Claude_kitchen_oven/Claude_kitchen_oven.vox` (editable master)
- `models/furniture/Claude_kitchen_oven/model.json`
- `models/furniture/Claude_kitchen_oven/Claude_kitchen_oven.glb` (derived)
- `previews/furniture/Claude_kitchen_oven/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a3_kitchen.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
