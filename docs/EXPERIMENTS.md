# Planned segmentation experiments

This document records the initial experiment and plans for further evaluation.

## Current question

How accurately can a semantic model reproduce expert tissue-region masks while preserving irregular boundaries and holes?

The target is one categorical label per pixel/voxel: background, edema, non-enhancing tumor, or enhancing tumor. These labels do not constitute tumor-type diagnosis. Semantic segmentation can represent disconnected regions without converting them into separate object instances.

## Initial baseline

A small 2D U-Net in PyTorch uses a slice input and four per-pixel class scores. Start with a single-case overfit check only to verify the training pipeline. Keep integer expert masks directly; no polygon conversion or intentional filling of holes is needed.

FLAIR-only input is an initial learning simplification. It may not provide sufficient information for all expert labels; multi-sequence input is a planned comparison, not a proven improvement.

## Controlled comparisons

- Single-sequence versus multi-sequence input with other settings comparable.
- 2D versus neighboring-slice context (2.5D).
- A later 3D CNN baseline, documenting capacity and compute differences.
- Transformers or YOLO-based alternatives only when justified by a specific research question.

Use identical patient-separated evaluation sets. Split before extracting slices, and keep all sequences and repeat examinations of a patient together. Record seeds, normalization, augmentations, versions, runtime, and hardware. Apply spatial transforms consistently to images and masks; categorical mask resampling must preserve label identities. Do not tune on the test set.

## Evaluation

Report per-region Dice, surface distances in millimeters, volume errors, and false positives. Document handling of absent classes. Inspect holes, small regions, and consistency across slices. Use patient-level uncertainty estimates once sufficient cases exist. Retain original expert masks as the reference.

Preserved contour reconstruction on inspected slice 52 matched the source exactly. Filling edema outlines instead added 94 pixels: 26 from background and 68 from enhancing tumor. This is a preprocessing observation on one slice, not model performance.

## Deferred questions

Tumor-type diagnosis and whole-MRI versus two-step diagnostic classification are outside the active scope. Revisit only with appropriate diagnostic evidence, verified scan-level/region labels, and coexisting-condition data where relevant. Do not interpret region categories as diagnoses.

## Recorded notebook 1_2 result

One fixed batch from BRATS_457, four FLAIR slices, 60 updates per model, Adam learning rate 0.001, and unweighted cross-entropy. The z-score model restores the raw model’s saved initial state; the recorded equality check passed. The notebook includes seed setup and retained figures. These are training-batch diagnostics, not held-out validation.

- Raw final recorded pre-update loss: 0.139491; edema Dice: 0.000; 35 predicted edema pixels.
- Z-score final recorded pre-update loss: 0.030717; edema Dice: 0.861; 8,678 predicted edema pixels.
- Expert edema: 8,027 pixels; enhancing tumor: 566 pixels. Neither model predicted enhancing tumor.
- Non-enhancing tumor: absent; Dice not scored.

Decision: use z-score provisionally. Improved optimization on one batch does not establish an improvement on unseen patients. Region-specific metrics are necessary because falling aggregate loss concealed foreground failure.
