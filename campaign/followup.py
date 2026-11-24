"""Follow-up email, 3 working days after Email 1 (template approved by Paul 18 Nov 2026, no daily sign-off needed).
  python3 campaign/followup.py <address>              builds campaign/followups/<html_file>, prints subject + send time
  python3 campaign/followup.py <address> --id <id>    records the Resend email id (to cancel it later)
  python3 campaign/followup.py <address> --cancelled  records that it was cancelled
"""
import csv, sys, os, datetime, subprocess
from zoneinfo import ZoneInfo
D = os.path.dirname(os.path.abspath(__file__)); Q = os.path.join(D, "queue.csv")
rows = list(csv.DictReader(open(Q))); fields = list(rows[0].keys())
for c in ("follow_date", "follow_id"):
    if c not in fields: fields.append(c)
addr = sys.argv[1].lower(); row = next((r for r in rows if r["to"].lower() == addr), None)
if not row: sys.exit("not in queue: " + addr)
def save():
    with open(Q, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, restval=""); w.writeheader(); w.writerows(rows)
if "--id" in sys.argv:
    row["follow_id"] = sys.argv[sys.argv.index("--id") + 1]; save(); print("recorded"); sys.exit()
if "--cancelled" in sys.argv:
    row["follow_id"] = "cancelled " + (row.get("follow_id") or ""); save(); print("recorded"); sys.exit()
d = datetime.date.today(); n = 0
while n < 3:
    d += datetime.timedelta(days=1)
    if d.weekday() < 5: n += 1
at = datetime.datetime(d.year, d.month, d.day, 8, 30, tzinfo=ZoneInfo("Australia/Sydney"))
os.makedirs(os.path.join(D, "followups"), exist_ok=True)
out = os.path.join(D, "followups", row["html_file"])
subj = subprocess.run([sys.executable, os.path.join(D, "build_apps.py"), "--follow", addr, out],
                      capture_output=True, text=True, check=True).stdout.strip().splitlines()[-1]
row["follow_date"] = d.isoformat(); save()
print(f"to: {row['to']}\nsubject: {subj}\nhtml_file: {out}\nscheduledAt: {at.isoformat()}")
