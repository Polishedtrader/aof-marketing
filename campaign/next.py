"""Print the next queued email (or the one for an email address): python3 campaign/next.py [address]"""
import csv, sys, os
Q = os.path.join(os.path.dirname(__file__), "queue.csv")
rows = list(csv.DictReader(open(Q)))
want = sys.argv[1].lower() if len(sys.argv) > 1 else None
for r in rows:
    if (want and r["to"].lower() == want) or (not want and r["status"] == "queued"):
        print("\n".join(f"{k}: {v}" for k, v in r.items()))
        left = sum(1 for x in rows if x["status"] == "queued")
        print(f"queued_left: {left}  sent_so_far: {sum(1 for x in rows if x['status'] == 'sent')}")
        break
else:
    print("NONE: nothing queued")
