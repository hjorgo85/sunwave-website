"""
Comprehensive fix:
1. Correct German nav on all de/ pages (replace wholesale — no more text-node bugs)
2. Fix EN/DE switcher CSS (add media queries so mobile/desktop toggle correctly)
3. Remove duplicate/stray style blocks from all pages
4. Fix English pages nav
"""
import re, glob, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ── Correct switcher CSS ──────────────────────────────────────────────────────
SWITCHER_CSS = """<style>
  .nav__lang{display:flex;align-items:center;gap:2px;margin-left:10px}
  .nav__lang-btn{font-size:.68rem;font-weight:700;letter-spacing:.06em;color:rgba(255,255,255,.45);text-decoration:none;padding:3px 7px;border-radius:3px;border:1px solid rgba(255,255,255,.18);transition:all .2s}
  a.nav__lang-btn:hover,.nav__lang-btn.lang-active{color:var(--gold);border-color:var(--gold);background:rgba(245,197,24,.08)}
  .nav__lang-sep{color:rgba(255,255,255,.2);font-size:.7rem;padding:0 1px}
  .mobile-lang{display:none;align-items:center;gap:6px;padding:12px 20px;border-top:1px solid rgba(255,255,255,.1);margin-top:4px}
  .mobile-lang a,.mobile-lang span{font-size:.8rem;font-weight:700;color:rgba(255,255,255,.5);text-decoration:none;padding:4px 10px;border-radius:4px;border:1px solid rgba(255,255,255,.15)}
  .mobile-lang a:hover,.mobile-lang .lang-active{color:var(--gold);border-color:var(--gold)}
  @media(max-width:768px){.nav__lang{display:none}.mobile-lang{display:flex}}
</style>"""

# ── German nav templates ──────────────────────────────────────────────────────
def de_nav(prefix='', slug='index.html'):
    """Generate clean German nav for de/ pages. prefix='' for root, '../' for blog."""
    blog_link = 'blog/index.html' if prefix == '' else 'index.html'
    en_href = f'../{slug}' if prefix == '' else f'../../blog/{slug}'
    return f"""<nav class="nav" id="nav">
  <div class="nav__inner">
    <a href="{prefix}index.html" class="nav__logo">
      <img src="{prefix}../images/logo.webp" alt="SunWave Switzerland" style="height:44px;display:block;border-radius:6px;">
    </a>
    <div class="nav__links">
      <a href="{prefix}product.html">Das Paneel</a>
      <a href="{prefix}research.html">Forschung</a>
      <div class="nav__drop">
        <button class="nav__drop-btn">Für &#9662;</button>
        <div class="nav__drop-menu" id="nav-drop-menu">
          <a href="{prefix}for-solar.html">Solar-Installateure</a>
          <a href="{prefix}for-hotels.html">Hotels &amp; Gastronomie</a>
          <a href="{prefix}for-homes.html">Schweizer Haushalte</a>
          <a href="{prefix}for-offices.html">Büro &amp; Gewerbe</a>
        </div>
      </div>
      <a href="{prefix}index.html#calculator">Rechner</a>
      <a href="{prefix}{blog_link}">Blog</a>
      <a href="{prefix}contact.html">Kontakt</a>
    </div>
    <div class="nav__right">
      <a href="{prefix}product.html" class="nav__order-btn">Jetzt bestellen</a>
      <div class="nav__lang">
        <a href="{en_href}" class="nav__lang-btn">EN</a>
        <span class="nav__lang-sep">|</span>
        <span class="nav__lang-btn lang-active">DE</span>
      </div>
      <button class="nav__hamburger" id="nav-hamburger" aria-label="Menu">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
  <div class="nav__mobile" id="nav-mobile">
    <a href="{prefix}product.html">Das Paneel</a>
    <a href="{prefix}research.html">Forschung</a>
    <a href="{prefix}for-solar.html">Solar-Installateure</a>
    <a href="{prefix}for-hotels.html">Hotels &amp; Gastronomie</a>
    <a href="{prefix}for-homes.html">Schweizer Haushalte</a>
    <a href="{prefix}for-offices.html">Büro &amp; Gewerbe</a>
    <a href="{prefix}index.html#calculator">Rechner</a>
    <a href="{prefix}{blog_link}">Blog</a>
    <a href="{prefix}contact.html">Kontakt</a>
    <a href="{prefix}product.html" class="nav__mobile-order">Jetzt bestellen</a>
  </div>
  <div class="mobile-lang">
    <a href="{en_href}">EN</a>
    <span class="lang-active">DE</span>
  </div>
</nav>"""

