# Off The Wall Digital, "The Window"

Marketing site for Off The Wall Digital (Petro Wall, Ramsgate, Kent), a trading name of
Wall Media Ltd. Self-contained static HTML, no build step, no dependencies to install.
Open any of the files in a browser and it works.

## Files

| File | What it is |
| --- | --- |
| `index.html` | The whole marketing site: hero, outcomes, "Is this you", front of house / back of house, four case studies, the week graphic, About, and the contact section. |
| `blog/index.html` | Notes listing page. Short thoughts on running a small business without drowning in your own admin. |
| `blog/*.html` | Individual note pages. Each one is a standalone HTML file with its own header, footer, and the full legal footer. |
| `coffee.html` | The booking page. Every coffee call to action links here. Holds the LeadConnector calendar, which sizes itself, so it needs a full page rather than a modal to grow into. |
| `thanks.html` | Post-booking thank you page. Set this as the calendar's redirect URL in GoHighLevel. Marked `noindex`. |
| `privacy.html` | Combined privacy notice and terms of use, tabbed, deep linkable at `#privacy` and `#terms`. |

## Opening it

No server needed for a first look, just double click `index.html`.

For anything involving the calendar or the enquiry form, serve it over HTTP instead,
because both rely on browser storage and a cross-origin request:

```
python3 -m http.server 8000
# then open http://localhost:8000/
```

## Deployment

All files sit at the repo root, so any static host works. On GitHub Pages, serve from
`main` / root and `index.html` is picked up automatically. Vercel needs no config either.

Booking happens in a popup, so there is no separate booking page. The coffee links carry
the calendar URL as their `href`, which only comes into play when scripts are off or
browser storage is blocked. Nothing needs editing for deployment.

Set `thanks.html` as the calendar's redirect URL in GoHighLevel so people land somewhere
of ours after booking rather than on a LeadConnector confirmation screen.

## Integrations

**Booking calendar.** LeadConnector widget `dqB0NblntdSZnLlpSFEz` ("Coffee with Petro",
30 min), resized by `https://link.msgsndr.com/js/form_embed.js`.

The widget needs browser storage. The site checks for it before deciding what to do:

- storage available (a normal domain) → the calendar opens embedded in the coffee popup
- storage blocked (sandboxed preview hosts) → the popup is skipped and the coffee links
  behave as ordinary links straight to the calendar
- JavaScript off → same, the `href` does the work

`form_embed.js` parks the iframe off screen to measure its content height and does not
restore it, so `.cal` reclaims `position`, `opacity`, `visibility` and `pointer-events`
with `!important` while leaving the height the script calculates alone. Do not remove
those overrides or the calendar will load invisibly.

There is a nine second safety net that redirects to the calendar if the widget never
renders at all. It is guarded on the modal still being open, and cleared both on iframe
load and on modal close. Those guards matter: a closed modal is `display:none`, so the
iframe measures zero height, and without them the timer fires and navigates away from
whatever the visitor moved on to.

**Enquiry form.** Posts JSON to a GoHighLevel inbound webhook. The URL is the
`ENQUIRY_WEBHOOK` constant near the top of the script block. Payload:

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
  at runtime and sits behind a labelled button, with a no-script note pointing at the
  phone number.
- **Cream palette only, never dark, and no light/dark toggle.** Tokens live in `:root`.
- **SVG line art, never emoji.**
- Calls to action are coffee invitations that warm up down the page: "Fancy a coffee?",
  "Start with a coffee", "That sounds like me", "Tell me about yours", "Put the kettle on".

## Images are still hosted externally

The seven images (`hero-open`, `hero-shut`, the four case study screenshots and Petro's
portrait) are still served from `pub.hyperagent.com`. They work, but they are an external
dependency the site should not have. Download them into an `assets/` folder and repoint
the `src` attributes before this goes anywhere permanent.

## Still outstanding

- Four client testimonial quotes.
- One real result per case study (hours saved, or the client's own words). The case studies
  are written as "Before" and "Now" with a deliberate gap where a result belongs.

## Legal

Off The Wall Digital is a trading name of Wall Media Ltd, registered in England and Wales,
company number 15045668. Registered office: Longfrey Cottage, Dorking Road, Chilworth,
Surrey, GU4 8RH.
