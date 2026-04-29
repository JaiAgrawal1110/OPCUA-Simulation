# 🏭 OPC UA CNC Machine Monitor

A real-time web dashboard for monitoring CNC machine data using the OPC UA protocol — built during my internship. The dashboard pulls live data from CNC machines every 2 seconds and displays it on a local web interface with filtering options based on machine status.

---

## 🚀 Features

- **Real-time data** — fetches live CNC machine data every 2 seconds via OPC UA
- **Monitored parameters** — Temperature, Spindle Speed, and Machine Status
- **Status-based filtering** — users can filter the dashboard view by machine status (e.g. Running, Idle, Error)
- **Live dashboard** — clean web interface built with HTML, CSS, and JavaScript
- **Django backend** — handles OPC UA communication and serves data to the frontend
- **Multi-database support** — data stored in MongoDB and MySQL

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Django |
| Frontend | HTML, CSS, JavaScript |
| Protocol | OPC UA (`opcua` / `asyncua` library) |
| Database | MongoDB, MySQL, SQLite |
| Data | Real CNC machine data (internship environment) |

---

## 📊 Dashboard Overview

The web dashboard shows live CNC machine metrics that refresh every 2 seconds:

- **Temperature** — real-time thermal readings from machines
- **Spindle Speed** — current RPM of the CNC spindle
- **Status** — machine state (Running / Idle / Error)

Users can filter the view to show only machines in a specific status — for example, showing only machines in an **Error** state for quick diagnostics.

---

## ⚙️ Setup & Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/opcua-cnc-monitor.git
cd opcua-cnc-monitor

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the server
python manage.py runserver
```

Then open your browser and go to `http://127.0.0.1:8000`

---

## 📁 Project Structure

```
opcua-cnc-monitor/
│
├── manage.py
├── db.sqlite3
├── requirements.txt
├── README.md
│
├── Home/                         # Main Django app
│   ├── backend/
│   │   ├── cnc_to_opcua.py       # Reads CNC data via OPC UA protocol
│   │   ├── display_data.py       # Processes and formats data for frontend
│   │   ├── mongoDB_insert.py     # Inserts data into MongoDB
│   │   └── mysql_insert.py       # Inserts data into MySQL
│   ├── views.py                  # Django views
│   ├── urls.py
│   ├── models.py
│   ├── admin.py
│   └── apps.py
│
├── OPCUA/                        # Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── static/                       # CSS, JS files
└── templates/                    # HTML templates
```

---

## 📝 Notes

- This project was built during an internship using **real CNC machine data** in a controlled industrial environment
- OPC UA server address and node IDs are not included for security reasons — configure them in your local settings
- Database credentials should be added to a `.env` file and never committed to GitHub
- Data refresh interval is set to **2 seconds** by default

---

## 👨‍💻 Author

**Jai Agrawal** — Internship Project
