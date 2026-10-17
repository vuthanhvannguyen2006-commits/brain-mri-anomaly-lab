# Data notes

Start with one case from Medical Segmentation Decathlon Task01_BrainTumour.
The image contains multiple MRI sequences; the mask contains integer region labels.
Read `dataset.json` to determine channel order and label meanings rather than guessing.

The public bucket is `msd-for-monai` in AWS region `us-west-2`.
The registry documents anonymous access: https://registry.opendata.aws/msd/.
The downloader records the archive URL, member paths, and byte sizes in a local manifest. It uses partial HTTP requests because the bucket contains tar archives.
Size checking detects incomplete transfers; it is not a cryptographic integrity check.

Keep original files unchanged. Keep all examinations belonging to a patient in one
split, and create splits before extracting slices. Verify patient identity grouping
from available metadata before treating filenames as patient identifiers.

Do not interpret a tumor-free slice from a tumor case as a normal examination.
Additional datasets and consistent diagnostic labels will be required for disease
classification and hemorrhage detection. Check overlap with BraTS-derived data
before combining datasets.

The dataset license is CC BY-SA 4.0 according to the AWS registry. Preserve source
attribution and check its terms before redistributing data or derivatives. The code
license in this repository does not relicense the dataset.

## Diagnostic dataset requirements

For each target condition, distinguish positive, verified negative, and unknown labels. An examination may have several conditions; absent annotations do not prove absence. Distinguish scan diagnoses from region labels. Do not copy every scan diagnosis onto every crop. Check sequence compatibility and validate localization on the diagnostic dataset before reusing the tumor-only localizer.
