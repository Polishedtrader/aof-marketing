# Tracking and ad audiences: what needs setting up

Paul asked (25 Nov 2026) what has to be set up on Facebook, Instagram and the website to see who visits and to
market to them. Nothing here is live yet. Who does each step is in brackets.

## 1. Accounts (Paul, about 30-45 min, once)
- **Meta Business** (business.facebook.com) for MeasureFlow: link the MeasureFlow Facebook Page and the Instagram
  account (it must be a professional account), create one ad account, and add a card. No spend until the Friday OK.
- **Verify the domain** measureflow.com.au in Meta Business. It's a TXT record at Vodien; the team gives you
  the exact record.
- **LinkedIn**: a MeasureFlow Company Page plus a Campaign Manager ad account.
- **Google Ads** account (and Google Analytics 4 if you want visit reports in one place).

## 2. Website (the AI Office Flow code chat, not this chat)
- Put the **Meta Pixel**, **LinkedIn Insight Tag** and **Google tag** on the public marketing pages only: the home
  page, /ecosystem/ (the demo) and any booking page.
- **Never** put them on customer pages (quotes, chat, fabricator upload, the customer and installer apps). Those
  are the businesses' customers' data.
- Events to record: page view; "viewed demo" on /ecosystem/; "booked a look" when someone books.
- A clear **"Book a 15-min look with Paul"** button and form on the demo, if there isn't one already. Without a
  booking action there's nothing to measure an ad against.
- Update **/privacy/** to say the site uses advertising and analytics cookies (Facebook, LinkedIn, Google).
  This is good practice under the Australian Privacy Principles.

## 3. Email links (this team, needs Paul's OK at Friday's meeting because it changes the signed-off emails)
- Add a tag to every demo link so the site can tell which business clicked, e.g. `?r=<queue number>`, plus
  `utm_source=email&utm_campaign=apps-v1`.
- Resend already shows which address clicked. The tag also shows what they looked at and for how long, and puts
  demo visitors from our emails into the Meta/LinkedIn retargeting audiences.
- The Sales manager puts businesses that opened the demo at the top of your visit list.

## 4. Audiences to build once tracking is on (team drafts, Paul approves)
- **Demo visitors**, last 180 days: Meta and LinkedIn retargeting. This is the best paid audience we'll have.
- **People who watched 50%+ of your video** on Facebook/Instagram. This works without the pixel, so it can start
  as soon as the video is posted as an ordinary post.
- **Page and Instagram engagers**, last 365 days.
- **LinkedIn company list**: business names and websites from queue.csv, then target Owner/Director titles.
- **Exclude:** existing customers, Keena Kitchens, Northern Beaches Kitchens, CTI Kitchens, and anyone marked
  no-thanks or bounced.
- **Don't upload our email list to Meta.** The addresses were collected from public websites, not given to us for
  ads, and Meta's custom audience terms require that we have permission to use them. Company lists on LinkedIn are
  business names, not personal data.

## 5. What it will and won't tell us
- **Will:** how many visit the demo, from where (email, ad, social), how long they stay, which ad led to a booking,
  and, through the email tag, which campaign business looked at it.
- **Won't:** Facebook and LinkedIn never tell you *who* an individual ad visitor is. Only the email tag and
  bookings name a business.
