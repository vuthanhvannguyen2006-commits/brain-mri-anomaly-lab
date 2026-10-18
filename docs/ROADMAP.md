# Learning roadmap

## Current scope

Semantic segmentation of background (0), edema (1), non-enhancing tumor (2), and enhancing tumor (3). These are tissue-region categories, not tumor diagnoses. Tumor-type diagnosis and whole-MRI versus two-step diagnostic classification are deferred, not current milestones.

## 1. Investigation and preparation

- Completed: `1_1` sample download, MRI exploration, mask inspection, and audit.
- Completed: `1_2_semantic_segmentation_baseline_raw_vs_zscore.ipynb`, covering preparation and a fixed-batch U-Net comparison. Keep native integer masks; polygon export is no longer required. The contour exercise demonstrated how lossy conversion could alter annotations.
- Preserve mask holes and small regions. Verify shapes, affine alignment, label values, and image/mask transformations.
- Prepare one slice for inspection, then extend to the volume. Keep original files unchanged.
- Initial single-sequence FLAIR input is a learning simplification; region labels may require other sequences. Document this limitation and later compare multi-sequence input.

Deliverable: reproducible image/mask pairs with exact target-label preservation. Rename the notebook descriptively when appropriate, retaining the user's stage_activity numbering. Do not silently rename user files.

## 2. First semantic model

The completed baseline uses a small 2D U-Net in PyTorch: input MRI slice, output four per-pixel class scores. A one-case overfit exercise verifies the pipeline only; it cannot establish generalization.

Before validation, obtain more cases, verify patient grouping, and create patient-separated train/validation/test splits before slice extraction. Keep all sequences and repeated examinations of one patient in the same split.

Deliverable: working semantic training loop, predictions, and held-out evaluation when sufficient data exists.

## 3. Spatial context and MRI sequences

Compare single-sequence and multi-sequence inputs under matched conditions. Then progress from 2D to neighboring-slice context (2.5D) and a 3D CNN baseline. Keep sequence channels distinct from depth. Consider transformers only to address demonstrated remaining problems. Depth is spatial, not time; sequential models are optional.

Deliverable: controlled experiments on the same patient-separated data, including consistency across slices.

## 4. Evaluation and explainability

Report per-region Dice, boundary distances in millimeters, and volume error. Inspect absent classes, small regions, holes, and false positives. Keep expert masks as the reference. Investigate uncertainty and test attribution explanations rather than treating them as proof of valid reasoning.

Deliverable: documented performance, uncertainty, and representative failures. No clinical-use claims based on segmentation scores alone.

## 5. Share and revisit future questions

Publish code, configurations, and honest results. Keep private working notes excluded. One explicitly attributed public sample is bundled; other data stays ignored.

YOLO detection/instance segmentation can be a later comparison if it answers a defined question. It is not the required primary model for this semantic task. Diagnostic classification requires a separate data and label plan and is deferred.

## Checkpoint after notebook 1_2

Both raw and z-score experiments ran 60 updates on the same four-slice training batch. Z-score improved edema Dice from 0.000 to 0.861; neither model predicted enhancing tumor, and non-enhancing tumor was absent. Adopt z-score provisionally and retain raw results. Next activity remains to be planned; patient-separated evaluation and the unresolved smaller-region failure remain open. Preserve saved notebook outputs to show the evidence behind decisions.
