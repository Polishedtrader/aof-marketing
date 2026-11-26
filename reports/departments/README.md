# Weekly department reports

Paul (25 Nov 2026): each department gives its own weekly report; the Friday sales meeting then gives a
conclusion report and meeting minutes.

## Where and when
Each department writes `reports/departments/<Friday date YYYY-MM-DD>/<department>.md` for the week ending that Friday:

| Department | File | Written on |
|---|---|---|
| Lead research | lead-research.md | Monday run (covers last week + this run) |
| List building | list-building.md | Friday run |
| Email | email.md | Friday run |
| Inbox | inbox.md | Friday run |
| Social | social.md | Wednesday run |
| Strategy | strategy.md | Thursday run |

The sales meeting (Friday 2:47pm) reads them all. A missing report is reported as a problem.

## Template (keep it under ~30 lines, plain Australian English)
```
# <Department> - week ending <date>
## Headline
One line: the most important thing this week.
## Done this week
Numbers first (sent, opened, logos found, posts written, ideas researched...).
## Results
What happened because of it, measured against the target of 2 new sales a month.
## Working / not working
Plainly. Say when the sample is too small to judge.
## Problems
Anything that failed or blocked us, and what was done.
## Recommendations
1-3 ideas from this department, each with why and cost.
## Needed from Paul
At most one thing.
## Next week
What this department will do.
```

## Sales meeting outputs
1. One Claude Doc "AOF sales meeting - <date>" with: the department reports (each in full), the conclusion
   report, and the meeting minutes (filled in once Paul has answered).
2. `meetings/<date>.md`: the minutes (attendees, items, decisions, actions with who and when).

## Opens and clicks (Paul, 27 Nov 2026) - in the Email report and the conclusion every week
Per business sent this week and still open: business, first email (sent / opened / clicked), follow-up
(sent / opened / clicked), replied y/n. Read them this way:
- CLICKED (tapped "See the apps" or a button) = real interest. Rank the visit list on clicks and replies.
- OPENED = maybe. Paul's BCC copy is the same email, so his opening it marks it "opened"; Apple Mail and spam
  filters can also auto-open. Say this in one line under the table.
- Deleted can't be tracked by any email system.
