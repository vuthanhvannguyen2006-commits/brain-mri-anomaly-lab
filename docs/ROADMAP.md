# Learning roadmap

## 1. Understand one MRI — completed first exploration

Learn volume, slice, sequence, voxel spacing, and mask labels. Display expert regions with a fixed-color legend. Explain why edema, non-enhancing tumor, and enhancing tumor are region labels rather than separate diagnoses.

Deliverable: exploration notebook and observations. CPU is enough.

## 2. Choose data for the final question — current stage

Start with `notebooks/1_1_msd_task01_brain_tumour_dataset_explore_mri_and_data_audit.ipynb` to inventory the starter case and identify missing diagnostic labels. Then define a small set of target conditions. Audit MRI datasets for verified diagnoses, coexisting conditions, normal examinations, mimics, sequence availability, and location annotations. Complete this before extensive training.

Keep positive, verified-negative, and unknown labels distinct. Missing findings are not confirmed absences. Labels must belong to the actual scan used. Check patient overlap across data sources and keep repeat scans together when splitting.

Deliverable: dataset audit, label definitions, and patient-separated train/validation/test manifest. If multi-condition data is unavailable, narrow the claims explicitly.

## 3. Learn localization with YOLO

Prepare slices and derive boxes from masks on a small starter-data subset. Split by patient before extracting slices. Train a YOLO segmentation baseline and inspect boundary errors.

Deliverable: reproducible region-segmentation exercise, not tumor-diagnosis classification.

## 4. Build the whole-MRI classifier

On the diagnostic dataset, predict one independent probability per condition. Begin with a manageable slice/patch encoder and aggregate information across the examination. Do not use only a manually selected abnormal slice.

Deliverable: baseline examination-level predictions and evaluation.

## 5. Build the two-step classifier

Validate and adapt localization on the diagnostic dataset. Retain multiple candidates and surrounding tissue. Classify candidates and combine evidence into examination-level probabilities.

Multiple lesions may share one diagnosis. Different conditions may occur in separate regions or overlap in one region. Use verified region labels, or learn from sets of crops using examination-level labels (multiple-instance learning). Do not copy every scan diagnosis onto every crop.

Deliverable: complete pipeline, including behavior for zero candidates and false-positive candidates. Missed lesions count in evaluation.

## 6. Test whether localization helps

Compare whole-MRI, expert-region, predicted-region, and full-MRI-plus-region models on the same patients. Add joint YOLO diagnostic classification when matching location and diagnosis annotations are available; overlapping conditions may need adapted object-label handling.

Deliverable: controlled results, patient-level uncertainty, and separate evaluation of cases with coexisting conditions. See EXPERIMENTS.md.

## 7. Add context and explanations

Compare 2D/2.5D and 3D context as separate experiments. Evaluate calibration, abstention, and attribution sanity checks. A segmentation mask shows location; it does not explain a class decision by itself.

Deliverable: documented failures, successes, and limitations.

## 8. Share the project

Publish code, configurations, documentation, and honest results on GitHub. Optionally publish weights with a model card and a Hugging Face demo using permitted public samples. Keep scans, credentials, and checkpoints outside the code repository.

Deliverable: reproducible public project with source attribution and clear research scope.

## Agreed scope and spatial-context progression

Current focus: localize and segment edema, enhancing tumor, and non-enhancing tumor. These are tissue-region categories, not tumor diagnoses. Specific tumor-type diagnosis is deferred for later consideration; appropriate diagnostic evidence and labels would be needed.

1. Start with 2D YOLO segmentation. Apply it slice by slice across the provided volume and reconstruct the predicted masks in 3D. Stacking predictions does not make the model a 3D model.
2. Test neighboring-slice inputs (2.5D), predicting the middle slice from adjacent slices. Keep MRI sequence channels distinct from spatial slice positions.
3. Establish a 3D CNN segmentation baseline using volumetric patches as memory permits.
4. Consider transformers only if they address a remaining problem and improve held-out performance. Sequential models are optional alternatives, not required because MRI has ordered slices: depth is spatial, not time.

Compare approaches on the same patient-separated evaluation data. Inspect consistency across slices as well as region overlap and boundary accuracy. Initial single-slice conversion is a learning exercise, not a complete training or evaluation dataset.
