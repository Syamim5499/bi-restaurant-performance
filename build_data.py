#!/usr/bin/env python3
"""Rebuild the embedded dashboard data from the public seaborn-data sample."""
import csv
import hashlib
import io
import json
import urllib.request
from collections import defaultdict
from pathlib import Path

KIND = "tips"
EXPECTED_BLOB_SHA = "1280a10886c1f858b29c1be1740619cdef3d6be1"
URL = f"https://raw.githubusercontent.com/mwaskom/seaborn-data/master/{KIND}.csv"

raw = urllib.request.urlopen(URL, timeout=30).read()
git_blob_sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
if git_blob_sha != EXPECTED_BLOB_SHA:
    raise SystemExit("Source file changed; review the new version before refreshing the dashboard.")
records = list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
if KIND == "flights":
    result = [{"year": int(r["year"]), "month": r["month"], "passengers": int(r["passengers"])} for r in records]
elif KIND == "tips":
    result = [{"bill": float(r["total_bill"]), "tip": float(r["tip"]), "sex": r["sex"],
               "smoker": r["smoker"], "day": r["day"], "time": r["time"], "size": int(r["size"])}
              for r in records]
else:
    groups = {}
    for r in records:
        pickup = r["pickup"]
        if not pickup or len(pickup) < 13:
            continue
        date, hour = pickup[:10], int(pickup[11:13])
        borough, payment = r["pickup_borough"] or "Unknown", r["payment"] or "Unknown"
        key = (date, hour, borough, payment)
        if key not in groups:
            groups[key] = {"date": date, "hour": hour, "borough": borough, "payment": payment,
                           "trips": 0, "fare": 0, "tip": 0, "total": 0, "distance": 0}
        g = groups[key]
        g["trips"] += 1
        for field in ("fare", "tip", "total", "distance"):
            if r[field]:
                g[field] += float(r[field])
    result = list(groups.values())
    for g in result:
        for field in ("fare", "tip", "total", "distance"):
            g[field] = round(g[field], 2)
Path(__file__).with_name("data.js").write_text("window.DATA=" + json.dumps(result, separators=(",", ":")) + ";", encoding="utf-8")
print(f"Prepared {len(result)} dashboard rows from {len(records)} source rows.")
