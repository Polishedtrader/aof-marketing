# Brief for the AI Office Flow code chat: tracking, booking button and demo-visit log

From: Paul / marketing team, 25 Nov 2026
Repo: Polishedtrader/ai-office-flow (live: https://officeflow.measureflow.com.au). Follow that repo's CLAUDE.md.
Goal: see who visits the demo and where they came from, so we can retarget visitors on Facebook, Instagram,
LinkedIn and Google, and put businesses that looked at the demo at the top of Paul's visit list.
Nothing is spent on ads until Paul approves. This brief is only the site work.

---

## 1. Ad and analytics tags: public marketing pages ONLY

**Load them on:** the home page `/` and the demo `/ecosystem/` (plus its sub-pages), `/privacy/` and the new
booking page (part 3).
**Never load them on:** customer quote pages, website chat, the reception, fabricator upload, the customer and installer
apps, sign-in, setup, or any page showing a business's or customer's data. Use an allow-list of paths, not a block-list.

Tags (each loads only if its ID is set, so other businesses' copies stay clean; nothing hard-coded):

| Tag | Netlify env var | Notes |
|---|---|---|
| Meta Pixel | `NEXT_PUBLIC_META_PIXEL_ID` | Facebook + Instagram |
| LinkedIn Insight Tag | `NEXT_PUBLIC_LINKEDIN_PARTNER_ID` | |
| Google tag (gtag.js) | `NEXT_PUBLIC_GOOGLE_TAG_ID` | GA4 and/or Google Ads ID |

Paul will add the IDs in Netlify once the ad accounts exist. Until then the site must behave exactly as it does now.

Events:
- `PageView` on every allowed page (all three tags).
- `ViewContent` (Meta) / `view_item` (Google) on `/ecosystem/`.
- `Lead` (Meta) / `generate_lead` (Google) / LinkedIn conversion when a booking is submitted (part 3).

## 2. Campaign link tag (`?r=`), so we know which emailed business looked

Campaign emails will link to the demo as e.g.
`https://officeflow.measureflow.com.au/ecosystem/?r=27&utm_source=email&utm_medium=cold&utm_campaign=apps-v1`
(`r` = the business's row number in the marketing queue; no names in URLs).

On the allowed pages:
- Read `r` and the `utm_*` values on arrival, and keep them for the visit (sessionStorage).
- Log one row per visit: `r`, `utm_source`, `utm_medium`, `utm_campaign`, `referrer` host, landing path, pages viewed,
  seconds on site (send on `pagehide`), and timestamp. **No IP address and no personal data.**
- New table, e.g. `public.demo_visits`, written by a small edge function, **not** a direct anon insert.
  - Per CLAUDE.md (new tables since 30 Oct 2026): grant explicitly to `service_role` only and revoke from `anon` and
    `authenticated`.
  - Rate-limit or validate input so it can't be spammed (r must be numeric, sensible lengths).
- Pass `r`/utm on to the booking form (part 3) as hidden fields.
- The marketing team reads this table weekly (read-only), so a simple query/view such as "visits by r, last 7 days" is enough.

## 3. "Book a 15-min look with Paul" button and page

- Add the button where people will see it on `/ecosystem/` (top and bottom) and on `/`. Use the MeasureFlow
  palette: accent #C1683A, ink #0A0A0A, paper #FAF8F4.
- Page `/book/` (or a modal) with these fields: name, business name, phone, email, best time (morning/afternoon), and an
  optional note. Include hidden `r`/utm fields.
- On submit:
  - fire the `Lead` events;
  - email Paul at accounts@measureflow.com.au through Resend (use the existing `EMAIL_FROM` secret) with every field
    plus `r`/utm;
  - show "Thanks, Paul will call you to set a time."
- It must work on phones as well as iPad and desktop (it's a public customer-facing page).
- If the job system already has a booking/enquiry flow that fits, reuse it rather than building a second one.

## 4. Privacy page

Add a short section to `/privacy/`, in plain English:
> This website uses cookies and similar tools from Meta (Facebook/Instagram), LinkedIn and Google to understand
> how visitors use our public pages and to show our ads to people who have visited. They are not used on any page
> that shows customer or job information. You can opt out of personalised ads in your Facebook, LinkedIn and Google
> ad settings, or by blocking cookies in your browser.

## 5. Done when

1. With no IDs set, the site is unchanged, and no tag requests appear in the browser network tab on any page.
2. With test IDs set, the tags fire on `/`, `/ecosystem/` and `/book/` only. Check with Meta Pixel Helper and
   LinkedIn/Google tag assistants.
3. A visit to `/ecosystem/?r=999&utm_source=test` writes one `demo_visits` row with seconds-on-site.
4. A test booking emails accounts@ with `r=999`, and fires `Lead`.
5. Customer pages (quote, chat, apps, fabricator upload) load no third-party tags.
6. Checked on iPad, desktop and a phone (`/book/`).

Do not change the campaign emails here. The marketing team adds `?r=` to its email links once Paul approves.
