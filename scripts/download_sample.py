"""Download one MSD case using byte ranges, without downloading the full tar."""

import argparse
import io
import json
import tarfile
from pathlib import Path
from urllib.request import Request, urlopen

URL = "https://msd-for-monai.s3.us-west-2.amazonaws.com/Task01_BrainTumour.tar"


class RemoteTar(io.RawIOBase):
    """Seekable HTTP reader: seeking changes position without transferring data."""

    def __init__(self, url):
        self.url = url
        self.position = 0
        self.transferred = 0

    def readable(self):
        return True

    def seekable(self):
        return True

    def tell(self):
        return self.position

    def seek(self, offset, whence=0):
        if whence == 0:
            self.position = offset
        elif whence == 1:
            self.position += offset
        else:
            raise ValueError("Seeking from archive end is unsupported")
        return self.position

    def read(self, size=-1):
        if size < 0:
            raise ValueError("Unbounded reads would download the archive")
        if size == 0:
            return b""
        start = self.position
        request = Request(self.url, headers={"Range": f"bytes={start}-{start + size - 1}"})
        with urlopen(request, timeout=60) as response:
            if response.status != 206:
                raise RuntimeError("Server did not honor a partial request; stopped to avoid a full download")
            content_range = response.headers.get("Content-Range", "")
            if not content_range.startswith(f"bytes {start}-"):
                raise RuntimeError("Unexpected partial response offset")
            data = response.read(size)
        self.position += len(data)
        self.transferred += len(data)
        return data


def download_sample(output_dir: Path, case: str | None = None) -> Path:
    output_dir = Path(output_dir)
    prefix = "Task01_BrainTumour/"
    if case and (Path(case).name != case or not case.endswith('.nii.gz')):
        raise ValueError("Use a filename such as BRATS_001.nii.gz")
    manifest_path = output_dir / 'sample_manifest.json'
    if manifest_path.exists():
        previous = json.loads(manifest_path.read_text())
        if previous.get('source_url') == URL and (case is None or case == previous['case']):
            if all((output_dir / obj['path']).is_file() and
                   (output_dir / obj['path']).stat().st_size == obj['bytes']
                   for obj in previous['objects']):
                print('Sample already downloaded:', previous['case'])
                return output_dir
    print('Scanning archive headers; skipping unrelated image contents.', flush=True)
    print('This may take several minutes. The full archive will not be downloaded.', flush=True)
    remote = RemoteTar(URL)
    found = {}
    selected = case
    with tarfile.open(fileobj=remote, mode='r:') as archive:
        for count, member in enumerate(archive):
            if count % 100 == 0:
                print(f'Inspected {count} entries; transferred {remote.transferred / 1e6:.1f} MB', flush=True)
            if not member.isfile():
                continue
            name = member.name.removeprefix('./').removeprefix(prefix)
            path = Path(name)
            if path.name.startswith('._'):
                continue
            # Choose whichever image/mask case occurs first, then find its partner.
            if selected is None and path.parent.as_posix() in ('imagesTr', 'labelsTr') and name.endswith('.nii.gz'):
                selected = path.name
                print('Selected:', selected, flush=True)
            wanted = {'dataset.json', f'imagesTr/{selected}', f'labelsTr/{selected}'}
            if name not in wanted or name in found:
                continue
            destination = output_dir / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            temporary = destination.with_name(destination.name + '.part')
            source = archive.extractfile(member)
            with temporary.open('wb') as target:
                while chunk := source.read(4 * 1024 * 1024):
                    target.write(chunk)
            if temporary.stat().st_size != member.size:
                raise RuntimeError(f'Incomplete transfer: {name}')
            temporary.replace(destination)
            found[name] = {'path': name, 'bytes': member.size}
            print('Saved:', destination, flush=True)
            if len(found) == 3:
                break
    if len(found) != 3:
        raise RuntimeError(f'Could not find complete case {selected}; found {list(found)}')
    manifest = {'source_url': URL, 'case': selected, 'objects': list(found.values()),
                'transferred_bytes': remote.transferred}
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'Done. Transferred {remote.transferred / 1e6:.1f} MB.', flush=True)
    return output_dir


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', help='Optional exact case filename')
    parser.add_argument('--output-dir', type=Path, default=Path(__file__).resolve().parents[1] / 'data' / 'sample')
    args = parser.parse_args()
    download_sample(args.output_dir, args.case)
