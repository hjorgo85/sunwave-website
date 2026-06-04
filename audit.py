import re, glob, os

files = glob.glob('*.html') + glob.glob('blog/*.html')
print(f"{'FILE':<52} {'T_LEN':<8} {'D_LEN':<8} {'H1':<5} {'CANON':<7} {'OG':<5} {'SCHEMA'}")
print('-'*110)
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        c = fh.read()
    title = re.search(r'<title>(.*?)</title>', c)
    desc  = re.search(r'name="description"\s+content="(.*?)"', c)
    h1    = 'YES' if re.search(r'<h1', c) else 'NO'
    canon = 'YES' if 'rel="canonical"' in c else 'NO'
    og    = 'YES' if 'og:title' in c else 'NO'
    schema= 'YES' if 'ld+json' in c else 'NO'
    tlen  = len(title.group(1)) if title else 0
    dlen  = len(desc.group(1))  if desc  else 0
    tflag = ' LONG!' if tlen > 60 else ''
    dflag = ' MISSING!' if dlen == 0 else (' SHORT!' if dlen < 140 else '')
    print(f'{f:<52} {str(tlen)+tflag:<8} {str(dlen)+dflag:<8} {h1:<5} {canon:<7} {og:<5} {schema}')

print()
print('sitemap.xml:', os.path.exists('sitemap.xml'))
print('robots.txt: ', os.path.exists('robots.txt'))

print('\n--- Images missing alt text ---')
missing = []
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        c = fh.read()
    for img in re.findall(r'<img[^>]+>', c, re.DOTALL):
        src = re.search(r'src="([^"]+)"', img)
        alt = re.search(r'alt="([^"]*)"', img)
        if src:
            if not alt or not alt.group(1).strip():
                missing.append((f, src.group(1).split('/')[-1]))
print(f'Total: {len(missing)}')
for f, s in missing[:20]:
    print(f'  {f}: {s}')
