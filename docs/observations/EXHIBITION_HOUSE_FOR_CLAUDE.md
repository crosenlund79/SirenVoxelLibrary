# Future observation — The exhibition house

**Status:** User-requested observation to discuss with Claude later. **NOT an implementation request for this milestone.** This document does not authorize work in Sirens Went Quiet.

## Purpose

A dedicated **demonstration / exhibition house** should let us inspect **every real in-game item and voxel model together**, at the correct physical scale, under the game's actual lighting, materials and camera. It is a visual QA and art-review environment, not another survival level.

The user suggested access through the **F10 developer / cheat menu**.

## Desired behavior

1. Open a separate exhibition house from the cheat menu and return safely to the active game. Entering must not mutate the survival world, mission state, character inventory, or save.
2. **Automatically include every registered in-game model.** Whenever a voxel model is added to the game, the exhibit should display it as well. Prefer registry-driven, data-driven generation rather than a manually maintained list.
3. Display furniture, weapons, tools, construction pieces, consumables, medical items, equipment, vegetation, vehicles and architecture together in recognizable groups. For extremely large items, an exterior yard or annex may be more practical than squeezing them into rooms.
4. Group related objects at real scale with clear labels, enough spacing and representative lighting. Include an unobstructed way to move the camera around the models and compare appearances.
5. **Include models of every enemy archetype**, including runners, brutes and suicide bombers. They must be entirely **dormant**: no pursuit, attacks, nav requests, explosions, damage, hit responses or world-side effects.
6. Character/enemy exhibits should default to a neutral **T-pose** or the equivalent rig-compatible neutral/rest pose. Remain still rather than looping animations.
7. Show a clearly marked *missing model* placeholder for items that exist in the game registry but have no associated artwork. Don't silently hide unavailable entries.
8. Use the **game's actual runtime model selection and overrides**, not manually copied screenshots. This allows us to judge how the integrated Claude/GPT assets coexist, without treating library candidates as already integrated.
9. Whenever the registry changes or the house opens again, rebuild/reconcile the exhibit. Avoid duplicates and preserve deterministic grouping.
10. Include a way to filter/hide categories and optionally compare variants, but don't turn the scene into a fully fledged modeling application.

## Specific design caution

The user said **demonstration house**, rather than a museum-like asset gallery. A recognizable house with appropriate interior displays is the preferred starting image; if not all models fit, a simple adjoining garden/warehouse-like annex can be considered later.

## Scope boundary

- **Do not build this now.** Preserve it as a future Claude playtest/implementation observation.
- Do not edit Sirens Went Quiet to implement it until the user explicitly requests that work.
- The models in SirenVoxelLibrary are independent candidates. This exhibit should show *models actually integrated into the game*, not every unapproved library candidate.
