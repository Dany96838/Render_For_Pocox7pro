#!/usr/bin/env python3
"""Reuse the validated baseline collector for the separate POCO release build."""
from pathlib import Path

source = Path(__file__).with_name('collect.py').read_text()
replacements = {
    'app/build/outputs/apk/debug': 'app/build/outputs/apk/release',
    'Render-POCO-X7-Pro-baseline-v0.1.0-debug.apk': 'Render-POCO-X7-Pro-v0.2.0-experimental.apk',
}
for old, new in replacements.items():
    if source.count(old) != 1:
        raise SystemExit(f'Unexpected baseline collector layout: {old}')
    source = source.replace(old, new, 1)
exec(compile(source, 'collect-poco-baseline-adapter', 'exec'), {'__name__': '__main__'})

# Preserve generated compile command evidence if available, without requiring
# it to exist or pretending a missing file proves a particular optimization.
import shutil
for index, p in enumerate(Path('work/plugin/MobileGlues').rglob('compile_commands.json')):
    shutil.copy2(p, Path('artifacts')/f'core-compile-commands-{index}.json')
