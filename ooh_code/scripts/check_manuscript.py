"""Check manuscript references and artifact paths."""
import re
import os

tex_files = []
for root, dirs, files in os.walk('manuscript'):
    for f in files:
        if f.endswith('.tex'):
            tex_files.append(os.path.join(root, f))

labels = set()
refs = set()
label_pat = re.compile(r'\\label\{([^}]+)\}')
ref_pat = re.compile(r'\\ref\{([^}]+)\}')
atable_pat = re.compile(r'\\ArtifactTable\{([^}]+)\}')
afig_pat = re.compile(r'\\ArtifactFigure\{([^}]+)\}')

for path in tex_files:
    with open(path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    labels.update(label_pat.findall(content))
    refs.update(ref_pat.findall(content))

undefined = []
for r in refs:
    if any(r.startswith(p) for p in ['tab:', 'fig:', 'sec:', 'eq:', 'app:']):
        if r not in labels:
            undefined.append(r)

if undefined:
    print('UNDEFINED REFERENCES:')
    for u in sorted(set(undefined)):
        print(f'  {u}')
else:
    print('All internal references resolve correctly.')

for path in tex_files:
    with open(path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    for match in atable_pat.finditer(content):
        apath = match.group(1)
        full = os.path.normpath(os.path.join(os.path.dirname(path), apath))
        if not os.path.exists(full):
            print(f'MISSING ARTIFACT: {apath} (from {path})')
    for match in afig_pat.finditer(content):
        apath = match.group(1)
        full = os.path.normpath(os.path.join(os.path.dirname(path), apath))
        if not os.path.exists(full):
            print(f'MISSING FIGURE: {apath} (from {path})')

print('Check complete.')
