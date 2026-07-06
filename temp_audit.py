import re
lines = open('app.py', encoding='utf-8').readlines()
for i, line in enumerate(lines, 1):
    if i > 370 and 'style=' in line and 'border-radius' in line:
        m = re.findall(r'border-radius\s*:\s*([0-9]+px)', line, re.IGNORECASE)
        if m and m[0] not in ('20px','22px','24px','28px','999px'):
            print(f'L{i:5d}  {m[0]:6s}  {line.strip()[:180]}')
