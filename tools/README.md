# Workshop Tools

No production scripts are required for the initial guidelines-only setup. Add small, purpose-built tools **when a model-generation batch is explicitly commissioned**.

Suggested minimum tasks for the first pilot:
- `generate`: generate valid MagicaVoxel-compatible `.vox` from reproducible geometry data when useful.
- `validate`: parse VOX source, verify bounds/palette/counts, metadata, catalog references, pivot and dimensions.
- `preview`: render the **actual voxels** in consistent three-quarter, front, side and scale-reference views.
- `export`: optionally derive an optimized `.glb` mesh with correct orientation and materials.
- `contact_sheet`: combine real rendered previews into one batch-review image.

Avoid prebuilding a large framework, a Godot add-on, or hundreds of empty files. Prefer Python standard-library tools where practical, with optional imaging/3D dependencies documented if needed.

Do not claim that a self-written binary VOX parser alone proves external editor compatibility. Record what was actually verified.
