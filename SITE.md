# SITE.md — Off The Wall Digital

Read this before changing anything on this site.

This file exists because the site has no build step and no shared stylesheet, so the same
thing lives in several places. This is the map. It was written from a full read of every file
on 4 September 2026.

---

## Rule zero

Every count in this file is a snapshot, not a promise. Before changing anything that appears
in more than one place, SEARCH the repo for the current occurrences and update every one you
find. If your search returns a different number than this file says, trust your search, make
the change, and flag the difference so this file gets corrected.

Two specific traps that a single find-and-replace will miss, both explained below: the booking
widget ID is embedded inside an element ID as well as in URLs, and the email address is
assembled from arrays that are split differently in different files.

---

## Deployment and previews

Hosted on **Vercel**, serving this repo. Confirmed from the live response headers on
4 September 2026: the apex redirects 308 to www, and both are served by Vercel.

Pushing to `main` deploys straight to production. **On this site that is the agreed way of
working**, decided by Colin on 4 September 2026. Commit to main, let it go live, then show
Petro. Do not open branches and pull requests for ordinary changes here.

`vercel.json` sets `cleanUrls: true` and `trailingSlash: false` so canonical paths like `/blog/why-your-website-should-feel-like-you` and `/coffee` resolve without the `.html` suffix. Keep that file. Do not remove it to "simplify" the deploy.

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
| index.html | / | The whole marketing site, 92,918 bytes, about 1,723 lines. Readable, not minified. |
| privacy.html | /privacy | Privacy and terms, tabbed. |
| thanks.html | /thanks | Post-booking landing page. Carries `noindex,nofollow` deliberately, set as the calendar's redirect URL in GoHighLevel. Do not remove the robots tag. |
| blog/index.html | /blog/ | Notes listing page with category filter chips and rich post cards. |
| blog/why-your-website-should-feel-like-you.html | /blog/why-your-website-should-feel-like-you | Draft post (noindex). First note on brand voice and websites. |
| blog/category/websites.html | /blog/category/websites | Category listing for Websites notes. |
| blog/tag/*.html | /blog/tag/* | Tag listing pages (websites, brand-voice, small-business). |
| rss.xml | /rss.xml | RSS feed for published notes. Excludes drafts. |
| sitemap.xml | /sitemap.xml | Site sitemap including blog pages. Draft posts omitted. |
| README.md | — | Petro's conventions and copy rules. Read it alongside this file. |

Most marketing images are still hosted externally on pub.hyperagent.com (hero before and after,
four case study screenshots). Petro's Notes author portrait is in-repo at
`assets/blog/petro.jpg`. Moving the remaining Hyperagent images into `assets/` is still
outstanding work, already flagged in the README.

---

## The design system

Defined as CSS custom properties in a `:root` block. Use these tokens, never raw hex values,
and never introduce a colour that is not here.

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

### The token blocks are NOT identical across files

This is the trap. Each file has its own `:root` and they hold different subsets.

- **index.html** has the full set above.
- **privacy.html** is condensed. It is missing `--sage`, `--tealwash`, `--coralwash`,
  `--green-deep`, `--gold-dark`, `--coral-dark`, `--pane-border`, `--shadow-s`, `--shadow-l`,
  `--maxw` and `--gutter`.
- **thanks.html** sits in between, and deliberately uses **different values**:
  `--maxw:1000px` and `--gutter:clamp(20px,5vw,56px)` against index's 1240px and 64px. Those
  differences are intentional, do not "fix" them.

So a token change that should apply site-wide is a three-file change, and you must check which
tokens each file actually declares before assuming one exists there.

---

## Shared values, and everywhere they live

**Phone number.** `07775 562102` displayed, `tel:+447775562102` in links. Four occurrences:
two in index.html (the contact section and the coffee modal), one in privacy.html as body text
("ring 07775 562102"), one in thanks.html. Search both forms separately.

**Email address.** Never write `petro@wallmedia.co.uk` into the source. It is deliberately
assembled in JavaScript at runtime so scrapers cannot read it, and that protection must
survive any edit. Two different patterns are in use:

- index.html and thanks.html: `var user = ['pe','tro'], host = ['wallmedia','co','uk'];`
- privacy.html: `var u=['petro'], d=['wallmedia','co','uk'];`

Both join with `String.fromCharCode(64)` for the @. A search for `['pe','tro']` finds two of
the three files and silently misses privacy.html.

**Legal footer.** Appears in all three files and must be reproduced word for word:

> Off The Wall Digital, a trading name of Wall Media Ltd. Registered in England and Wales,
> company number 15045668. Registered office: Longfrey Cottage, Dorking Road, Chilworth,
> Surrey, GU4 8RH.

Company number and registered office also appear twice in privacy.html's own body text, in the
"Who we are" and "Who runs this site" sections. Five occurrences of each in total across the
repo. Do not split, shorten or paraphrase any of it.

**Header and footer markup** is duplicated across all three files and the structures differ.
index.html has the full sticky nav with a mobile hamburger; privacy.html and thanks.html have
their own simpler topbars. Never copy index.html's header structure into the other two.

---

## Stop list: do not change these

Anything here needs a human. Say plainly that it affects how the site takes bookings or what
it is legally required to say, pass it on, and never partially do it.

**The booking widget.** The GoHighLevel calendar ID `dqB0NblntdSZnLlpSFEz` appears **ten
times** in index.html. Five are `href` fallbacks on `data-coffee` links (desktop nav, mobile
nav, hero, "Is this you", case studies), one is the iframe's `data-src`, one is inside a
nine-second fallback redirect, and critically **one is part of an element ID**:
`dqB0NblntdSZnLlpSFEz_1788453583961`. A find-and-replace on the URL will miss the element ID
and break the widget.

**The `.cal` iframe CSS overrides.** A stack of `!important` rules (position, left, top,
opacity, visibility, pointer-events, overflow) exists specifically to counteract what
GoHighLevel's `form_embed.js` does to the iframe after it measures height. Remove or rewrite
them and the calendar loads invisibly, which looks like nothing is wrong. The README says the
same thing.

**The enquiry webhook.** `ENQUIRY_WEBHOOK` near the top of index.html's script block, pointing
at a GoHighLevel hook. Setting it to an empty string is the documented way to fall back to a
prefilled mailto, but changing it otherwise breaks enquiry delivery silently.

**`EMBED_SRC`**, the GoHighLevel `form_embed.js` URL.

**The email assembly JavaScript**, in all three files. See above.

**The legal footer text**, in all three files.

**`noindex,nofollow` on thanks.html.** It is the calendar's redirect target and must stay out
of search.

**Inline SVG.** The shopfront illustration is around 120 lines and the back-of-house diagram
another 80, plus browser chrome on every case study card. Copy near them can be edited; SVG
attributes must not be touched or the artwork corrupts.

**`data-coffee` attributes.** Every booking CTA carries one, and JavaScript intercepts clicks
on `[data-coffee]` to open the modal. A new booking CTA without the attribute will jump
straight to the external calendar instead of opening the popup.

**`[hidden]{display:none!important}`.** Declared in all three files. Do not add the `hidden`
attribute to anything you intend to be visible.

There is **no analytics, no tracking pixel and no cookie consent logic** on this site, and
none should be added without Petro asking. The only localStorage use is a one-line
availability test deciding whether the booking modal can open. The privacy policy states that
nothing is stored on the visitor's device, so adding tracking would make that page untrue.

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

**Change a phone number.** Search both the spaced display form and the `tel:` form. Four
places across three files. Check the coffee modal in index.html, it is easy to miss.

**Change a colour or spacing token.** Three files, and check which tokens each one actually
declares before editing. Remember thanks.html deliberately differs on `--maxw` and `--gutter`.

**Edit copy in a section with an illustration.** Change the text nodes only. Leave every SVG
attribute alone.

**Add a booking CTA.** Copy an existing one including its `data-coffee` attribute and its
`href` fallback to the calendar URL. Without the attribute it bypasses the popup.

**Add a page.** No template exists, so the new page needs the head boilerplate, a `:root`
block, its own header and footer, and the email assembly script if it shows an email. Match
privacy.html's simpler structure rather than index.html's. Vercel serves a new .html file at
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

**Author card on every note.** Every post carries the same author call-out after the
coffee CTA and before Related notes. Copy it from
`blog/your-website-should-feel-like-meeting-you.html` (the `aside.author-card` block). Photo
lives at `assets/blog/petro.jpg`. Do not rewrite the bio per post. If the card copy or
photo changes, update the template post and every existing note in one go.

**Add a category or tag.** Create `blog/category/<slug>.html` or `blog/tag/<slug>.html`
following the existing pattern. Add the category chip to `blog/index.html`. Add new category
or tag pages to sitemap.xml. Update category/tag lists on existing posts as needed.

---

## Known weaknesses, for us rather than the agent

Recorded so they get fixed rather than rediscovered. The booking widget ID should be a single
constant at the top of the script block the way `ENQUIRY_WEBHOOK` already is, which would turn
ten scattered occurrences into one. The three `:root` blocks want a single source. The seven
external images should live in the repo. And the email assembly pattern should be made
identical across the three files so one search finds all of them.
