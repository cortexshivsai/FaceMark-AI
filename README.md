# 🎯 FaceMark AI - Intelligent Facial Recognition Attendance System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/OpenCV-Computer%20Vision-green?style=for-the-badge&logo=opencv"/>
  <img src="https://img.shields.io/badge/Face%20Recognition-AI-orange?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Status-Completed-success?style=for-the-badge"/>
</p>

<p align="center">
An AI-powered attendance management system that uses facial recognition to automatically identify individuals and record attendance in real time.
</p>

---

## 📖 Overview

**FaceMark AI** is a smart attendance system built using **Python**, **OpenCV**, and the **face_recognition** library. The system detects faces from a live webcam feed, compares them with registered users, and automatically records attendance.

This project demonstrates the practical use of **Computer Vision**, **Face Recognition**, and **Python automation**.

---

# ✨ Features

- 📷 Real-time webcam face detection
- 🧠 AI-based facial recognition
- 👤 Automatic person identification
- 📝 Automatic attendance recording
- ⚡ Fast face encoding for efficient recognition
- 📁 Attendance stored in CSV format
- 🔒 Prevents duplicate attendance entries
- 🎯 Easy to add new registered users

---

# 🛠️ Tech Stack

| Technology | Usage |
|------------|-------|
| Python | Programming Language |
| OpenCV | Image Processing |
| face_recognition | Facial Recognition |
| NumPy | Numerical Operations |
| CSV | Attendance Storage |
| Datetime | Timestamp Generation |

---

# 📂 Project Structure

```
FaceMark-AI/
│
├── imgattendance/
│   ├── Shivsai.jpg
│   ├── Alok.jpg
│   ├── Satyam.jpg
│   └── ...
│
├── attendance.csv
├── main.py
├── requirements.txt
├── README.md
└── screenshots/
```

---

# ⚙️ Installation

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/facemark-ai.git
```

```bash
cd facemark-ai
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually install:

```bash
pip install opencv-python
pip install face-recognition
pip install numpy
```

---

## 3️⃣ Add Known Faces

Place all registered users inside the **imgattendance** folder.

Example:

```
imgattendance/
│
├── Rahul.jpg
├── Shivsai.jpg
├── Alok.jpg
```

The filename becomes the person's name.

---

## 4️⃣ Run the Project

```bash
python main.py
```

---

# 📷 How It Works

1. Load known face images.
2. Encode all registered faces.
3. Open webcam.
4. Detect faces in real time.
5. Compare detected face with known encodings.
6. Recognize the person.
7. Record attendance with timestamp.
8. Prevent duplicate attendance entries.

---

# 📊 Sample Attendance

| Name | Date | Time |
|------|------|------|
| SHIVSAI | 2026-08-04 | 09:20:18 |
| ALOK | 2026-08-04 | 09:22:44 |
| SATYAM | 2026-08-04 | 09:25:03 |

---

# 🚀 Future Improvements

- ✅ SQLite/MySQL Database
- ✅ Streamlit Dashboard
- ✅ Flask Web Application
- ✅ Face Registration Module
- ✅ Admin Login
- ✅ Attendance Reports (PDF/Excel)
- ✅ Email Notifications
- ✅ Anti-Spoofing Detection
- ✅ Multi-Face Attendance
- ✅ Cloud Deployment

---

# 📸 Screenshots

Add screenshots here.

```
screenshots/

home.png

recognition.png

attendance.png
```

---

# 💡 Learning Outcomes

This project helped in understanding:

- Computer Vision
- Face Recognition
- Image Encoding
- Real-time Video Processing
- Python File Handling
- AI-based Attendance Systems

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Added new feature"
```

4. Push the branch

```bash
git push origin feature-name
```

5. Open a Pull Request

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

---

# 👨‍💻 Author

**Shivsai Jagadale**

🎓 B.Tech AIML Student

💻 Python Developer

🤖 Aspiring AI Engineer

📫 GitHub: https://github.com/shivsai1396

---

## 📄 License

This project is licensed under the MIT License.
