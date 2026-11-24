"""Mark a row: python3 campaign/mark.py <address> <sent|skipped|no-thanks|bounced|queued> [note]"""
import csv, sys, os, datetime
Q = os.path.join(os.path.dirname(__file__), "queue.csv")
addr, status = sys.argv[1].lower(), sys.argv[2]
note = " ".join(sys.argv[3:])
rows = list(csv.DictReader(open(Q))); fields = list(rows[0].keys()); hit = 0
for r in rows:
    if r["to"].lower() == addr:
        r["status"] = status; hit += 1
        if status == "sent": r["sent_date"] = datetime.date.today().isoformat()
        if note: r["notes"] = note
with open(Q, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, restval=""); w.writeheader(); w.writerows(rows)
print("updated", hit)
