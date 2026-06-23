import json

NB = r'ML Engineering & Ops.ipynb'
with open(NB, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']
issues = []
ok = []

for i, c in enumerate(cells):
    if c.get('cell_type') != 'code':
        continue
    ec = c.get('execution_count')
    out = c.get('outputs', [])
    src = ''.join(c.get('source', []))
    short = src[:70].replace('\n', ' ').strip()

    if ec is None:
        issues.append(f'Cel {i+1}: NOOIT UITGEVOERD  -- {short}')
    for o in out:
        if o.get('output_type') == 'error':
            ename = o.get('ename', '')
            evalue = str(o.get('evalue', ''))[:80]
            issues.append(f'Cel {i+1}: FOUT OPGESLAGEN  -- {ename}: {evalue}')

total_code = sum(1 for c in cells if c.get('cell_type') == 'code')
print(f'Codecellen totaal  : {total_code}')
print(f'Problemen gevonden : {len(issues)}')
print()
for issue in issues:
    print(issue)
if not issues:
    print('Geen problemen gevonden.')
