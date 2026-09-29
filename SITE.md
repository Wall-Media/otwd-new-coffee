# SITE.md — Off The Wall Digital

Read this before changing anything on this site.

This file exists because the site has no build step, so the same thing (headers, footers, legal
text, head tags) lives in several places. Shared CSS now lives in `assets/css/`, but each page
still carries its own page specific `<style>`. This is the map. It was written from a full read of every file
on 4 September 2026 and re-checked against the code on 29 September 2026.

---

## Rule zero

Every count in this file is a snapshot, not a promise. Before changing anything that appears
in more than one place, SEARCH the repo for the current occurrences and update every one you
find. If your search returns a different number than this file says, trust your search, make
the change, and flag the difference so this file gets corrected.

Two specific traps that a single find-and-replace will miss, both explained below: the booking
widget ID is embedded inside an element ID as well as in URLs, and the email address is
assembled from split arrays, so searching for the address itself finds nothing.

---

## Deployment and previews

Hosted on **Vercel**, serving this repo. Confirmed from the live response headers on
4 September 2026: the apex redirects 308 to www, and both are served by Vercel.

Pushing to `main` deploys straight to production. **On this site that is the agreed way of
working**, decided by Colin on 4 September 2026. Commit to main, let it go live, then show
Petro. Do not open branches and pull requests for ordinary changes here.

`vercel.json` sets `cleanUrls: true` and `trailingSlash: false` so canonical paths like `/blog/your-website-should-feel-like-meeting-you` and `/coffee` resolve without the `.html` suffix. It also carries a permanent redirect from the first post's old slug (`/blog/why-your-website-should-feel-like-you`). Keep that file. Do not remove it to "simplify" the deploy.

### Why this site works differently from a client site

Everywhere else the rule is: change on a preview, show it, then go live. Here it is: change
it, then show it. Two reasons that is acceptable on this site specifically.

Petro owns this site. She is not a client waiting to be reassured, she is the person who would
have approved it anyway, and a wrong change costs the business nothing but a minute.

And a preview link would not work here in any case. Deployment Protection is switched on for
this Vercel team, verified on 4 September 2026 by opening a real preview URL from outside the
account: it returns Vercel's own login page rather than the site. Anyone without a Vercel
account sees a login screen and assumes the site is broken.

**So the rule stands everywhere else: never send a raw Vercel preview URL to a client.** If a
paying client is ever put on this workflow, Deployment Protection has to be dealt with first,
either by turning it off for previews or by enabling Protection Bypass for Automation, which
produces a secret that can be appended to a preview URL so someone without a Vercel account
can open it. The second is better, because previews stay closed to anything that has not been
handed the link.

### What still has to happen on every change here

Going live first does not mean going quiet. After each change:

- screenshot the live page on desktop and on a phone width, and post both to Petro
- say plainly what changed and where
- if she does not like it, revert immediately. It is one commit, it takes seconds, and it is
  never charged or counted

The safety rules below do not relax because there is no preview. The stop list still stops.

---

## Pages

