# test
import sys
from pathlib import Path
import requests
import zipfile
import io
import shutil
import json
import time
import os

from tools.compiler import compile_package

KAIDO_DIR = Path.home() / ".kaido"
PACKAGES_DIR = KAIDO_DIR / "packages"

BASE_URL = "https://raw.githubusercontent.com/Create-Lua/kaido/main/packages"


# =============================
# INSTALL
# =============================
def install(pkg_name):
    url = f"{BASE_URL}/{pkg_name}.zip"

    print("Downloading...")
    r = requests.get(url)

    if r.status_code != 200:
        print(f"Failed to download package ({r.status_code})")
        print("URL:", url)
        return

    # sanity check (zip signature)
    if r.content[:4] != b'PK\x03\x04':
        print("Downloaded file is not a valid zip (bad URL or repo issue)")
        return

    temp = KAIDO_DIR / "_temp"

    if temp.exists():
        shutil.rmtree(temp)

    temp.mkdir(parents=True, exist_ok=True)

    zipfile.ZipFile(io.BytesIO(r.content)).extractall(temp)

    # =============================
    # FIX: unwrap nested folder
    # =============================
    contents = list(temp.iterdir())
    if len(contents) == 1 and contents[0].is_dir():
        temp = contents[0]

    print("Compiling...")

    compile_package(temp, pkg_name, PACKAGES_DIR)

    shutil.rmtree(KAIDO_DIR / "_temp", ignore_errors=True)

    print(f"✔ Installed {pkg_name}")


# =============================
# RUN
# =============================
def run(pkg_name):
    pkg_path = PACKAGES_DIR / pkg_name / "manifest.json"

    if not pkg_path.exists():
        print("Package not installed")
        return

    data = json.loads(pkg_path.read_text())

    entry = data.get("entry")

    if not entry:
        print("No entry file defined")
        return

    entry_path = PACKAGES_DIR / pkg_name / "files" / entry

    if not entry_path.exists():
        print("Entry file missing")
        return

    # =============================
    # FIX: proper import support
    # =============================
    pkg_files_dir = PACKAGES_DIR / pkg_name / "files"
    sys.path.insert(0, str(pkg_files_dir))

    # safer execution context
    code = open(entry_path).read()
    exec(compile(code, str(entry_path), "exec"), {
        "__name__": "__main__",
        "__file__": str(entry_path),
    })


# =============================
# MAIN
# =============================
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
        if len(args) < 2:
            print("Usage: kaido install <pkg>")
            return
        install(args[1])

    elif cmd == "run":
        if len(args) < 2:
            print("Usage: kaido run <pkg>")
            return
        run(args[1])

    else:
        print("Unknown command")


if __name__ == "__main__":
    main()