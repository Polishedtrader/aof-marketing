# Brief for "Service Graph Ai": make the email phones look like the business's own app

From the AI Office Flow marketing team, for Paul to paste in. 25 Nov 2026.

Paul: branding is what we sell. The campaign emails go to the business, so the customer and installer phones
(/email-art k=cust, k=inst, k=home, k=badge) and /preview/apps/ must look like THAT business is already using its
own app. Today, when there's no logo, they fall back to the business name in plain text (Mid Coast Kitchens, 25 Nov),
which reads as generic.

## What to change
1. **Their logo, everywhere:** app header, the notification ("Mid Coast Kitchens - now: Your install starts
   Monday..."), the home-screen icon (k=home) and the badge. Use l= at full quality; fit, never stretch or crop.
2. **Their colours:** pick the brand colour from the logo (dominant non-white/black colour) and use it for the app's
   header bar, buttons, chips (Plan / Elevations / Benchtops) and the "Signed" ticks, so the screens look like their
   app, not ours. Keep AI Office Flow orange only outside the phones. Optional c= override for a hand-picked colour.
3. **Their details on screen:** suburb/region in the sample address (e.g. "14 Ocean St, Port Macquarie"), job number
   in their style (K1043-SURNAME), installer names generic.
4. **No name-only fallback:** if l= is missing or the logo can't be loaded, return a clear error image/status (e.g.
   HTTP 422 + header X-Email-Art: no-logo) instead of drawing the name, so the Email writer's check catches it and
   holds the email.
5. **/preview/apps/** gets the same: logo, brand colour, home-screen icon, plus a "Book a 15-min look with Paul"
   button to https://ecosystem.measureflow.com.au/?business=<n>&source=preview#demo (carrying r).

## Done when
- [ ] k=cust/inst/home/badge for Hastings Kitchens (logo https://assets.cdn.filesafe.space/OXg2JWVJpCnA2kP7WLO1/media/6215840b8fc49e882f389f99.png)
      show their logo and colour on every phone, in Gmail, Outlook (light and dark) and Apple Mail on a phone.
- [ ] Same URL with no l= returns the no-logo error, not a name-only picture.
- [ ] /preview/apps/ for Hastings looks like their app and has the booking button.
- [ ] Existing params keep working (n, s, l, i, w, c); no change needed to emails already sent.

Marketing will update the email build (campaign/build_apps.py) only if a new parameter is needed - tell us which.
