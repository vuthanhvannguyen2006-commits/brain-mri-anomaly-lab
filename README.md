# Brain MRI Anomaly Lab

A learning project exploring how AI can locate abnormal regions in brain MRI and, eventually, classify findings.

**Status:** first MRI exploration and audit completed; preparing YOLO segmentation data. No models have been trained and no performance results are claimed. This is a research and learning project, not a diagnostic tool.

Current focus: segment edema, enhancing tumor, and non-enhancing tumor. Specific tumor-type diagnosis is deferred.

## Research questions

- Does locating abnormalities first improve multi-label classification compared with classifying the whole MRI?
- Does combining whole-MRI and localized-region information help further?
- How does joint YOLO localization and classification compare with a two-step system, if suitable labels become available?
- How well do these systems handle irregular boundaries, multiple lesions, and coexisting conditions?
- What evidence supports each prediction, and how reliable are explanations?

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

## Dataset

We begin with **Medical Segmentation Decathlon, Task01_BrainTumour**. The downloader uses HTTP byte ranges to scan archive headers and fetch one case, skipping unrelated contents. Scanning may take several minutes; progress shows transferred bytes. Re-running it skips existing files with the expected byte size.

- [Dataset website](https://medicaldecathlon.com/)
- [Public AWS registry and license](https://registry.opendata.aws/msd/)
- [Dataset paper](https://doi.org/10.1038/s41467-022-30695-9)

The dataset is distributed under **CC BY-SA 4.0**. Its license is separate from the MIT license for this repository's original code. MRI data is not included in this repository. See [data notes](docs/DATA.md).

**Scope limitation:** this dataset supports tumor-region segmentation. Region labels are not separate tumor diagnoses. It does not provide a complete tumor-versus-hemorrhage classification task or a representative normal examination cohort.

## Learning roadmap

- [x] Project structure and first exploration notebook
- [x] Complete first MRI and expert-mask exploration
- [x] Inspect the starter sample and audit its annotations
- [ ] Prepare YOLO segmentation annotations in notebook 1_2 (current activity)
- [ ] Select suitable diagnostic data for future multi-condition studies
- [ ] Define target conditions and patient-separated splits
- [ ] Train a small YOLO segmentation learning baseline
- [ ] Train a whole-MRI multi-label classifier
- [ ] Adapt localization and train a two-step classifier on the diagnostic dataset
- [ ] Compare whole-MRI, expert-region, predicted-region, and combined-input models
- [ ] Compare joint YOLO diagnostic predictions when matching location labels exist
- [ ] Evaluate coexisting conditions, 3D context, uncertainty, and explainability
- [ ] Publish reproducible results and a public-sample demo

Follow the [step-by-step roadmap](docs/ROADMAP.md) and [experiment design](docs/EXPERIMENTS.md). No model training or evaluation has been completed.

## Repository layout

```text
notebooks/   Guided learning exercises
scripts/     Small reusable utilities
docs/        Dataset notes and experiment design
data/        Local downloads; ignored by Git
outputs/     Local figures and results; ignored by Git
```

Model checkpoints, downloaded scans, credentials, and generated notebook outputs are excluded from version control. Before publishing a notebook, use **Restart Kernel and Clear Outputs**, save it, and review the staged changes.

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
