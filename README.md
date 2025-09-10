<<<<<<< HEAD
# e_notice_board
=======
# E-Notice Board

E-Notice Board is a web-based application built with **Flask** for managing monitors and notices. It allows administrators to create, edit, and assign notices to specific monitors, and displays notices on virtual monitors with scheduling, priority, and status control.

---

## Features

### Admin Panel
- Login/logout system.
- Add, edit, and delete monitors.
- Add, edit, and delete notices.
- Assign notices to one or multiple monitors.
- Set notice priority, display position, duration, and active status.
- Check and deactivate expired notices automatically.
- View monitor status including assigned notices.

### Monitor Display
- Active monitors display assigned notices.
- Notices are displayed based on priority, position, and duration.
- API endpoint available for fetching monitor-specific notice data.

---

## Project Structure
```
e_notice_board/
│
├─ app.py # Main Flask application
├─ models.py # SQLAlchemy models
├─ routes/
│ ├─ admin_routes.py # Admin routes (login, dashboard, manage monitors/notices)
│ ├─ monitor_routes.py # Monitor routes (status, display, API)
│ └─ modify.py # Monitor CRUD operations
├─ templates/
│ ├─ admin/
│ │ ├─ add_monitor.html
│ │ ├─ edit_monitor.html
│ │ ├─ list_monitors.html
│ │ ├─ edit_notice.html
│ │ └─ list_notices.html
│ └─ monitor/
│ ├─ status.html
│ └─ display.html
├─ static/
│ ├─ css/
│ │ └─ style.css
│ └─ js/
├─ .myenv/ # Python virtual environment
└─ requirements.txt # Python dependencies
```
some additional file for testing checking ignore that all files 

---

## Installation

### 1. Clone the repository:

```bash
git clone <your-repo-url>
```
```
cd e_notice_board
```
### 2. Install dependencies:
```bash
pip install -r requirements.txt
```
### 3. Run the application:
```bash
python app.py
```
#### Open your browser and navigate to click(http://127.0.0.1:5000)

## DEVELOPED BY ARYAN RANA // @mr-aryan-rana
>>>>>>> d38df03 (created.....)
