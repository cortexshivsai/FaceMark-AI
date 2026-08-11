# FaceMark AI 🎯

> AI-powered face recognition attendance management system built with Python, OpenCV, Face Recognition, MySQL, and CustomTkinter.

FaceMark AI is a desktop-based attendance management system that uses **facial recognition** to identify registered students and automatically record their attendance in a **MySQL database**.

The application provides a modern GUI dashboard for monitoring students, attendance records, attendance statistics, and the face recognition system.

---

## ✨ Features

### 🤖 Face Recognition
- Real-time face detection using webcam
- Face recognition using `face_recognition`
- Multiple known faces supported
- Face distance calculation for recognition confidence
- Unknown faces are displayed as `UNKNOWN`
- Green bounding box for recognized students
- Red bounding box for unknown faces

### 📊 Dashboard
- Total students count
- Present students count
- Today's attendance percentage
- MySQL connection status
- Face recognition system status

### 👥 Student Management
- View registered students
- Student ID and name management
- MySQL-based student records

### 📝 Attendance Management
- Automatically records recognized students
- Attendance date and time
- Attendance hour tracking
- Attendance status
- Recognition confidence
- Prevents duplicate attendance within the same hour

### 🔎 Attendance Search
- Search attendance by:
  - Student ID
  - Student name
- View attendance records from the database

### 🖥️ Desktop GUI
- Built with CustomTkinter
- Modern dark-themed interface
- Sidebar navigation
- Dashboard
- Students
- Attendance
- Face Recognition
- Reports

### 🔐 Secure Configuration
- Database credentials stored using environment variables
- `.env` excluded from Git using `.gitignore`

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| OpenCV | Webcam and image processing |
| Face Recognition | Face detection and recognition |
| NumPy | Numerical and face-distance calculations |
| MySQL | Database management |
| MySQL Connector | Python-MySQL connection |
| CustomTkinter | Desktop GUI |
| Pillow | Image handling |
| python-dotenv | Environment variable management |

---

## 📂 Project Structure

```text
FaceMark-AI/
│
├── gui.py
├── main.py
├── database.py
├── dashboard.py
├── attendance.py
│
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
│
├── imgattendance/
│   └── face images
│
└── .env
