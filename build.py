#!/usr/bin/env python3
"""Keeps the shared parts of this static site in sync. Python 3 standard library only.

    python3 build.py           update every file in place
    python3 build.py --check   change nothing; exit 1 and list the files that are out of date

What it does
  1. Blocks. A page marks a shared region like this:

         <!-- block:notes-header back_href="/blog" back_label="Notes" -->
         ...anything here is replaced on every build...
         <!-- /block:notes-header -->

     If partials/<name>.html exists, the region becomes that partial with the attributes
     filled in ({{back_href}}). Partials can pull in other partials inline with
     {{> mark size="34"}}. Otherwise <name> is one of the generators below.
     Everything outside the markers is left exactly as it is.

  2. Notes. Each post in blog/ is read for its details (JSON-LD, robots, read time, hero
     image) and the build writes the post cards, the category and tag pages, rss.xml and
     sitemap.xml from them.

The pages stay complete HTML, so the site still deploys with no build step on Vercel.
Run this after editing, and commit what it changes. SITE.md has the full recipes.
"""
import datetime
import email.utils
import html
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://www.offthewalldigital.com'
PARTIALS = os.path.join(ROOT, 'partials')

BLOCK_RE = re.compile(r'<!-- block:([\w-]+)((?:\s+[\w-]+="[^"]*")*)\s*-->(.*?)<!-- /block:\1 -->', re.S)
INCLUDE_RE = re.compile(r'\{\{>\s*([\w-]+)((?:\s+[\w-]+="[^"]*")*)\s*\}\}')
PARAM_RE = re.compile(r'\{\{\s*([\w-]+)\s*\}\}')
ATTR_RE = re.compile(r'([\w-]+)="([^"]*)"')

# Pages that carry blocks. Tag and category pages are generated whole, so are not listed.
PAGES = ['index.html', 'coffee.html', 'thanks.html', 'privacy.html', '404.html', 'blog/index.html']

# Sitemap entries for pages that are not Notes: (path on disk, URL path, changefreq, priority)
STATIC_URLS = [
    ('index.html', '/', 'monthly', '1.0'),
    ('coffee.html', '/coffee', 'monthly', '0.9'),
    ('privacy.html', '/privacy', 'yearly', '0.3'),
]


class BuildError(Exception):
    pass


def read(rel):
    with open(os.path.join(ROOT, rel), encoding='utf-8') as f:
        return f.read()


def slugify(name):
    return re.sub(r'[^a-z0-9-]', '', re.sub(r'\s+', '-', name.strip().lower()))


def attrs(text):
    return dict(ATTR_RE.findall(text or ''))


# ---------------------------------------------------------------- partials

def render_partial(name, params, stack=()):
    if name in stack:
        raise BuildError('partial %s includes itself' % name)
    path = os.path.join(PARTIALS, name + '.html')
    if not os.path.exists(path):
        raise BuildError('no partial named %s (looked for partials/%s.html)' % (name, name))
    with open(path, encoding='utf-8') as f:
        text = f.read().rstrip('\n')
    text = INCLUDE_RE.sub(lambda m: render_partial(m.group(1), attrs(m.group(2)), stack + (name,)), text)
    return fill(text, params, 'partials/%s.html' % name)


def fill(text, params, where):
    def sub(m):
        key = m.group(1)
        if key not in params:
            raise BuildError('%s needs a value for {{%s}}' % (where, key))
        return params[key]
    return PARAM_RE.sub(sub, text)


# ---------------------------------------------------------------- notes

def post_files():
    out = []
    for fn in sorted(os.listdir(os.path.join(ROOT, 'blog'))):
        if fn.endswith('.html') and fn != 'index.html':
            out.append('blog/' + fn)
    return out


def strip_tags(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s)).strip()


def load_post(rel):
    src = read(rel)
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', src, re.S)
    if not m:
        raise BuildError('%s has no JSON-LD block' % rel)
    ld = json.loads(m.group(1))
    need = ['headline', 'description', 'datePublished', 'articleSection', 'keywords', 'image']
    missing = [k for k in need if not ld.get(k)]
    if missing:
        raise BuildError('%s JSON-LD is missing %s' % (rel, ', '.join(missing)))
    robots = re.search(r'<meta name="robots" content="([^"]*)"', src)
    read_time = re.search(r'<span class="meta__read">(.*?)</span>', src, re.S)
    hero = re.search(r'<img\b[^>]*class="post-hero-img"[^>]*>', src)
    alt = re.search(r'alt="([^"]*)"', hero.group(0)) if hero else None
    excerpt = re.search(r'<meta name="excerpt" content="([^"]*)"', src)
    if excerpt:
        blurb = html.unescape(excerpt.group(1))
    else:
        first_p = re.search(r'<article>\s*<p>(.*?)</p>', src, re.S)
        if not first_p:
            raise BuildError('%s: no <meta name="excerpt"> and no first <p> in <article>' % rel)
        blurb = strip_tags(first_p.group(1))
    if not read_time:
        raise BuildError('%s has no <span class="meta__read">' % rel)
    if not alt:
        raise BuildError('%s has no <img class="post-hero-img" alt="..."> for the card thumbnail' % rel)
    published = datetime.datetime.fromisoformat(ld['datePublished'])
    check_post(rel, src, ld, published)
    return {
        'file': rel,
        'slug': os.path.basename(rel)[:-5],
        'title': ld['headline'],
        'description': ld['description'],
        'published': published,
        'category': ld['articleSection'],
        'tags': list(ld['keywords']),
        'image': ld['image'].replace(SITE, ''),
        'thumb': thumb_path(ld['image']),
        'alt': html.unescape(alt.group(1)),
        'read': strip_tags(read_time.group(1)),
        'blurb': blurb,
        'draft': bool(robots and 'noindex' in robots.group(1)),
    }


