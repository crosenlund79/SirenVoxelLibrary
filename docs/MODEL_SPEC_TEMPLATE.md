# Model Specification Template

Copy this template to `docs/specs/<category>/<asset_id>.md` when a specific asset is proposed. The asset ID is exactly `GPT_<base_id>` or `Claude_<base_id>` (case-sensitive); both versions share the same base brief. A spec describes **one asset**, not an entire batch. Proposed dimensions, materials and resolutions may be revised during visual review.

```md
# <Readable model name>
- Asset ID: <GPT_base_id | Claude_base_id>
- Base ID: <lowercase_snake_case_id>
- Creator: <GPT | Claude>
- Category: <furniture | survival | vegetation | vehicles | decorations | architecture>
- Status: Proposed
- Intended uses: <possible game(s); not authorization to integrate>
- Brief approved by: <user / pending>

## Function and story
What does this object do? What small, believable story does its condition tell?

## Silhouette
Primary volume(s); recognizable functional details; desired asymmetry.
Which features must remain clear at three-quarter and thumbnail scale?

## Dimensions and orientation
- Width (X): <m>
- Depth (Y): <m>
- Height (Z): <m>
- Front direction: +Y (library voxel)
- Floor or attachment pivot: <bottom-center or named mount>
- Suggested cell size: <0.20 / 0.10 / 0.05 m> with reason

## Materials and colors
List material roles (e.g., aged pine, dark steel, canvas), local value variations, and small accent colors.

## Details to include
Functional details in descending order of importance.

## Details to exclude
No logos; no random speckling; list model-specific exclusions.

## Variant and state requirements
Default state only, or explicitly requested variants. Damage variants are never automatic.

## Construction and placement notes
Required ground contact, wall clearance, mounts, origin, collision proxy suggestions.
Only metadata in this library; game placement mechanics live in the receiving game.

## Required outputs
- Editable <asset_id>.vox
- model.json (creator, base ID, prefixed ID/source, dimensions, cell size, pivot, axes, palette roles, counts)
- Preview: three-quarter, front, side, and scale/scene comparison
- Optional derived <asset_id>.glb; if present, must be verified against source

## Acceptance checks
- [ ] Recognizable silhouette at thumbnail size
- [ ] Physically believable scale next to 1.75 m person
- [ ] Geometry is connected or separation is intentional/documented
- [ ] Correct forward/pivot/ground contact
- [ ] No unexplained voxel noise or oversized voxel count
- [ ] Source parses and matches render
- [ ] Preview images are actual renders from source, not generated concept images
- [ ] User has reviewed and explicitly approved this revision
```

### Scope discipline

Claude can propose improvements during generation, but a written spec or a proposal is **not user approval**. Claude must create only `Claude_` models, while ChatGPT uses `GPT_`; neither modifies the other's candidate. Work only on the models/batch the user actually authorizes. Use clear version identifiers if an already-approved asset needs a revision. Do not overwrite its source before approval.
