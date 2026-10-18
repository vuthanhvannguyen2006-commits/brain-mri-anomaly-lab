# Brain MRI Anomaly Lab

A learning project exploring how AI can locate abnormal regions in brain MRI and, eventually, classify findings.

**Status:** notebooks 1_1 and 1_2 completed, including a small U-Net fixed-batch training comparison. No held-out patient evaluation has been performed. This is a research and learning project, not a diagnostic tool.

Current focus: segment edema, enhancing tumor, and non-enhancing tumor. Specific tumor-type diagnosis is deferred.

## Research questions

- How accurately can semantic segmentation reproduce the annotated tissue regions, including irregular boundaries and holes?
- How do MRI sequence choice and neighboring-slice or 3D context affect performance?
- How reliable are uncertainty estimates and explanations?

The baseline is a small 2D U-Net using native pixel masks. YOLO instance segmentation is no longer the primary approach. Tumor-type diagnosis and diagnostic classification comparisons are deferred.

## Start here

Use Python 3.11 or 3.12 for the initial environment. The first exercise uses CPU; a GPU is unnecessary.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/download_sample.py
jupyter lab
```

Open `notebooks/1_1_msd_task01_brain_tumour_dataset_explore_mri_and_data_audit.ipynb`. It loads one MRI, reads the sequence and label definitions, and overlays its expert mask.

**Colab alternative:** upload the notebook to Colab and follow its setup cell. That cell downloads only one case and its mask into the temporary runtime. Keep the runtime on CPU.

## Completed baseline experiment

[Notebook 1_2: semantic segmentation baseline — raw versus z-score](notebooks/1_2_semantic_segmentation_baseline_raw_vs_zscore.ipynb) includes preparation, reproducibility setup, a small U-Net, and saved comparison plots.

On one fixed batch of four slices from case BRATS_457, after 60 updates per model, edema Dice was 0.000 for raw input and 0.861 for z-score input. Both models missed enhancing tumor; non-enhancing tumor was absent from this batch and was not scored. Z-score is the provisional preprocessing default, not a validated generalization result. The original masks remain unchanged.

## Dataset

We begin with **Medical Segmentation Decathlon, Task01_BrainTumour**. The downloader uses HTTP byte ranges to scan archive headers and fetch one case, skipping unrelated contents. Scanning may take several minutes; progress shows transferred bytes. Re-running it skips existing files with the expected byte size.

- [Dataset website](https://medicaldecathlon.com/)
- [Public AWS registry and license](https://registry.opendata.aws/msd/)
- [Dataset paper](https://doi.org/10.1038/s41467-022-30695-9)

The dataset is distributed under **CC BY-SA 4.0**. Its license is separate from the MIT license for this repository's original code. One attributed learning sample (case BRATS_457, approximately 9.7 MB) is included in `data/msd_brain_tumour_sample.zip`; other MRI data remains excluded. See [sample attribution and Colab loading instructions](data/README.md). See [data notes](docs/DATA.md).

**Scope limitation:** this dataset supports tumor-region segmentation. Region labels are not separate tumor diagnoses. It does not provide a complete tumor-versus-hemorrhage classification task or a representative normal examination cohort.

## Learning roadmap

- [x] Project structure, sample exploration, and data audit in notebook 1_1
- [x] Inspect contours and demonstrate the effect of filling holes on one slice
- [x] Prepare native semantic image/mask pairs in notebook 1_2
- [x] Run a small 2D U-Net fixed-batch learning diagnostic and compare raw versus z-score input
- [ ] Obtain sufficient cases and establish patient-separated evaluation splits
- [ ] Evaluate segmentation and compare single/multi-sequence input
- [ ] Compare 2D, 2.5D, and 3D context; consider transformers if justified
- [ ] Investigate uncertainty and explainability; publish reproducible results

Follow the [roadmap](docs/ROADMAP.md) and [experiment design](docs/EXPERIMENTS.md). Training-batch diagnostics have been completed; generalization to unseen patients remains untested.

## Repository layout

```text
notebooks/   Guided learning exercises
scripts/     Small reusable utilities
docs/        Dataset notes and experiment design
data/        Local downloads; ignored by Git
outputs/     Local figures and results; ignored by Git
```

Model checkpoints, other downloaded scans, and credentials are excluded from version control. The explicitly attributed sample ZIP is included. Retain reviewed notebook outputs and figures when they explain experimental decisions; check outputs for sensitive content before publishing. Saved outputs are evidence of a recorded run, not a substitute for a fresh-runtime reproducibility check.

## Publishing on GitHub

Create an empty public repository named `brain-mri-anomaly-lab` on GitHub. Do not initialize it with another README or license. From this project folder:

```bash
git init -b main
git add .
git diff --cached --stat
git diff --cached
git commit -m "Set up brain MRI learning project"
git remote add origin https://github.com/YOUR_USERNAME/brain-mri-anomaly-lab.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username. Review the staged changes before committing, especially for data and notebook outputs.