def check_post(rel, src, ld, published):
    """The post's visible header is hand-written; stop if it disagrees with its JSON-LD."""
    slug = os.path.basename(rel)[:-5]
    problems = []

    def first(pattern):
        m = re.search(pattern, src, re.S)
        return m.groups() if m else None

    h1 = first(r'<h1>(.*?)</h1>')
    if not h1 or strip_tags(h1[0]) != ld['headline']:
        problems.append('<h1> should be "%s"' % ld['headline'])
    cat = first(r'<a class="meta__cat" href="([^"]*)">(.*?)</a>')
    want_cat = '/blog/category/' + slugify(ld['articleSection'])
    if not cat or cat[0] != want_cat or strip_tags(cat[1]) != ld['articleSection']:
        problems.append('the category link should be <a class="meta__cat" href="%s">%s</a>' % (want_cat, ld['articleSection']))
    date = first(r'<span class="meta__date">(.*?)</span>')
    want_date = published.strftime('%-d %B %Y')
    if not date or strip_tags(date[0]) != want_date:
        problems.append('the date should read "%s" (from datePublished)' % want_date)
    tags_div = first(r'<div class="tags">(.*?)</div>')
    have = re.findall(r'<a class="tag" href="/blog/tag/([^"]*)">#([^<]*)</a>', tags_div[0]) if tags_div else []
    want = [slugify(k) for k in ld['keywords']]
    if [h for h, _ in have] != want or any(h != label for h, label in have):
        problems.append('the tag links should be, in order: %s' % ', '.join(
            '<a class="tag" href="/blog/tag/%s">#%s</a>' % (t, t) for t in want))
    for label, pattern in (('canonical', r'<link rel="canonical" href="([^"]*)"'),
                           ('og:url', r'<meta property="og:url" content="([^"]*)"')):
        got = first(pattern)
        if not got or got[0] != '%s/blog/%s' % (SITE, slug):
            problems.append('%s should be %s/blog/%s' % (label, SITE, slug))
    for label, pattern in (('og:image', r'<meta property="og:image" content="([^"]*)"'),
                           ('twitter:image', r'<meta name="twitter:image" content="([^"]*)"')):
        got = first(pattern)
        if not got or got[0] != ld['image']:
            problems.append('%s should match the JSON-LD image, %s' % (label, ld['image']))
    hero = first(r'<img\b[^>]*class="post-hero-img"[^>]*src="([^"]*)"')
    if not hero or hero[0] != ld['image'].replace(SITE, ''):
        problems.append('the hero image src should be %s' % ld['image'].replace(SITE, ''))
    if not os.path.exists(os.path.join(ROOT, ld['image'].replace(SITE, '').lstrip('/'))):
        problems.append('the image %s does not exist' % ld['image'].replace(SITE, ''))
    if problems:
        raise BuildError('%s does not match its own JSON-LD:\n  - %s' % (rel, '\n  - '.join(problems)))


def thumb_path(image_url):
    """Cards use a small copy of the post image: /assets/blog/<name>-thumb.jpg."""
    return os.path.splitext(image_url.replace(SITE, ''))[0] + '-thumb.jpg'


THUMB_W, THUMB_H, THUMB_QUALITY = 720, 480, 68


