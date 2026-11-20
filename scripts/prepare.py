#!/usr/bin/env python3
from pathlib import Path
import subprocess, json

PLUGIN = "f5105e4ddd1752cccdcc6421c402960d40ec3d9d"
CORE = "f56af31d3e490d95808b3adc4ace20234249a37a"

def run(*args, cwd=None):
    subprocess.run(args, cwd=cwd, check=True)

root = Path("work/plugin")
if root.exists():
    raise SystemExit("work/plugin already exists; refusing to overwrite")
root.parent.mkdir(parents=True, exist_ok=True)
run("git", "clone", "--no-checkout", "https://github.com/MobileGL-Dev/MobileGlues-plugin.git", str(root))
run("git", "checkout", "--detach", PLUGIN, cwd=root)
run("git", "submodule", "update", "--init", "--recursive", cwd=root)
actual = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root/"MobileGlues", text=True).strip()
if actual != CORE:
    raise SystemExit(f"Unexpected MobileGlues core revision: {actual}")
for relative in ("app/build.gradle.kts", "MobileGlues/build.gradle.kts"):
    path = root / relative
    source = path.read_text()
    marker = "    defaultConfig {\n"
    if source.count(marker) != 1:
        raise SystemExit(f"Unexpected Gradle layout: {relative}")
    path.write_text(source.replace(marker, marker + '        ndk { abiFilters += listOf("arm64-v8a") }\n', 1))
Path("work/build-identity.json").write_text(json.dumps({
    "plugin": PLUGIN, "core": CORE, "abi": "arm64-v8a",
    "variant": "debug", "status": "experimental; stable release equivalence unverified"
}, indent=2) + "\n")
print("Pinned sources prepared for arm64 debug build.")