def en_nav_switcher(slug, is_blog=False):
    """Desktop + mobile lang switcher HTML for English pages."""
    de_href = f'de/{slug}' if not is_blog else f'../de/blog/{slug}'
    return (
        f'<div class="nav__lang">\n        <span class="nav__lang-btn lang-active">EN</span>\n        <span class="nav__lang-sep">|</span>\n        <a href="{de_href}" class="nav__lang-btn">DE</a>\n      </div>',
        f'<div class="mobile-lang">\n    <span class="lang-active">EN</span>\n    <a href="{de_href}">DE</a>\n  </div>'
    )

def clean_switcher_css(content):
    """Remove ALL existing switcher style blocks, return cleaned content."""
    content = re.sub(r'\s*<style>\s*\.nav__lang\{.*?</style>', '', content, flags=re.DOTALL)
    content = re.sub(r'\s*<style>\s*\.nav__lang\s*\{.*?</style>', '', content, flags=re.DOTALL)
    return content

def clean_switcher_html(content):
    """Remove ALL existing switcher divs."""
    content = re.sub(r'\s*<div class="nav__lang">.*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'\s*<div class="mobile-lang">.*?</div>', '', content, flags=re.DOTALL)
    return content

# ── Fix German pages ──────────────────────────────────────────────────────────
print('=== Fixing German pages ===')
de_root = [(f.replace('\\','/'), False) for f in glob.glob('de/*.html')]
de_blog  = [(f.replace('\\','/'), True)  for f in glob.glob('de/blog/*.html')]

for path, is_blog in de_root + de_blog:
    slug = path.split('/')[-1]
    prefix = '' if not is_blog else '../'

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove all switcher CSS and HTML
    content = clean_switcher_css(content)
    content = clean_switcher_html(content)

    # 2. Replace entire nav block with clean German nav
    new_nav = de_nav(prefix=prefix, slug=slug)
    content = re.sub(r'<nav class="nav"[^>]*>.*?</nav>', new_nav, content, flags=re.DOTALL)

    # 3. Inject correct switcher CSS
    content = content.replace('</head>', SWITCHER_CSS + '\n</head>', 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  Fixed DE: {path}')

# ── Fix English pages ─────────────────────────────────────────────────────────
print()
print('=== Fixing English pages ===')
en_root = [(f.replace('\\','/'), False) for f in glob.glob('*.html')]
en_blog  = [(f.replace('\\','/'), True)  for f in glob.glob('blog/*.html')]

for path, is_blog in en_root + en_blog:
    slug = path.split('/')[-1]
    if path.startswith('de/'): continue

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove all old switcher CSS and HTML
    content = clean_switcher_css(content)
    content = clean_switcher_html(content)

    # 2. Build correct switcher
    desktop_sw, mobile_sw = en_nav_switcher(slug, is_blog)

    # 3. Inject desktop switcher after Order Now button in nav__right
    content = re.sub(
        r'(class="nav__order-btn">[^<]+</a>)',
        f'\\1\n      {desktop_sw}',
        content,
        count=1
    )

    # 4. Inject mobile switcher just before </nav>
    content = re.sub(r'(\s*)</nav>', f'\\1  {mobile_sw}\n</nav>', content, count=1)

    # 5. Inject CSS once before </head>
    content = content.replace('</head>', SWITCHER_CSS + '\n</head>', 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  Fixed EN: {path}')

print()
print('All done. Verifying...')

# ── Quick verification ────────────────────────────────────────────────────────
with open('de/index.html','r',encoding='utf-8') as f: c=f.read()
nav = re.search(r'<nav class="nav".*?</nav>', c, re.DOTALL)
nav_text = re.sub(r'<[^>]+>','|',nav.group()) if nav else ''
nav_text = [t.strip() for t in nav_text.split('|') if t.strip() and len(t.strip()) > 1]
print('DE nav items:', nav_text[:12])

styles = re.findall(r'<style>', c)
print(f'DE style blocks: {len(styles)}')

with open('index.html','r',encoding='utf-8') as f: ce=f.read()
styles_en = re.findall(r'<style>', ce)
print(f'EN style blocks: {len(styles_en)}')

# Check Forschung is correct
print('Forschung correct:', 'Foderschung' not in c and 'Forschung' in c)
