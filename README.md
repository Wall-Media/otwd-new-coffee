# Off The Wall Digital, "The Window"

Marketing site for Off The Wall Digital (Petro Wall, Ramsgate, Kent), a trading name of
Wall Media Ltd. Self-contained static HTML, no build step, no dependencies to install.
Serve the folder over HTTP and it works.

## Files

| File | What it is |
| --- | --- |
| `index.html` | The whole marketing site: hero, outcomes, "Is this you", front of house / back of house, four case studies, the week graphic, About, and the contact section. |
| `blog/index.html` | Notes listing page. Short thoughts on running a small business without drowning in your own admin. |
| `blog/*.html` | Individual note pages. Each one is a standalone HTML file with its own header, footer, and the full legal footer. |
| `coffee.html` | The booking page. Every coffee call to action links here. Holds the LeadConnector calendar, which sizes itself, so it needs a full page rather than a modal to grow into. |
| `thanks.html` | Post-booking thank you page. Set this as the calendar's redirect URL in GoHighLevel. Marked `noindex`. |
| `privacy.html` | Combined privacy notice and terms of use, tabbed, deep linkable at `#privacy` and `#terms`. |
| `blog/` | Notes section. Static HTML blog with categories and tags. See Blog structure below. |
| `404.html` | Branded "page not found" page. Vercel serves it automatically for any missing URL. |
| `robots.txt` | Lets every crawler in and points at the sitemap. |
| `rss.xml` | RSS feed for published notes. |
| `sitemap.xml` | Site sitemap. |

## Opening it

Serve it over HTTP. Double clicking a file will show the words but not the images, because
images use root-absolute paths (`/assets/...`), and the calendar and enquiry form need a real
origin too:

```
python3 -m http.server 8000
# then open http://localhost:8000/
```

## Deployment

All files sit at the repo root, so any static host works. On GitHub Pages, serve from
`main` / root and `index.html` is picked up automatically. Vercel uses `vercel.json` with `cleanUrls: true` so paths without `.html` resolve.

Booking happens on its own page, `coffee.html` (served at `/coffee`). Every coffee call to
action is a plain link to it. Nothing needs editing for deployment.

Set `thanks.html` as the calendar's redirect URL in GoHighLevel so people land somewhere
of ours after booking rather than on a LeadConnector confirmation screen.

## Integrations

**Booking calendar.** LeadConnector widget `dqB0NblntdSZnLlpSFEz` ("Coffee with Petro",
30 min), resized by `https://link.msgsndr.com/js/form_embed.js`.

The widget is embedded in `coffee.html`. The calendar ID is the `CAL_ID` constant in that
page's script, repeated only in the `<noscript>` link; change both to switch calendar. With JavaScript off, a `<noscript>` link opens
the calendar directly instead.

`form_embed.js` parks the iframe off screen to measure its content height and does not
restore it, so `.cal` reclaims `position`, `opacity`, `visibility` and `pointer-events`
with `!important` while leaving the height the script calculates alone. Do not remove
those overrides or the calendar will load invisibly.

There is a nine second safety net that redirects to the calendar if the widget never
renders at all (the iframe is still under 260px tall after nine seconds).

**Enquiry form.** Posts JSON to a GoHighLevel inbound webhook. The URL is the
`ENQUIRY_WEBHOOK` constant near the top of the script block in `index.html`. Payload:

```json
{
  "name": "...",
  "first_name": "...",
  "last_name": "...",
  "email": "...",
  "phone": "...",
  "message": "...",
  "source": "offthewalldigital.com contact form",
  "page": "...",
  "submitted_at": "ISO 8601"
}
```

All four visible fields are required. If the POST fails, the visitor is offered a mailto
pre-filled with everything they typed, so an enquiry is never lost silently. Setting
`ENQUIRY_WEBHOOK` back to an empty string switches the form to that email hand-off.

## Conventions worth keeping

- **UK English throughout.**
- **No em dashes or en dashes anywhere**, including meta tags. Commas, full stops or a
  rewrite instead.
- **The term "AI" never appears** in customer-facing copy. Say automation, systems or
  processes.
- **No urgency, scarcity or countdowns.** No invented statistics or testimonials.
- **Petro's former employers are never named**; her background stays generalised.
- **Email addresses never appear in the source.** The address is assembled in JavaScript
  at runtime in `index.html` only, and used as the fallback when the enquiry form cannot
  send. Other pages link to `./#enquiry` rather than carry their own copy. There is no
  phone number on the site.
- **Cream palette only, never dark, and no light/dark toggle.** Tokens live in `assets/css/site.css`.
- **SVG line art, never emoji.**
- Calls to action are coffee invitations that warm up down the page: "Fancy a coffee?",
  "Start with a coffee", "That sounds like me", "Tell me about yours", "Put the kettle on".

## Images

Every image lives in the repo. Nothing is hotlinked from another host.

- `assets/img/` holds the marketing images: `hero-shut.jpg` and `hero-open.jpg` (the hero
  before and after slider), `case-mamas.jpg`, `case-ocean.jpg`, `case-boiler.jpg`,
  `case-ignite.jpg` (case study screenshots) and `share-shopfront.jpg` (social share image).
- `assets/blog/` holds Petro's portrait `petro.jpg` (used on the home page and on every
  note's author card) and each note's featured image.

Keep new images around 1600px wide at most and compressed, since there is no build step.

## Build script

The shared parts of every page (fonts, tab icon, logo mark, headers, footers, legal line) and
the whole Notes index (post cards, category and tag pages, `rss.xml`, `sitemap.xml`) are kept
in step by `build.py`. Python 3, nothing to install. After any edit:

```
python3 build.py
```

and commit what it changed. `python3 build.py --check` changes nothing and fails if anything
is out of date. Turn on the pre-commit check once per clone:

```
git config core.hooksPath .githooks
```

Shared regions sit between `<!-- block:name -->` and `<!-- /block:name -->` markers. Edit the
matching file in `partials/`, never the region in the page. SITE.md has the details and the
recipes.

## Blog structure

The Notes section (`/blog`) is static HTML. Posts are hand-written HTML files in `blog/`;
everything that lists them is generated.

**Adding a note:** copy an existing post to `blog/<slug>.html`, add its image at
`assets/blog/<slug>.png`, set its details (the JSON-LD headline, description, dates, category,
tags and image, plus the matching hero), and run `python3 build.py`. The build adds the card
everywhere, creates any new category or tag page, and updates RSS and the sitemap. A new
category needs its wording in `blog/categories.json` first; the build tells you if it is
missing.

**Author card:** every note ends with the same Petro call-out (`aside.author-card`), photo at `assets/blog/petro.jpg`. Copy it from an existing post. Do not rewrite per note.

**Draft vs published:** a post with `noindex,nofollow` is a draft. It is listed with a Draft
label but left out of RSS and the sitemap. `index,follow` publishes it.

## Still outstanding

- Four client testimonial quotes.
- One real result per case study (hours saved, or the client's own words). The case studies
  are written as "Before" and "Now" with a deliberate gap where a result belongs.

## Legal

Off The Wall Digital is a trading name of Wall Media Ltd, registered in England and Wales,
company number 15045668. Registered office: Longfrey Cottage, Dorking Road, Chilworth,
Surrey, GU4 8RH.
