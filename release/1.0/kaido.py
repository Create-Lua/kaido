import sys
from pathlib import Path
import requests
import zipfile
import io
import shutil
import time

from tools.compiler import compile_package

KAIDO_DIR = Path.home() / ".kaido"
PACKAGES_DIR = KAIDO_DIR / "packages"

BASE_URL = "https://raw.githubusercontent.com/Create-Lua/kaido/main/packages"


def install(pkg_name):
    url = f"{BASE_URL}/{pkg_name}.zip"

    print("Downloading...")
    r = requests.get(url)

    if r.status_code != 200:
        print("Failed to download package")
        return

    temp = KAIDO_DIR / "_temp"

    if temp.exists():
        shutil.rmtree(temp)

    temp.mkdir(parents=True, exist_ok=True)

    zipfile.ZipFile(io.BytesIO(r.content)).extractall(temp)

    print("Compiling...")

    compile_package(temp, pkg_name, PACKAGES_DIR)

    shutil.rmtree(temp)

    print(f"✔ Installed {pkg_name}")


def run(pkg_name):
    pkg_path = PACKAGES_DIR / pkg_name / "manifest.json"

    if not pkg_path.exists():
        print("Package not installed")
        return

    import json

    data = json.loads(pkg_path.read_text())

    entry = data.get("entry")

    if not entry:
        print("No entry file defined")
        return

    entry_path = PACKAGES_DIR / pkg_name / "files" / entry

    if not entry_path.exists():
        print("Entry file missing")
        return

    exec(open(entry_path).read(), {})


def main():
    KAIDO_DIR.mkdir(parents=True, exist_ok=True)
    PACKAGES_DIR.mkdir(parents=True, exist_ok=True)

    args = sys.argv[1:]

    if not args:
        print("Kaido 1.0")
        print("Commands: install <pkg> | run <pkg>")
        return

    cmd = args[0]

    if cmd == "install":
        install(args[1])
    elif cmd == "run":
        run(args[1])
    else:
        print("Unknown command")

if __name__ == "__main__":
    main()