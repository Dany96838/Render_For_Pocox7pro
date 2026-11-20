#!/usr/bin/env python3
"""POCO v0.2.0: explicit specialization, no unmeasured rendering shortcuts."""
from pathlib import Path
import argparse
import runpy
import json

def replace_once(text, old, new, label):
    if text.count(old) != 1:
        raise RuntimeError(f'Unexpected source layout: {label}')
    return text.replace(old, new, 1)

def specialize(root):
    changes = {}
    p = root/'app/build.gradle.kts'
    s = p.read_text()
    s = replace_once(s, 'applicationId = "com.fcl.plugin.mobileglues"',
                     'applicationId = "com.dany96838.render.pocox7pro"', 'applicationId')
    s = replace_once(s, 'versionName = "2.0.0"', 'versionName = "0.2.0-poco-experimental"', 'versionName')
    s = replace_once(s, 'signingConfig = signingConfigs.getByName("release")',
                     'signingConfig = signingConfigs.getByName("debug")', 'test signature')
    s = replace_once(s, 'isMinifyEnabled = true', 'isMinifyEnabled = false', 'diagnostic names')
    s = replace_once(s, 'resValue("string","app_name","MobileGlues")',
                     'resValue("string","app_name","Render POCO X7 Pro (Experimental)")', 'app label')
    s = replace_once(s, '"MobileGlues (OpenGL 4.0, 1.17+)"',
                     '"Render POCO X7 Pro experimental (MobileGlues fork)"', 'FCL description')
    s = replace_once(s, '"MobileGlues:libmobileglues.so:libmobileglues.so"',
                     '"RenderPOCOX7Pro:libmobileglues.so:libmobileglues.so"', 'FCL renderer label')
    changes[p] = s

    core = root/'MobileGlues/MobileGlues-cpp'
    p = core/'config/gpu_utils.cpp'
    s = p.read_text()
    start = s.index('int isAdreno(const char* gpu) {')
    end = s.index('static std::optional<int> hasVk12;', start)
    block = s[start:end]
    if block.count('int isAdreno') != 4 or block.count('bool checkIfANGLESupported') != 1:
        raise RuntimeError('Unexpected classifier block')
    s = s[:start] + '''// Specialized distribution: no Adreno model classification.
// Unknown renderers retain a conservative automatic ANGLE decision;
// explicit ForceEnable/ForceDisable options in settings.cpp remain intact.
bool checkIfANGLESupported(const char* gpu) {
    return gpu != nullptr && strstr(gpu, "Mali-G720") != nullptr && hasVulkan12();
}

''' + s[end:]
    changes[p] = s

    p = core/'config/gpu_utils.h'
    s = p.read_text()
    for name in ('isAdreno', 'isAdreno730', 'isAdreno740', 'isAdreno830'):
        s = replace_once(s, f'    int {name}(const char* gpu);\n\n', '', name+' declaration')
    changes[p] = s

    p = core/'config/settings.cpp'
    s = p.read_text()
    for name, var in [('isAdreno','isQcom'), ('isAdreno730','is730'), ('isAdreno740','is740'), ('isAdreno830','is830')]:
        s = replace_once(s, f'    int {var} = {name}(gpu_cstr);\n', '', name+' call')
    for label, var in [('Is Adreno?', 'isQcom'), ('Is Adreno 730?', 'is730'), ('Is Adreno 740?', 'is740'), ('Is Adreno 830?', 'is830')]:
        s = replace_once(s, f'    LOG_D("{label} = %s", {var} ? "true" : "false")\n', '', label+' log')
    marker = '    bool isANGLESupported = checkIfANGLESupported(gpu_cstr);\n'
    s = replace_once(s, marker, marker + '''    LOG_V("[RenderPOCO v0.2.0] GPU = %s; automatic ANGLE eligible = %d",
          gpu_cstr, static_cast<int>(isANGLESupported))
    if (gpuString.find("Mali-G720") == std::string::npos) {
        LOG_W_FORCE("[RenderPOCO] Target Mali-G720 not identified; automatic ANGLE remains off. Explicit backend options are preserved.")
    }
''', 'profile log')
    changes[p] = s

    p = root/'app/src/main/AndroidManifest.xml'
    s = p.read_text()
    for name in ('MGApplication', 'MainActivity', 'MgQueryService'):
        s = replace_once(s, f'android:name=".{name}"',
                         f'android:name="com.fcl.plugin.mobileglues.{name}"', 'manifest '+name)
    changes[p] = s
    for p, s in changes.items():
        p.write_text(s)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--patch-only', type=Path)
    args = parser.parse_args()
    if args.patch_only:
        specialize(args.patch_only)
        return
    runpy.run_path(str(Path(__file__).with_name('prepare.py')), run_name='__main__')
    specialize(Path('work/plugin'))
    p = Path('work/build-identity.json')
    info = json.loads(p.read_text())
    info.update(version='0.2.0-poco-experimental', variant='release',
                signing='Android debug certificate (not production)',
                applicationId='com.dany96838.render.pocox7pro',
                modifications=['arm64-only','Adreno classification removed',
                               'target-gated automatic ANGLE','separate install identity',
                               'upstream release native build flags; no new fast-math'])
    p.write_text(json.dumps(info, indent=2)+'\n')
    print('Prepared POCO v0.2.0. No measured FPS or shader support claims.')

if __name__ == '__main__':
    main()
