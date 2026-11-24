# AI Office Flow marketing

Marketing for AI Office Flow (Paul's AI office system for kitchen and joinery businesses, sold through MeasureFlow).
The code lives in Polishedtrader/ai-office-flow: never change it from here. The email pictures (/email-art) and
/preview/apps pages live there; if they need changing, Paul asks the AI Office Flow code chat.

## How it runs (Paul's rules, 24 Nov 2026)
- Paul signs off major campaigns and scripts at the Friday sales meeting. Once signed off, a campaign runs on its own.
  Signed-off campaigns: the current first email and follow-up, plus everything in `campaign/approved.md`.
- Paul replies himself to anyone who shows interest. The team never replies for him.
- Never contact Keena Kitchens, Northern Beaches Kitchens or CTI Kitchens. Leave CTI out of all copy.
  Paul is introduced as having run a kitchen business for over 25 years.
- Only publicly listed business enquiry addresses; the footer says where the address came from. No personal addresses.
- Images PNG/JPG only (no raw SVG). Any reply, bounce or no-thanks: cancel the follow-up, mark it, suppress, never email again.
- Commit as Paul: `git -c user.name="Paul" -c user.email="enquiry@ctikitchens.com.au" commit ...`

## The team (scheduled tasks; each reports to Paul)
| Role | When (Sydney) | Job |
|---|---|---|
| Email writer | Weekdays 8:11am | One email a day from a signed-off campaign, after checks; books one follow-up (3 working days, 8:30am); logs to `reports/sent-log.md`. |
| Inbox watcher | Weekdays 11:53am | Bounces, replies, no-thanks; pushes interested replies to Paul straight away. |
| Social writer | Wednesdays 10:23am | 3 posts for Facebook, Instagram, LinkedIn in `social/`, for Paul to approve and post. |
| Lead researcher | Mondays 8:52am | New kitchen/joinery businesses by region into contacts.csv + queue.csv (runs on Paul's PC). |
| Sales manager | Fridays 2:47pm | Weekly sales meeting: report doc, who to call, plan, sign-offs; decisions in `meetings/`. |

## Files
- `campaign/` - the email campaign; read `campaign/README.md` first. `queue.csv` (send order + status),
  `contacts.csv`, `emails/`, `followups/`, scripts (`next.py`, `mark.py`, `followup.py`, `build_apps.py`, `preview.cjs`),
  `approved.md` (signed-off campaigns and scripts). Run scripts from the repo root.
- `web/public/email/` - email fonts and images used by `campaign/preview.cjs`.
- `leads/2026-11-mid-north-coast-social.csv` - 23 Mid North Coast businesses from Paul's social lists, not yet in the
  queue and no emails yet. `fit`: kitchen / joinery / check / no.
- `reports/` - `sent-log.md` (every send) and `weekly.md` (weekly numbers). `meetings/` - sales meeting decisions.
  `social/` - weekly posts.

## Sending setup
- Resend, from `MeasureFlow <jobs@officeflow.measureflow.com.au>`, reply-to `accounts@measureflow.com.au` (Titan mail at
  Vodien), header `List-Unsubscribe: <mailto:accounts@measureflow.com.au?subject=Unsubscribe>`.
- Domain officeflow.measureflow.com.au (DNS at Vodien). Receiving and open/click tracking turned on 24 Nov 2026; they
  need the MX record (`officeflow` -> receive-apne1.forge.rmta.net, priority 10) and the tracking CNAME
  (`track.officeflow` -> links2.resend-dns.com) at Vodien. Planned: a replies@officeflow.measureflow.com.au inbox in Resend.
- Logos: use the PNG favicon via `https://officeflow.measureflow.com.au/.netlify/images?url=<encoded>&w=96&h=96&fit=contain&fm=png`.

## Where things stood at the move (24 Nov 2026)
5 sent (Port Kitchen World, DMB Kitchens, Concept Kitchens, Unique Design Kitchens & Joinery, Old Lake Joinery), each
with one follow-up booked; 321 queued. No replies, bounces or no-thanks. Two AI Office Flow sales so far.

## About AI Office Flow (for writing)
Website chat that answers enquiries and books measures, reception, numbered jobs, quotes signed online, payment stages
into Xero/MYOB, Google Calendar, factory and site packs, customer and installer apps with the business's own logo, job
profit. A one-off build for each business, on accounts in the business's own name, with a monthly support plan. Built
and run by Paul (MeasureFlow). Demo: https://officeflow.measureflow.com.au/ecosystem/
The pain Paul pitches: the "where are we up to?" calls and quoting many jobs to win one.