def ensure_thumb(p, check):
    """Create a missing card thumbnail with macOS sips: centre crop to 720x480."""
    dest = os.path.join(ROOT, p['thumb'].lstrip('/'))
    if os.path.exists(dest):
        return False
    how = 'Run python3 build.py on a Mac to create it, or save a %dx%d JPEG there yourself.' % (THUMB_W, THUMB_H)
    if check or not shutil.which('sips'):
        raise BuildError('%s needs a card thumbnail at %s. %s' % (p['file'], p['thumb'], how))
    src = os.path.join(ROOT, p['image'].lstrip('/'))
    dims = subprocess.run(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', src],
                          capture_output=True, text=True, check=True).stdout
    w, h = [int(x) for x in re.findall(r'pixel\w+: (\d+)', dims)]
    fit = ['--resampleHeight', str(THUMB_H)] if w * THUMB_H >= h * THUMB_W else ['--resampleWidth', str(THUMB_W)]
    run = lambda *a: subprocess.run(['sips'] + list(a), capture_output=True, check=True)
    run('-s', 'format', 'jpeg', *fit, src, '--out', dest)
    run('--cropToHeightWidth', str(THUMB_H), str(THUMB_W), '-s', 'formatOptions', str(THUMB_QUALITY), dest)
    return True


def load_posts():
    posts = [load_post(f) for f in post_files()]
    return sorted(posts, key=lambda p: p['published'], reverse=True)


def esc(s):
    """Escape for an attribute value."""
    return html.escape(s, quote=True)


def text(s):
    """Escape for text between tags, where quotes can stay as they are."""
    return html.escape(s, quote=False)


def card(p):
    tags = '\n'.join('          <span class="post-card__tag">%s</span>' % text(t) for t in p['tags'])
    draft = '\n          <span class="post-card__draft">Draft</span>' if p['draft'] else ''
    return render_partial('post-card', {
        'slug': p['slug'], 'thumb': esc(p['thumb']), 'alt': esc(p['alt']),
        'category': text(p['category']), 'date': p['published'].strftime('%-d %B %Y'),
        'read': text(p['read']), 'title': text(p['title']), 'blurb': text(p['blurb']),
        'tags': tags, 'draft': draft,
    })


def gen_post_cards(params, ctx):
    posts = ctx['posts']
    if 'category' in params:
        posts = [p for p in posts if slugify(p['category']) == params['category']]
    if 'tag' in params:
        posts = [p for p in posts if params['tag'] in [slugify(t) for t in p['tags']]]
    return '\n'.join(card(p) for p in posts)


def gen_category_chips(params, ctx):
    active = params.get('active', '')
    chips = [('', '/blog', 'All notes')]
    chips += [(slug, '/blog/category/' + slug, ctx['categories'][slug]['name']) for slug in ctx['category_order']]
    return '\n'.join('      <a class="cat-chip%s" href="%s">%s</a>' % (' active' if slug == active else '', href, text(name))
                     for slug, href, name in chips)


GENERATORS = {'post-cards': gen_post_cards, 'category-chips': gen_category_chips}


# ---------------------------------------------------------------- blocks

def render_block(name, params, ctx, where):
    if os.path.exists(os.path.join(PARTIALS, name + '.html')):
        return render_partial(name, params)
    if name in GENERATORS:
        return GENERATORS[name](params, ctx)
    raise BuildError('%s: unknown block %s (no partials/%s.html and no generator)' % (where, name, name))


def apply_blocks(text, ctx, where):
    def sub(m):
        name, raw_attrs, old = m.group(1), m.group(2), m.group(3)
        new = render_block(name, attrs(raw_attrs), ctx, where)
        if '\n' in new or old.startswith('\n'):
            new = '\n' + new + '\n'
        return '<!-- block:%s%s -->%s<!-- /block:%s -->' % (name, raw_attrs, new, name)
    return BLOCK_RE.sub(sub, text)


# ---------------------------------------------------------------- whole generated pages

GENERATED_NOTE = '<!-- Generated by build.py from partials/pages/%s.html. Edit that template, or blog/categories.json, not this file. -->\n'


def page_from_template(kind, params, ctx, where):
    text = read('partials/pages/%s.html' % kind)
    text = fill(text, params, 'partials/pages/%s.html' % kind)
    text = text.replace('<!DOCTYPE html>\n', '<!DOCTYPE html>\n' + GENERATED_NOTE % kind, 1)
    return apply_blocks(text, ctx, where)


# ---------------------------------------------------------------- git dates

def lastmod(rel, pending):
    """Last commit date of a file, or today if it is about to change or has uncommitted edits."""
    today = datetime.date.today().isoformat()
    if rel in pending:
        return today
    try:
        dirty = subprocess.run(['git', 'status', '--porcelain', '--', rel], cwd=ROOT,
                               capture_output=True, text=True, check=True).stdout.strip()
        if dirty:
            return today
        date = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', rel], cwd=ROOT,
                              capture_output=True, text=True, check=True).stdout.strip()
        return date or today
    except (OSError, subprocess.CalledProcessError):
        return today


# ---------------------------------------------------------------- feeds

