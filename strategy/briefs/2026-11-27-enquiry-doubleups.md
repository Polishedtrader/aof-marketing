---
title: "Brief: how an enquiry is created, and where double-ups happen"
subtitle: "From the AOF marketing team, for the Service Graph Ai project (AI chat, AI calls, enquiries). Copy to Measureflow Ecosystem for the booking form. 27 Nov 2026"
---

## Why

Paul wants one enquiry per business, whichever way they come in. We can't see the AOF or website code from the
marketing project, so this brief sets out what we know from the outside and asks you to map the rest and stop
double-ups.

A real example from 27 Nov: Nicole Smith (Unique Coastal Kitchens) came in through the website form. The
notification read **"Business: Business"**. The business-name field sent its placeholder or label, not the real
name. Please check that first.

## The ways an enquiry comes in (as we understand it)

| # | Way in | What happens (known) | Please confirm |
|---|---|---|---|
| 1 | Ecosystem **Book a demo form** | Saved in Netlify Forms. Email to accounts@ tagged "website form" with r and utm. Branded confirmation to the customer. | Does it also create an enquiry or job number in AOF? |
| 2 | **AI chat** on the ecosystem site (AOF's chat) | Texts Paul (Twilio) for demo, price, "call me" or 3+ people. Lead emailed to accounts@ tagged "chat". "Book a 15-min look" opens the form **prefilled**. | Is an enquiry created when the chat captures details, and again when the prefilled form is sent? |
| 3 | **AI phone calls** (Twilio number) | Not known to us. | What does a call create? Does it match an existing chat, form or enquiry by phone number? |
| 4 | **Replies to our campaign emails** ("show me", walkthrough mailto, questions) | Arrive at accounts@ and are picked up by the marketing Inbox watcher. | Do these ever create an AOF enquiry? |
| 5 | Paul's own calls, visits and texts | Paul logs them. | Is there a manual "new enquiry" in AOF? |

## Where double-ups can happen

1. **Chat, then the prefilled form.** The chat sends a lead, then the same person sends the form: two leads, two
   emails, maybe two enquiry numbers, plus a text to Paul. *Most likely double-up.*
2. **Chat or form, then a phone call** (or the other way round), from the same person or phone number.
3. **The same form sent twice.** A double tap, the back button and resubmit, or coming back days later.
4. **Same business, different person or email.** For example, admin@ fills the form and the owner rings the AI
   line.
5. **A campaign email reply plus a form or chat** from the same business. Marketing will now link these on our
   side (below).
6. **Phone formats don't match** (0408 856 839, 0408856839, +61408856839), so matching by phone fails.
7. **Free email domains** (gmail, outlook): matching by domain would wrongly merge different businesses.

## What we'd like

1. **One matching rule** on every way in, before creating anything new. Match on the same email, **or** the same
   phone number (stored as +61…), **or** the same business email domain (not gmail, outlook and the like),
   within 30 days.
2. **If it matches:** add to the existing enquiry ("also came in by chat / call / form, date, notes"). Don't
   create a new one. Send Paul **one** alert, not several.
3. **Chat to form:** pass the chat's lead ID into the prefilled form (a hidden field) so the form updates that
   lead instead of creating a second one.
4. **Forms:** stop double submits (disable the button after sending, and ignore an identical resend within 10
   minutes). Fix the "Business: Business" field.
5. **Calls:** look up the caller's number first. Known caller: add the call to their enquiry and tell Paul who it
   is.
6. **Every enquiry records its source** (form, chat, call, email reply, Paul) plus r and utm, and a list of every
   way that business has contacted us.
7. **Reply with a one-page map**, so Paul and the marketing team see the full picture: each way in, what it
   creates, and where it is stored (Netlify, AOF, Twilio, email).

## What marketing is doing on our side

- The Inbox watcher now also reads the form and chat lead emails at accounts@. If the business is in our email
  campaign, it cancels their pending follow-up, marks them "replied", and flags them to Paul. A business that's
  already talking to us never gets a cold email.
- Inbound leads are logged in reports/pipeline.md and added to the queue as "never cold-email".
