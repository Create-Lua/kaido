from pathlib import Path
import json
import shutil

def compile_package(temp_path: Path, package_name: str, output_dir: Path):
    """
    Takes extracted GitHub package → normalizes it into Kaido format
    """

    package_root = None

    # detect root folder OR flat structure
    items = list(temp_path.iterdir())

    if len(items) == 1 and items[0].is_dir():
        package_root = items[0]
    else:
        package_root = temp_path

    link_file = package_root / "link.txt"

    if not link_file.exists():
        raise Exception("Missing link.txt in package")

    # read file list
    files = [line.strip() for line in link_file.read_text().splitlines() if line.strip()]

    # build manifest
    manifest = {
        "name": package_name,
        "entry": files[0] if files else None,
        "files": files
    }

    # destination
    pkg_dir = output_dir / package_name
    files_dir = pkg_dir / "files"

    if pkg_dir.exists():
        shutil.rmtree(pkg_dir)

    files_dir.mkdir(parents=True, exist_ok=True)

    # copy files into Kaido format
    for f in files:
        src = package_root / f
        dst = files_dir / f

        dst.parent.mkdir(parents=True, exist_ok=True)

        if src.exists():
            shutil.copy2(src, dst)

    # write manifest
    with open(pkg_dir / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=4)

    return pkg_dir