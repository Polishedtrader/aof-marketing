# Tracking and ads rollout checklist (Meta, LinkedIn, Google)

Owner in brackets. Tick as done. Nothing is spent until Paul approves a campaign at the Friday meeting.

## 1. Build (no IDs yet, so nothing tracks)
- [ ] Ecosystem site: tags (off until IDs set), booking form picks up r + utm, Lead event on submit, privacy wording [Website dev]
- [ ] officeflow: tags on /ecosystem/, /roadmap/, /privacy/ only; visit log on /ecosystem/ + /preview/apps/; "Book a 15-min look with Paul" buttons -> ecosystem form; roadmap direct Send [AI Office Flow code chat]
- [ ] measureflow.com.au + cabinetcare.com.au public pages: "Book a demo" button -> ecosystem form (with source) [whoever builds those sites]
- [ ] Check: no tag requests anywhere with no IDs set [both chats]

## 2. Accounts (Paul - about 30-45 min total)
- [ ] Meta: Business portfolio for MeasureFlow -> Events Manager -> create a dataset (Pixel) -> copy the Pixel ID
- [ ] Meta: verify the domain measureflow.com.au (adds a DNS TXT record at Vodien)
- [ ] LinkedIn: company page for MeasureFlow -> Campaign Manager ad account -> Insight Tag -> copy the Partner ID
- [ ] Google: Analytics (GA4) property -> copy the Measurement ID (G-...); Google Ads account if ads are wanted -> conversion ID (AW-...)
- [ ] Add a payment method to each ad account only when a campaign is approved

## 3. Switch on (Paul, 10 min)
- [ ] Add the IDs as Netlify environment variables on BOTH sites (names given by the website chats), redeploy

## 4. Test [website chats + Paul]
- [ ] Meta Pixel Helper / LinkedIn Insight Tag check / Google Tag Assistant on: ecosystem home, officeflow /ecosystem/ and /roadmap/
- [ ] Not firing on: officeflow sign-in (/), /preview/apps/, customer pages, partner portal, account pages
- [ ] Test booking with ?r=999 -> lead email shows r=999, customer gets the confirmation, Lead fires
- [ ] /preview/apps/?r=999 -> one visit-log row, no tag requests

## 5. Use it [Marketing team]
- [ ] Approve ?r= links in campaign emails (Friday sign-off) -> Email writer adds them
- [ ] Sales meeting reports visits by business, time on page, bookings and source each week
- [ ] Build audiences once there's traffic: website visitors 30/90 days, demo viewers, roadmap starters; exclude customers
- [ ] Strategist proposes a first small retargeting test (budget, audience, ad, 2-week check) for Paul's sign-off

## Meta Pixel (27 Nov 2026)
- Created: dataset "MeasureFlow ecosystem", ID 1179568654407034, on ad account 409888448181393 (Paul Snell; MeasureFlow page and measureflow Instagram sit under it). Sent to website dev to install on ecosystem.measureflow.com.au. CabinetCare Portal dataset (2238942376926051) is separate.
- 27 Nov 2026, dev reply (strategy/briefs/2026-11-27-reply-booking-form-and-ad-tracking.pdf): LIVE - form field
  "Business name" (required), double-submit protection, source/utm tags in lead emails (fb-group example tested),
  Meta Pixel PageView + Lead, privacy page. GA4 + Google Ads tag BUILT, waiting on Paul: create GA4 + Google Ads,
  put IDs in Netlify (site measureflowecosystem) env vars NEXT_PUBLIC_GOOGLE_TAG_ID and
  NEXT_PUBLIC_GOOGLE_ADS_CONVERSION, then trigger deploy. Needed before the 12 Jan search ads.
