import csv
from datetime import date, datetime, time, timedelta

# DEFINE ACTIVITIES AND INITIAL TIME OFFSET
ACTIVITIES = [("Echo Location", 30), ("Feed Sharing", 10), ("Feed Favorites", 20), ("Feed Recommendations", 20)]
INITIAL_OFFSET = 20         # 10 OR 20 MINUTES
TOTAL_LENGTH = 100          # TOTAL LENGTH OF SESSION

# PREPROCESS
td = date.today()
acc = INITIAL_OFFSET
activities = []
for a, t in ACTIVITIES:
    acc += t
    activities.append((a, acc))

# READ AND WRITE TO CSV
with open("input_data.csv", "r") as f:
    with open("output_times.csv", "w") as f2:
        c = csv.reader(f)
        for row in c:
            t1 = row[1].split("-")[1]
            is_pm = bool("pm" in t1.lower())
            t1 = t1[:-2]
            t1 = t1.split(":")
            t1_hours, t1_mins = int(t1[0]), int(t1[1])
            if is_pm and t1_hours != 12:
                t1_hours += 12
            f2.write("EST Time, PST Time\n")
            i = 0
            for activity, offset in activities:
                delta = offset - TOTAL_LENGTH
                delta_start = offset - TOTAL_LENGTH - ACTIVITIES[i][1]
                t = time(t1_hours, t1_mins)
                dt_est_start = datetime.combine(td, t) + timedelta(minutes=delta_start)
                dt_est_end = datetime.combine(td, t) + timedelta(minutes=delta)
                dt_pst_start = datetime.combine(td, t) + timedelta(minutes=delta_start - 180)
                dt_pst_end = datetime.combine(td, t) + timedelta(minutes=delta - 180)
                dt_est_start = dt_est_start.strftime('%I:%M%p')
                dt_est_end = dt_est_end.strftime('%I:%M%p')
                dt_pst_start = dt_pst_start.strftime('%I:%M%p')
                dt_pst_end = dt_pst_end.strftime('%I:%M%p')
                f2.write(f"\"{dt_est_start}-{dt_est_end}\"")
                f2.write(f",\"{dt_pst_start}-{dt_pst_end}\"\n")
                i += 1
