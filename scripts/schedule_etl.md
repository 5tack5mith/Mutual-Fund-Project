# B1 — Scheduled ETL Pipeline

## Overview
The ETL pipeline is scheduled to auto-fetch live NAV data from mfapi.in 
every weekday at 8:00 PM using Windows Task Scheduler.

## Schedule Details
- **Task Name:** Bluestock NAV Fetch
- **Schedule:** Monday to Friday, 8:00 PM
- **Script:** scripts/etl_pipeline.py
- **Python:** Python 3.14

## To recreate the scheduled task
Run this command in Command Prompt as Administrator:

```cmd
schtasks /create /tn "Bluestock NAV Fetch" /tr "C:\Users\samya\AppData\Local\Python\pythoncore-3.14-64\python.exe C:\Users\samya\mutual_fund_project\scripts\etl_pipeline.py" /sc weekly /d MON,TUE,WED,THU,FRI /st 20:00 /f
```

## To verify the task exists
```cmd
schtasks /query /tn "Bluestock NAV Fetch"
```

## To run manually
```cmd
py -3.14 scripts/etl_pipeline.py
```

## What it does
Fetches live NAV data for 6 key mutual fund schemes from mfapi.in REST API 
and saves updated CSVs to data/raw/ folder automatically every weekday evening.