def build_rss(ctx):
    items = []
    for p in ctx['posts']:
        if p['draft']:
            continue
        url = '%s/blog/%s' % (SITE, p['slug'])
        items.append('''    <item>
      <title>%s</title>
      <link>%s</link>
      <guid>%s</guid>
      <pubDate>%s</pubDate>
      <description>%s</description>
      <category>%s</category>
    </item>''' % (esc(p['title']), url, url, email.utils.format_datetime(p['published']),
                  esc(p['description']), esc(p['category'])))
    return '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Off The Wall Digital · Notes</title>
    <link>%s/blog</link>
    <description>Notes from Petro Wall. How you show up online, how the work gets done, and the small shifts that make room for a life again.</description>
    <language>en-GB</language>
    <atom:link href="%s/rss.xml" rel="self" type="application/rss+xml"/>
%s
  </channel>
</rss>
''' % (SITE, SITE, '\n'.join(items))


def build_sitemap(ctx, pending):
    entries = list(STATIC_URLS)
    entries.append(('blog/index.html', '/blog', 'weekly', '0.8'))
    for slug in ctx['category_order']:
        entries.append(('blog/category/%s.html' % slug, '/blog/category/' + slug, 'weekly', '0.6'))
    for slug in ctx['tag_order']:
        entries.append(('blog/tag/%s.html' % slug, '/blog/tag/' + slug, 'weekly', '0.5'))
    for p in ctx['posts']:
        if not p['draft']:
            entries.append((p['file'], '/blog/' + p['slug'], 'monthly', '0.7'))
    urls = ['''  <url>
    <loc>%s%s</loc>
    <lastmod>%s</lastmod>
    <changefreq>%s</changefreq>
    <priority>%s</priority>
  </url>''' % (SITE, url, lastmod(rel, pending), freq, prio) for rel, url, freq, prio in entries]
    return '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
%s
</urlset>
''' % '\n'.join(urls)


# ---------------------------------------------------------------- main

def build(check=False):
    posts = load_posts()
    for p in posts:
        if ensure_thumb(p, check):
            print('created ' + p['thumb'])
    cats_file = json.loads(read('blog/categories.json'))
    categories, tags = {}, {}
    for p in posts:
        slug = slugify(p['category'])
        if slug not in cats_file:
            raise BuildError('%s uses category "%s", which is not in blog/categories.json. Add it there with '
                             'a name, heading, intro and description, then build again.' % (p['file'], p['category']))
        categories[slug] = dict(cats_file[slug], slug=slug)
        for t in p['tags']:
            tags.setdefault(slugify(t), t)
    ctx = {
        'posts': posts,
        'categories': categories,
        'category_order': sorted(categories, key=lambda s: categories[s]['name'].lower()),
        'tag_order': sorted(tags),
    }

    outputs = {}
    for rel in PAGES:
        outputs[rel] = apply_blocks(read(rel), ctx, rel)
    for p in posts:
        outputs[p['file']] = apply_blocks(read(p['file']), ctx, p['file'])
    for slug in ctx['category_order']:
        c = categories[slug]
        outputs['blog/category/%s.html' % slug] = page_from_template('category', {
            'slug': slug, 'name': esc(c['name']), 'heading': esc(c['heading']),
            'intro': esc(c['intro']), 'description': esc(c['description'])}, ctx, 'category ' + slug)
    for slug in ctx['tag_order']:
        outputs['blog/tag/%s.html' % slug] = page_from_template('tag', {
            'slug': slug, 'name': esc(tags[slug])}, ctx, 'tag ' + slug)
    outputs['rss.xml'] = build_rss(ctx)

    pending = set()
    for rel, text in outputs.items():
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path) or read(rel) != text:
            pending.add(rel)
    outputs['sitemap.xml'] = build_sitemap(ctx, pending)
    if read('sitemap.xml') != outputs['sitemap.xml']:
        pending.add('sitemap.xml')

    orphans = []
    for kind, keep in (('category', ctx['category_order']), ('tag', ctx['tag_order'])):
        folder = os.path.join(ROOT, 'blog', kind)
        for fn in sorted(os.listdir(folder)) if os.path.isdir(folder) else []:
            if fn.endswith('.html') and fn[:-5] not in keep:
                orphans.append('blog/%s/%s' % (kind, fn))
    return outputs, sorted(pending), orphans


def main():
    check = '--check' in sys.argv[1:]
    try:
        outputs, pending, orphans = build(check)
    except (BuildError, ValueError, KeyError, subprocess.CalledProcessError) as e:
        print('build.py: %s' % e, file=sys.stderr)
        return 2
    for rel in orphans:
        print('note: %s is no longer used by any post. Delete it if that is intended.' % rel)
    if check:
        if pending:
            print('Out of date (run python3 build.py):')
            for rel in pending:
                print('  ' + rel)
            return 1
        print('Everything is up to date.')
        return 0
    for rel in pending:
        path = os.path.join(ROOT, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(outputs[rel])
        print('updated ' + rel)
    if not pending:
        print('Everything is up to date.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
