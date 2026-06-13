# 🏭 OPC UA CNC Machine Monitor

> Real-time CNC machine monitoring dashboard built during my internship at INDXO — streams historical machine telemetry from MongoDB via OPC UA protocol and displays it on a live web dashboard refreshing every 2 seconds.

---

> **The problem:** Factory floor engineers needed a way to monitor CNC machine health (temperature, spindle speed, status) at a glance without manually querying the database. This dashboard simulates live telemetry by streaming 1000s of historical CNC records from MongoDB through an OPC UA layer, mimicking production machine monitoring.

---

## Key Numbers

| Metric | Value |
|--------|-------|
| Data source | MongoDB — 1000s of CNC machine records |
| Dashboard refresh rate | every 2 seconds |
| Monitored parameters | Temperature, Spindle Speed, Machine Status |
| Databases | MongoDB + MySQL |
| Deployment | Branch merged into INDXO core repository |

---

## What's Built

- **OPC UA simulation layer** — reads historical CNC records from MongoDB, publishes them as OPC UA nodes at 2-second intervals, mimicking live machine telemetry
- **Django backend** — polls the OPC UA server, processes data, writes to MySQL, and serves the frontend
- **Real-time dashboard** — auto-refreshing web interface showing live machine parameters
- **Status-based filtering** — filter view by machine state: Running / Idle / Error
- **Dual database pipeline** — MongoDB for time-series machine data, MySQL for structured relational records

---

## Architecture

```
MongoDB (1000s of historical CNC records)
    │
    ▼
cnc_to_opcua.py
    │  Reads records → publishes as OPC UA nodes
    ▼
OPC UA Server (asyncua)
    │  Exposes Temperature, SpindleSpeed, Status nodes
    ▼
Django Backend (views.py)
    │  Polls OPC UA every 2s
    │  Writes structured records → MySQL
    ▼
Live Dashboard (HTML / CSS / JS)
    │  Auto-refreshes every 2 seconds
    ▼
Status Filter → Running / Idle / Error
```

---

## Tech Stack — and Why

| Layer | Choice | Reasoning |
|-------|--------|-----------|
| Protocol | OPC UA (asyncua) | Industry standard for industrial machine communication; used in real CNC environments |
| Backend | Python · Django | Rapid development, clean ORM for MySQL, easy API serving |
| Time-series data | MongoDB | Flexible schema for heterogeneous machine telemetry records |
| Relational data | MySQL | Structured storage for machine metadata and session records |
| Frontend | HTML · CSS · JavaScript | Lightweight, no framework overhead for a dashboard that only needs polling |

---

## Project Structure

```
OPCUA-Simulation/
│
├── manage.py
├── requirements.txt
├── README.md
│
├── Home/                          # Main Django app
│   ├── backend/
│   │   ├── cnc_to_opcua.py        # Reads CNC data from MongoDB, publishes via OPC UA
│   │   ├── display_data.py        # Processes and formats data for frontend
│   │   ├── mongoDB_insert.py      # MongoDB read/write pipeline
│   │   └── mysql_insert.py        # MySQL insert pipeline
│   ├── views.py                   # Django views — serves dashboard data
│   ├── urls.py
│   ├── models.py
│   ├── admin.py
│   └── apps.py
│
├── OPCUA/                         # Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── static/                        # CSS, JS assets
└── templates/                     # HTML dashboard templates
```

---

## Quick Start

```bash
git clone https://github.com/JaiAgrawal1110/OPCUA-Simulation.git
cd OPCUA-Simulation

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

pip install -r requirements.txt

python manage.py runserver
```

Open `http://127.0.0.1:8000` in your browser.

> **Note:** OPC UA server address and node IDs are not included for security reasons. Configure them in your local `settings.py` or `.env` file.

---

## The Hardest Problem I Solved

**Keeping the OPC UA simulation in sync with the dashboard refresh cycle.**

The OPC UA layer reads records from MongoDB and publishes them as nodes, but the Django backend polls those nodes every 2 seconds independently. Early on, the backend would sometimes read a stale node value before the OPC UA layer had updated it, causing the dashboard to show duplicate readings. Fixed by adding a timestamp node alongside each data node — the backend checks the timestamp before accepting a reading, discarding any value older than the last successful poll.

---

## Notes

- Built at INDXO as part of backend engineering internship
- Code maintained on a dedicated branch and merged into the INDXO core repository
- Database credentials managed via `.env` — never committed to version control
- OPC UA is the industry standard protocol for industrial IoT and CNC environments; real factory deployments use the same protocol stack

---

MIT © 2026 Jai Agrawal — Internship Project, INDXO