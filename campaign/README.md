# Kitchen business email campaign (MeasureFlow sales, not part of the app)

One personalised email a day to a kitchen business, NSW first.
**Paul's rule from 24 Nov 2026:** Paul signs off campaigns and scripts at the Friday sales meeting. Once a campaign
is signed off it runs on its own: the Email writer sends each weekday without asking him. Signed off: the current
first email (design approved 19 Nov, TEST 6) and follow-up (approved 18 Nov), plus anything in `approved.md`.
New wording, subject lines or campaigns are drafts for the Friday meeting until Paul approves them.
(Moved from the AI Office Flow code repo on 24 Nov 2026; never change that repo from here.)

- `queue.csv`: the send order (NSW first, then VIC, QLD, SA, WA, TAS, ACT, NT; chains/flat-pack last).
  `status` is `queued`, `sent`, `skipped`, `no-thanks` or `bounced`.
- `emails/<file>.html`: each business's finished email (their logo, name, owner's first name, personal preview link).
- `build_apps.py` + `contacts.csv`: Email 1 (the customer app and installer app with their logo). Re-run `python3 campaign/build_apps.py` after changing the design; it rebuilds every queued email and subject. The button opens `/preview/apps/` with their name and logo.
- `next.py`: shows the next queued email. `mark.py <address> <status> [note]`: records what happened.
- `preview.cjs`: phone-width PNG of an email for Paul to check (logo shows as the business name in the preview only).

## Each morning (scheduled task, weekdays 8:11am Sydney)

1. `git pull`. Run `python3 campaign/next.py`. If it prints NONE, tell Paul the list is finished and stop.
2. If that business has no logo in `contacts.csv`, look at their website first: add their logo if there is a dark one,
   otherwise put their name exactly as the site writes it in the `wordmark` column (and `&w=` on the link), then
   `python3 campaign/build_apps.py`.
   Also look for a square icon on their site (apple-touch-icon or favicon, at least 120px, not the Wix/Squarespace default).
   If there is one, put its URL in the `icon` column: it becomes their app icon on the phone home screen.
   Otherwise their logo is fitted into the square.
   The phones, home screen and logo badge are pictures from /email-art (web/netlify/functions/email-art.mjs),
   drawn with their logo so Outlook dark mode can't change them. Check each /email-art and /preview/apps link in the
   email loads (WebFetch) before sending. Design approved by Paul 19 Nov 2026 (TEST 6).
3. LOGO RULE (Paul, 25 Nov 2026): branding is what we sell. Never send an email whose phones/badge show only the
   business name: the business's real logo must be in contacts.csv (logo column) and on the apps. No logo = don't send;
   leave it queued, note "needs logo" in queue notes, and send the next business that has one.
   Checks before sending (all must pass, see the Email writer task): signed-off copy; not Keena, Northern Beaches
   Kitchens or CTI and no mention of CTI; a publicly listed business enquiry address with its source in the footer;
   never emailed before and not suppressed in Resend; region order kept; name and logo match; PNG/JPG images only.
4. If a check fails and can't be fixed within the signed-off copy: `python3 campaign/mark.py <address> skipped "<reason>"`
   and move to the next business (one send a day). No thanks / bounced: `mark.py <address> no-thanks` (or bounced).
5. Send with the Resend connector:
   - from: `MeasureFlow <jobs@officeflow.measureflow.com.au>`
   - reply_to: `accounts@measureflow.com.au`, bcc: `accounts@measureflow.com.au` (Paul keeps a copy of every send, from 24 Nov 2026)
   - to: the address in queue.csv, subject from queue.csv, html: the file's contents (signed-off copy).
   - header `List-Unsubscribe: <mailto:accounts@measureflow.com.au?subject=Unsubscribe>` if the tool allows headers.
   If the Resend connector isn't connected, don't send: tell Paul it needs connecting in claude.ai and stop.
6. `python3 campaign/mark.py <address> sent`.
7. Schedule the follow-up (no sign-off needed: Paul approved the template on 18 Nov 2026):
   `python3 campaign/followup.py <address>` builds `campaign/followups/<html_file>` and prints the subject and
   `scheduledAt` (3 working days later, 8:30am Sydney). Send it with the Resend connector, same from/reply_to,
   with `scheduledAt` set, then record the id: `python3 campaign/followup.py <address> --id <resend id>`.
8. Commit `campaign/queue.csv` (author Paul) and push. Log it in `reports/sent-log.md`; tell Paul only if something went wrong.

## Replies and "no thanks"

If a business replied (the Inbox watcher finds it, or Paul says so), said no thanks (the follow-up has a "Not for us right now" button that emails
accounts@ with the subject "No thanks – <business>") or bounced, and its follow-up hasn't gone yet:
cancel it with the Resend connector (cancel-email, the `follow_id` in queue.csv), then
`python3 campaign/followup.py <address> --cancelled`. For no thanks / bounced also run `mark.py <address> no-thanks`
(or bounced) and add the address to Resend suppressions.

Rules: one email per business, never to a row marked no-thanks/bounced/skipped/sent, never to Hold or Keena (not in the queue).
Only send signed-off campaigns (see the top of this file).
