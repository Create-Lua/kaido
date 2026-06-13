from pathlib import Path
import requests
import zipfile
import io
import shutil
import os
import stat
import time

print("=================================")
print("        Kaido Installer")
print("=================================\n")

# -----------------------------
# CONFIG
# -----------------------------
BASE_URL = "https://raw.githubusercontent.com/Create-Lua/kaido/main/release"
KAIDO_DIR = Path.home() / ".kaido"
CLI_PATH = Path("/opt/homebrew/bin/kaido")

# -----------------------------
# VERSION PICK
# -----------------------------
version = input("Version (latest / 1.0 / 1.1) [latest]: ").strip()
if version == "":
    version = "latest"

# 🔥 FIX: cache busting so GitHub never serves old zip
url = f"{BASE_URL}/{version}.zip?v={int(time.time())}"

print(f"\n→ Version: {version}")
print(f"→ Source:  {url}\n")

# -----------------------------
# CONFIRM
# -----------------------------
confirm = input("Install Kaido? (y/n): ").strip().lower()
if confirm != "y":
    print("Cancelled.")
    exit()

# -----------------------------
# DOWNLOAD
# -----------------------------
print("\nDownloading Kaido...")

# 🔥 FIX: force no-cache headers
headers = {
    "Cache-Control": "no-cache",
    "Pragma": "no-cache"
}

r = requests.get(url, headers=headers)

if r.status_code != 200:
    print("❌ Download failed. Check version name.")
    exit()

# -----------------------------
# EXTRACT (DUMB SIMPLE CORE)
# -----------------------------
print("Extracting...")

temp_dir = KAIDO_DIR / "_temp"

if temp_dir.exists():
    shutil.rmtree(temp_dir)

temp_dir.mkdir(parents=True, exist_ok=True)

zipfile.ZipFile(io.BytesIO(r.content)).extractall(temp_dir)

KAIDO_DIR.mkdir(parents=True, exist_ok=True)

print("Installing files...")

for item in temp_dir.iterdir():
    dest = KAIDO_DIR / item.name

    if dest.exists():
        if dest.is_dir():
            shutil.rmtree(dest)
        else:
            dest.unlink()

    shutil.move(str(item), str(dest))

shutil.rmtree(temp_dir)

# -----------------------------
# CLI SETUP
# -----------------------------
print("\nSetting up CLI...")

kaido_main = KAIDO_DIR / "kaido.py"

if not kaido_main.exists():
    print("❌ kaido.py not found in package. CLI not created.")
    exit()

wrapper = f"""#!/bin/bash
exec python3 "{kaido_main}" "$@"
"""

CLI_PATH.write_text(wrapper)
os.chmod(CLI_PATH, os.stat(CLI_PATH).st_mode | stat.S_IEXEC)

# -----------------------------
# DONE
# -----------------------------
print("\n=================================")
print("✔ Kaido installed successfully!")
print(f"Location: {KAIDO_DIR}")
print("CLI: kaido")
print("=================================")