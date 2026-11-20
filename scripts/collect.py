#!/usr/bin/env python3
from pathlib import Path
import zipfile, shutil, hashlib, subprocess, json

root = Path("work/plugin")
apks = list((root/"app/build/outputs/apk/debug").glob("*.apk"))
if len(apks) != 1:
    raise SystemExit(f"Expected one debug APK, found {len(apks)}")
source = apks[0]
with zipfile.ZipFile(source) as z:
    names = z.namelist()
    libs = [n for n in names if n.startswith("lib/") and n.endswith(".so")]
    abis = {n.split("/")[1] for n in libs}
    if abis != {"arm64-v8a"}:
        raise SystemExit(f"Unexpected packaged ABIs: {abis}")
    if "lib/arm64-v8a/libmobileglues.so" not in libs:
        raise SystemExit("Missing libmobileglues.so")
    if "AndroidManifest.xml" not in names:
        raise SystemExit("Missing AndroidManifest.xml")
out = Path("artifacts")
out.mkdir(exist_ok=True)
apk = out/"Render-POCO-X7-Pro-baseline-v0.1.0-debug.apk"
shutil.copy2(source, apk)
digest = hashlib.sha256(apk.read_bytes()).hexdigest()
(out/"SHA256SUMS.txt").write_text(f"{digest}  {apk.name}\n")
(out/"native-libraries.json").write_text(json.dumps(libs, indent=2)+"\n")
shutil.copy2("work/build-identity.json", out/"build-identity.json")
for name, cwd in (("plugin", root), ("core", root/"MobileGlues")):
    (out/f"{name}-build.patch").write_bytes(subprocess.check_output(["git", "diff"], cwd=cwd))
with zipfile.ZipFile(out/"corresponding-source.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        if any(part in {".git", ".gradle", ".cxx", "build"} for part in rel.parts):
            continue
        if p.name == "local.properties" or p.suffix in {".jks", ".keystore"}:
            continue
        z.write(p, str(Path("plugin")/rel))
print(f"APK validated and collected: {apk}")
