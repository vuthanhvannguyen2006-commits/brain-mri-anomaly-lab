# Planned experiments

These are plans, not completed experiments.

## Main question

Does localization improve examination-level multi-label classification over a whole-MRI classifier? Each condition gets an independent probability. Unknown labels are excluded from the relevant loss and metrics, not treated as negative.

## Models

- A: Whole-MRI classifier, using full-examination slice/patch aggregation if needed.
- B: Expert-region classifier with surrounding context; a reference for the potential benefit of localization, not a deployable pipeline or guaranteed upper bound.
- C: Predicted-region two-step pipeline: locate multiple candidates, classify, and aggregate examination evidence.
- D: Combined full-MRI and predicted-region model, preserving global context.
- E: Joint YOLO localization and diagnostic classification when corresponding region and diagnosis labels exist. Standard exclusive object labels may require adaptation for overlapping conditions.

Compare B and C on the same location-annotated held-out cases. This helps separate the value of localization from the impact of localization errors.

## Fair comparison

Use identical held-out patients, MRI sequence availability, and preprocessing. Keep classifier backbones and input resolution comparable where practical; document model capacity, tuning, and compute differences. Tune thresholds and aggregation only on validation data. Keep repeat scans and overlapping source cases in one split. Record seeds, versions, hardware, and runtime. Repeat with multiple seeds when feasible.

A later 3D-versus-2D architecture experiment is separate: it changes more than localization alone.

## Multiple lesions and conditions

Retain multiple candidate regions, not just the largest lesion. Compare a documented aggregation baseline, such as per-condition maximum, with learned aggregation when feasible. Calibrate final examination probabilities after aggregation on validation data.

Include false-positive crops in training. Use verified region labels or examination-supervised multiple-instance learning; do not assign all scan diagnoses to all crops. Define zero-candidate behavior and count missed lesions in full-pipeline evaluation. Validate a tumor-trained localizer before using it for other conditions. Diffuse findings may require semantic masks or global context.

## Evaluation

- Per condition: sensitivity, precision, precision–recall area, false positives, and prevalence at validation-selected thresholds; report macro averages.
- Examination: multi-label precision/recall, calibration, and separate coexisting-condition results.
- Localization: lesion sensitivity at false positives per examination, Dice, and surface distances in millimeters where annotations exist.
- Robustness: small lesions, lesion count, site/scanner, sequence availability, and external data where available.
- Uncertainty: patient-level confidence intervals and abstention performance, including coverage (fraction receiving predictions).

Evaluate all examinations, not only correctly detected lesions. Test attribution using model randomization, perturbations, occlusion, and sequence ablation. Record failures alongside representative successes.