| File | Serves | Notes |
|---|---|---|
| index.html | / | The whole marketing site, about 89,500 bytes and 1,640 lines. Readable, not minified. Holds the enquiry form. |
| coffee.html | /coffee | The booking page. Every coffee call to action links here. Holds the GoHighLevel calendar embed, which needs a full page to grow into. |
| privacy.html | /privacy | Privacy and terms, tabbed. |
| thanks.html | /thanks | Post-booking landing page. Carries `noindex,nofollow` deliberately, set as the calendar's redirect URL in GoHighLevel. Do not remove the robots tag. |
| blog/index.html | /blog | Notes listing page with category filter chips and rich post cards. Canonical URL is /blog (no trailing slash). |
| blog/your-website-should-feel-like-meeting-you.html | /blog/your-website-should-feel-like-meeting-you | First published note, and the template for every new note. |
| blog/category/websites.html | /blog/category/websites | Category listing for Websites notes. |
| blog/tag/*.html | /blog/tag/* | Tag listing pages (websites, brand-voice, small-business). |
| 404.html | any missing URL | Vercel serves it automatically with a 404 status. `noindex`. Uses root-absolute links (`/`, `/blog`, `/coffee`) because it can appear at any depth. |
| robots.txt | /robots.txt | Allows everything and points crawlers at the sitemap. Do not disallow thanks.html here: crawlers need to fetch it to see its `noindex`. |
| rss.xml | /rss.xml | RSS feed for published notes. Excludes drafts. |
| sitemap.xml | /sitemap.xml | Site sitemap including blog pages. Draft posts omitted. |
| README.md | — | Petro's conventions and copy rules. Read it alongside this file. |

### Images

Every image is in the repo. Nothing is loaded from pub.hyperagent.com any more (moved on
29 September 2026). Reference images with root-absolute paths (`/assets/...`), and use the
full `https://www.offthewalldigital.com/assets/...` URL in og:image, twitter:image and JSON-LD.

| File | Used by |
|---|---|
| assets/img/hero-shut.jpg | index.html hero, "before" side of the slider |
| assets/img/hero-open.jpg | index.html hero, "after" side of the slider (resized to 1600px to match) |
| assets/img/case-mamas.jpg, case-ocean.jpg, case-boiler.jpg, case-ignite.jpg | index.html case study cards |
| assets/img/share-shopfront.jpg | the default social share image: og:image and twitter:image on every page except notes with their own hero image, and 404.html |
| assets/blog/petro.jpg | index.html About portrait, and the author card on every note |
| assets/blog/<slug>.png | each note's hero image and listing thumbnail |

---

## The design system

Defined as CSS custom properties in the `:root` block of `assets/css/site.css`, the one place
they live. Use these tokens, never raw hex values, and never introduce a colour that is not here.

```css
--cream:#fdf8ec; --bone:#f6efdf; --sage:#e9ecda; --tealwash:#e3efec; --coralwash:#fbeae7;
--ink:#2f3327; --head:#2a2e21; --muted:#6d7360;
--green:#6f7d45; --green-deep:#5c6939;
--teal:#2ea89a; --teal-dark:#237a70;
--gold:#e3b23c; --gold-dark:#c9911f;
--coral:#e8547a; --coral-dark:#c23e63;
--link:#4d8b7f;
--pane-border:rgba(47,51,39,.16);
--shadow-s:0 2px 8px rgba(47,51,39,.06);
--shadow-m:0 18px 40px -22px rgba(47,51,39,.34);
--shadow-l:0 42px 90px -40px rgba(47,51,39,.42);
--spring:cubic-bezier(.34,1.56,.64,1);
--maxw:1240px; --gutter:clamp(20px,5vw,64px);
```

Type is Fraunces for display, with the variable axes in use (`"SOFT" 40, "WONK" 1` as the
base, some headings running SOFT 60 to 80), and Karla for body and UI. Primary buttons use
`linear-gradient(120deg, var(--green), var(--teal))`.

**This site is cream and never dark.** There is no dark mode and none should be added.

### Shared stylesheets

Every page links its shared CSS first, then keeps its own `<style>` block for what is unique to
it. The inline block comes after the links, so a page can still override a shared rule.

| File | Loaded by | Holds |
|---|---|---|
| assets/css/site.css | every page | the design tokens, `*{box-sizing:border-box}`, `[hidden]{display:none!important}` |
| assets/css/page.css | coffee.html, thanks.html, 404.html | the simple page shell: `header.top`, glow, eyebrow, buttons, footer |
| assets/css/notes.css | all Notes pages | Notes base type, topbar, footer, focus ring, reduced motion |
| assets/css/notes-list.css | blog index, category and tag pages | listing layout, post cards and thumbnails, category chips |

Link them with root-absolute paths (`/assets/css/site.css`), in that order, directly before the
page's `<style>`. index.html and privacy.html load only site.css; their CSS is unique to them.

The one deliberate token difference: thanks.html and 404.html set `--maxw:1000px` and
`--gutter:clamp(20px,5vw,56px)` in their own `<style>`, against site.css's 1240px and 64px.
That is intentional, do not "fix" it.

A rule belongs in a shared file only if it is character for character the same on every page
that loads that file. Same selector with different values (the Notes listing `.kicker`,
`.hero h1` and `.hero p` differ between the index/category pages and the tag pages) stays in
each page's own `<style>`. When you change a shared file, check every page that loads it.

The Google Fonts link also comes in two versions. index.html, coffee.html, thanks.html and 404.html load
Fraunces and Karla with italics; privacy.html and the Notes pages load them without. Keep each
file on the version it already uses unless the change is meant to add italics.

---

## Shared values, and everywhere they live

**Phone number.** There isn't one. It was removed from every page on 4 September 2026
(commit `798fff9`, "Drop the phone number"). Do not add one back unless Petro asks. If she
does, it needs adding to the contact section in index.html and checking against the privacy
notice, which mentions people ringing.

**Email address.** Never write `petro@wallmedia.co.uk` into the source. It is deliberately
assembled in JavaScript at runtime so scrapers cannot read it, and that protection must
survive any edit. It now lives in **index.html only**:

- `var user = ['pe','tro'], host = ['wallmedia','co','uk'];` joined with
  `String.fromCharCode(64)` for the @, and `mailto:` itself built from char codes.

The "Email me" buttons (`data-mail`) open the enquiry form rather than a bare mailto; the
assembled address is only used as the fallback when the form cannot send. Every other page
links to `./#enquiry` ("Send a message") instead of carrying its own copy of the script.
Search for `fromCharCode(64)` to confirm this is still the only place.

**Legal footer.** Appears on all ten pages and must be reproduced word for word:

> Off The Wall Digital, a trading name of Wall Media Ltd. Registered in England and Wales,
> company number 15045668. Registered office: Longfrey Cottage, Dorking Road, Chilworth,
> Surrey, GU4 8RH.

Company number and registered office also appear twice in privacy.html's own body text, in the
"Who we are" and "Who runs this site" sections. Twelve occurrences of each in total across the
repo. Do not split, shorten or paraphrase any of it.

**Header and footer markup** is duplicated on every page and the structures differ.
index.html has the full sticky nav with a mobile hamburger; every other page (coffee, thanks,
privacy and all Notes pages) has its own simpler topbar with no hamburger. Never copy
index.html's header structure into the others.

---

## Stop list: do not change these

Anything here needs a human. Say plainly that it affects how the site takes bookings or what
it is legally required to say, pass it on, and never partially do it.

**The booking page.** Booking no longer happens in a popup on index.html. Every coffee call to
action is a plain link to the booking page, `/coffee` (five in index.html: desktop nav, mobile
nav, hero, "Is this you", case studies, plus two in the first note). Do not point a coffee CTA straight at the external calendar.

**The booking widget ID.** The GoHighLevel calendar ID `dqB0NblntdSZnLlpSFEz` appears **twice,
both in coffee.html**: the `CAL_ID` constant at the top of the booking section of the script,
and the `<noscript>` fallback link, which has to repeat it because it works without JavaScript.
To change calendar, change both. Everything else is built from `CAL_ID` at runtime: the iframe's
`src`, the nine-second fallback redirect, and the iframe's element ID,
`CAL_ID + '_1788453583961'`. That element ID matters: `form_embed.js` tracks the iframe by it
to resize it, so the script sets it before setting `src`. In the markup the iframe is
`id="calFrame"` only so the script can find it. Do not rename `calFrame` without updating the
script, and do not give the iframe a `src` or `data-src` in the markup.

**The `.cal` iframe CSS overrides** in coffee.html. A stack of `!important` rules (position,
left, top, opacity, visibility, pointer-events, overflow) exists specifically to counteract
what GoHighLevel's `form_embed.js` does to the iframe after it measures height. Remove or
rewrite them and the calendar loads invisibly, which looks like nothing is wrong. The README
says the same thing.

**The `form_embed.js` URL**, the `EMBED_SRC` constant next to `CAL_ID` in coffee.html's
script.

**The enquiry webhook.** `ENQUIRY_WEBHOOK` near the top of index.html's script block, pointing
at a GoHighLevel hook. Setting it to an empty string is the documented way to fall back to a
prefilled mailto, but changing it otherwise breaks enquiry delivery silently.

**The email assembly JavaScript** in index.html. See above.

**The legal footer text**, on every page.

**`noindex,nofollow` on thanks.html.** It is the calendar's redirect target and must stay out
of search.

**Inline SVG.** The shopfront illustration is around 120 lines and the back-of-house diagram
another 80, plus browser chrome on every case study card. Copy near them can be edited; SVG
attributes must not be touched or the artwork corrupts.

**`[hidden]{display:none!important}`.** Declared in index.html, coffee.html, privacy.html and
thanks.html. Do not add the `hidden` attribute to anything you intend to be visible.

There is **no analytics, no tracking pixel and no cookie consent logic** on this site, and
none should be added without Petro asking. Nothing uses localStorage or cookies. The privacy
policy states that nothing is stored on the visitor's device, so adding tracking would make
that page untrue.

---

## Copy rules

These are Petro's, they are not negotiable, and they matter more than usual because this site
is her shopfront.

- The word **"AI" never appears**. Say automation, systems or processes.
- **No dashes as punctuation.** No em dashes, no en dashes, no double hyphens.
- **UK English**, warm, direct, personality led, no corporate speak.
- First person singular. It is Petro, not a team, and she speaks to one person rather than to
  "businesses" or "clients".
- **No urgency, scarcity, countdowns or limited spots.**
- **No invented statistics, reviews or testimonials.**
- **Never name Petro's former employers.** Her enterprise sales background stays general.
- One idea per sentence. Nothing over about 25 words in body copy, 12 in a heading. Do not
  reuse a phrase twice on the same page.
- **SVG line art only, never emoji.**
- Calls to action are coffee invitations, warming down the page: "Fancy a coffee?" in the nav,
  "Start with a coffee" in the hero, "Tell me about yours" after the case studies, "Put the
  kettle on" at the close. Never "Book a call" or "Have a chat". Because coffee implies
  meeting and Petro is Ramsgate based, the contact copy stays honest: a coffee if you are
  local, a phone call if you are not.

---

## Change recipes

**Add a phone number back.** Only if Petro asks. See Shared values above: it was removed on
4 September 2026, so there is nothing to find and replace.

**Change a colour or spacing token.** One place: `assets/css/site.css`. Remember thanks.html
and 404.html deliberately override `--maxw` and `--gutter`.

**Add or replace an image.** Save it into `assets/img/` (or `assets/blog/` for Notes), never
hotlink it from another host. Keep it around 1600px wide at most and compress it; the site has
no build step to do that for you. Reference it by root-absolute path.

**Edit copy in a section with an illustration.** Change the text nodes only. Leave every SVG
attribute alone.

**Share image and canonical on every page.** Every indexable page carries `rel="canonical"`,
og:title, og:description, og:url, og:image and the matching twitter tags with
`twitter:card` set to `summary_large_image`. Use the clean URL with no `.html` and no trailing
slash (`/coffee`, `/blog`), because Vercel redirects the other forms. Use
`share-shopfront.jpg` as og:image unless the page has its own hero image.

**Add a booking CTA.** Copy an existing one. It is a plain link to the booking page, `/coffee`. Use coffee wording from the copy rules.

**Add a page.** Copy 404.html as the template: it links site.css and page.css, has the
simple header and the legal footer, and uses root-absolute links. Add only what is unique to the
new page in its own `<style>`, and a "Send a message" link to `/#enquiry` rather than its own
copy of the email script. Never copy index.html's header structure. Vercel serves a new .html file at
its clean URL with no config change. Update the nav in whichever files carry links.

**Add a note (blog post).** Create a new HTML file in `blog/` following the pattern in
`your-website-should-feel-like-meeting-you.html`. Set unique title, meta description, canonical,
keywords. Use `noindex,nofollow` for drafts, `index,follow` for published. Include JSON-LD
BlogPosting with datePublished, dateModified, author (Petro Wall), publisher (Wall Media Ltd),
keywords from tags, articleSection from category, and image URL (string, not ImageObject) when
a hero image is included. Add og:image and twitter:image meta tags (with full 
https://www.offthewalldigital.com URL) when a hero image is present, and set twitter:card to
summary_large_image. Add the note to `blog/index.html`, relevant category page, and tag pages.
Update `rss.xml` if published (exclude drafts). Do not include draft posts in sitemap.xml.

**Listing card thumbnails (required for every note).** Every note card on listing pages 
(blog index, category pages, tag pages) displays a thumbnail of the post's featured image. The 
card uses a horizontal flexbox layout: image on the left (160px × 120px, rounded, with subtle 
shadow) and text content on the right. On mobile (below 640px) the layout stacks with image 
above text (full width, 200px height). Image src uses root-absolute paths like 
`/assets/blog/<slug>.png`. The thumbnail img element appears as the first child inside the 
`.post-card` link, followed by a `.post-card__content` wrapper containing the existing top, 
heading, excerpt, and tags structure. The whole card remains one clickable link. See 
`blog/index.html` for the complete pattern.

**Post hero images (optional).** When a note includes a hero image: (1) the title block
(category, date, read time, h1, tags, byline) appears first inside `.wrap.hero`, (2) the hero
image follows in a separate `.wrap` container with class `.post-hero-img`, positioned after
the hero div closes but before the article, (3) image styling via `.post-hero-img`: max-width
760px to match article column and other post content, max-height 480px with object-fit cover,
border-radius 16px, subtle shadow (0 8px 24px -12px rgba(47,51,39,.18)), margin-top
clamp(32px,5vw,48px). The image lives inside the content wrap, not full viewport width. Store
hero images in `assets/blog/` as PNG or JPG. Use relative path `../assets/blog/<slug>.png` in
the img src. Use full absolute URL
`https://www.offthewalldigital.com/assets/blog/<slug>.png` in og:image, twitter:image, and
JSON-LD image. Loading attribute should be "eager" for hero images. Include descriptive alt
text.

**Post column width (760px).** Every post follows a shared 760px max-width column for title,
hero image, article, coffee CTA (`.cta-block`), author card, and related notes (`.related`).
The `.cta-block` and `.related` divs must include `max-width:760px` in their inline styles,
with `margin:clamp(...) auto 0` for horizontal centring, matching the pattern used for 
`article` and `.author-card`. On wide viewports all content blocks sit in the same vertical
column.

**Author card on every note.** Every post carries the same author call-out after the
coffee CTA and before Related notes. Copy it from
`blog/your-website-should-feel-like-meeting-you.html` (the `aside.author-card` block). Photo
lives at `assets/blog/petro.jpg`. Do not rewrite the bio per post. If the card copy or
photo changes, update the template post and every existing note in one go.

**Add a category or tag.** Create `blog/category/<slug>.html` or `blog/tag/<slug>.html`
following the existing pattern. Add the category chip to `blog/index.html`. Add new category
or tag pages to sitemap.xml. Update category/tag lists on existing posts as needed.

**Links within Notes.** Use root-absolute paths (`/blog/category/websites`, `/blog/<slug>`) 
not relative paths (`./category/websites.html`, `./<slug>.html`). With `trailingSlash: false`, 
`/blog/index.html` is served at `/blog` (no trailing slash), so `./` relative links resolve 
against `/` (parent of last segment), not `/blog/`, causing 404s.

**Internal links use clean URLs.** Link to `/coffee`, `/privacy`, `/privacy#terms`, `/blog`,
never `coffee.html`, `privacy.html` or `/blog/`. Vercel answers those with a 308 redirect, so
every click on them costs an extra round trip. `./`, `/` and `./#enquiry` are fine as they are.

**Notes listing spacing.** All Notes listing pages (blog index, category, and tag pages) follow
the same tighter spacing standard to avoid large empty cream voids between sections. These
rules live once, in `assets/css/notes-list.css`. The standing CSS values are:

- `.hero` padding: `clamp(56px,9vw,90px) clamp(20px,5vw,40px) clamp(24px,4vw,40px)` (top, 
  horizontal, bottom). Bottom padding is intentionally short (24–40px) to keep category chips 
  close to the first post card.
- `.posts` padding-top `clamp(24px,4vw,40px)` and padding-bottom `clamp(80px,11vw,120px)`.
  Top padding is capped at 24–40px to prevent a tall unused void on short listings. Set top
  and bottom only, never the `padding` shorthand: the element is `wrap posts`, and the
  shorthand wipes out `.wrap`'s side gutter, which put cards flush against the screen edge on
  phones and tablets until 29 September 2026.
- `.post-card`: `display:flex; gap:clamp(18px,2.8vw,24px); padding:clamp(20px,3vw,26px)`. Flex 
  layout supports the thumbnail pattern (thumb left, text right; mobile column stack). Gap and 
  padding are modest to keep cards dense but readable.
- `.post-card__thumb`: `flex:none; width:160px; height:120px` on desktop, `width:100%; 
  height:200px` on mobile (under 640px).
- `.post-card__content`: `flex:1; min-width:0` ensures text content fills remaining space and 
  truncates gracefully.

These values apply identically on `blog/index.html`, `blog/category/*.html`, and 
`blog/tag/*.html`. When adding a new listing page or adjusting layout, prefer denser, calm 
spacing over generous clamps. The page should feel grounded, not floaty. Preserve the flex 
thumbnail layout and 24px margin between cards.

---

## Known weaknesses, for us rather than the agent

Recorded so they get fixed rather than rediscovered.

- Headers, footers and head tags are still copied into every page, because there is no
  build step to include them. Changing the footer or nav still means editing every page.
- Two versions of the Google Fonts link (with and without italics) are still in use.
- **No logo yet.** One will be designed as an SVG later. Until then the "crooked frame" mark
  stands in, and it is not a finished logo. It lives in two places on every one of the 11 pages:
  the inline `<svg>` inside the header's `.brand` link (search `rotate(-9 18 21)`), and the
  favicon, a URL-encoded SVG data URI in `<link rel="icon">`. When the logo arrives, save it as
  `assets/img/logo.svg`, point the favicon at `/assets/img/logo.svg` on every page, replace the
  header mark on every page, and add an Apple touch icon (a 180px PNG) at the same time.

Fixed on 29 September 2026: the external images now live in the repo, the email assembly
exists in one file only, robots.txt and a branded 404.html exist, every page has a social share
image, and canonical URLs match the clean URLs Vercel actually serves. privacy.html section 07 now
points rights requests at the enquiry form instead of an email button that no longer exists
(option chosen by Colin). Shared CSS moved into `assets/css/` with a computed style check on
every element of every page at four widths showing no visual change, and the unused Hyperagent
`.ha-img-placeholder` style blocks were removed from index.html and privacy.html. Internal
links point at clean URLs. The booking calendar ID is a single `CAL_ID` constant (plus the
`<noscript>` link) instead of five scattered copies.
