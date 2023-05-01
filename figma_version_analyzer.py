import requests
import csv
import os
from datetime import datetime, timedelta
import pytz
import argparse

def ftime(iso8601):
    utc_dt = datetime.fromisoformat(iso8601).replace(tzinfo=pytz.utc)
    gmt8 = pytz.timezone("Australia/Perth")  # Change this to your desired timezone
    local_dt = utc_dt.astimezone(gmt8)
    return local_dt, local_dt.strftime("%Y-%m-%d %H:%M:%S")

def fetch_version_history(headers, all_versions, file_id):
    file_url = f"https://api.figma.com/v1/files/{file_id}/versions"

    next_page = None

    url = file_url

    while True:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            all_versions.extend(data["versions"])

            if "next_page" in data["pagination"]:
                url = data["pagination"]["next_page"]
            else:
                break
        else:
            print("Error fetching version history:", response.status_code)
            break

    return all_versions

def save_version_history_to_csv(version_history, csvfile, dailyfile):
    daily_data = {}

    writer = csv.DictWriter(csvfile, fieldnames=["id", "created_at", "label", "description", "user"])
    writer.writeheader()

    for version in version_history:
        dt, dts = ftime(version["created_at"])
        day = dt.date()

        if day not in daily_data:
            daily_data[day] = {"start": dt, "end": dt, "count": 1}
        else:
            if dt < daily_data[day]["start"]:
                daily_data[day]["start"] = dt
            if dt > daily_data[day]["end"]:
                daily_data[day]["end"] = dt

        daily_data[day]["count"] += 1

        writer.writerow({"id": version["id"], "created_at": dts, "label": version["label"], "description": version["description"], "user": version["user"]["handle"]})

    writer = csv.DictWriter(dailyfile, fieldnames=["day", "start_time", "end_time", "change count", "duration"])
    writer.writeheader()

    for day, times in daily_data.items():
        duration_seconds = (times["end"] - times["start"]).total_seconds()
        duration_timedelta = timedelta(seconds=duration_seconds)
        duration_str = str(duration_timedelta // timedelta(hours=1)) + ":" + "{:02d}".format((duration_timedelta % timedelta(hours=1)).seconds // 60)
        writer.writerow({"day": day, "start_time": times["start"].strftime("%Y-%m-%d %H:%M:%S"), "end_time": times["end"].strftime("%Y-%m-%d %H:%M:%S"), "change count": times["count"], "duration": duration_str})

    return daily_data

def main(api_key, file_ids):
    headers = {"X-Figma-Token": api_key}
    all_versions = []

    with open("daily_data.csv", "w", newline="", encoding="utf-8") as dailyfile:
        with open("raw_data.csv", "w", newline="", encoding="utf-8") as csvfile:
            for fileid in file_ids:
                all_versions = fetch_version_history(headers, all_versions, fileid)
            save_version_history_to_csv(all_versions, csvfile, dailyfile)
    print("Figma version history has been saved to 'daily_data.csv'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retrieve Figma version history for a list of files.")
    parser.add_argument("api_key", help="Figma API key")
    parser.add_argument("file_ids", nargs="+", help="List of Figma file IDs")

    args = parser.parse_args()

    main(args.api_key, args.file_ids)