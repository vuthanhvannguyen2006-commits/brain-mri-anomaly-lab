# Bundled MRI sample: MSD Task01 BrainTumour

Case: BRATS_457.nii.gz, from Medical Segmentation Decathlon Task01_BrainTumour,
release 2.0 (04/05/2018), derived from BraTS glioma data.

Credit: Medical Segmentation Decathlon organizers and original BraTS data contributors.
Dataset reference supplied in dataset.json: https://www.med.upenn.edu/sbia/brats2017.html
Dataset website: https://medicaldecathlon.com/
Source archive: https://msd-for-monai.s3.us-west-2.amazonaws.com/Task01_BrainTumour.tar
Registry: https://registry.opendata.aws/msd/ (checked 2026-10-18).

License: Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).
License and terms: https://creativecommons.org/licenses/by-sa/4.0/
Legal code: https://creativecommons.org/licenses/by-sa/4.0/legalcode
This sample is not covered by the repository's MIT code license.

Citation: Simpson AL, Antonelli M, Bakas S, et al. A large annotated medical image
 dataset for the development and evaluation of segmentation algorithms (2019).
https://arxiv.org/abs/1902.09063

Changes: one image/mask pair and the dataset metadata were selected from the
source archive and repackaged as a ZIP with a generated download manifest and
this attribution notice. MRI, mask, and dataset.json contents are unchanged from
the locally supplied sample. No endorsement by the data creators is implied.

The labels describe edema, non-enhancing tumor, and enhancing tumor regions,
not tumor-type diagnoses. This single case is for learning and format checks;
it cannot establish generalization performance or support a patient-level split.

## Use in Colab

```python
from pathlib import Path
from urllib.request import urlretrieve
import zipfile

url = "https://raw.githubusercontent.com/vuthanhvannguyen2006-commits/brain-mri-anomaly-lab/main/data/msd_brain_tumour_sample.zip"
zip_path = Path("/content/msd_brain_tumour_sample.zip")
DATA_DIR = Path("/content/data/msd_task01_brain_tumour/sample")
urlretrieve(url, zip_path)
DATA_DIR.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(zip_path) as archive:
    archive.extractall(DATA_DIR)
assert (DATA_DIR / "imagesTr/BRATS_457.nii.gz").is_file()
assert (DATA_DIR / "labelsTr/BRATS_457.nii.gz").is_file()
```

ZIP SHA-256: `91b9f8f9b4b7d4054af22ec9b0957a5097a94b7c9fdad49ad1df75410f83a11f`
