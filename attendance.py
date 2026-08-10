import csv
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()


# ========================================
# DATABASE CONNECTION
# ========================================

def create_connection():
    try:
        connection = mysql.connector.connect(
           host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            print("MySQL database connected successfully!")
            return connection

    except Error as e:
        print("Database connection error:", e)

    return None


# ========================================
# VIEW ALL ATTENDANCE
# ========================================

def get_all_attendance():

    connection = create_connection()

    if connection is None:
        return []

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            a.id,
            s.student_id,
            s.name,
            a.attendance_date,
            a.attendance_time,
            a.attendance_hour,
            a.status,
            a.confidence
        FROM attendance a
        JOIN students s
            ON a.student_id = s.id
        ORDER BY a.id DESC
        """

        cursor.execute(query)

        attendance_records = cursor.fetchall()

        cursor.close()
        connection.close()

        return attendance_records

    except Error as e:
        print("Error fetching attendance:", e)

        if connection.is_connected():
            connection.close()

        return []


# ========================================
# DISPLAY ALL ATTENDANCE
# ========================================

def display_all_attendance():

    print("\n")
    print("=" * 100)
    print("                         ATTENDANCE RECORDS")
    print("=" * 100)

    records = get_all_attendance()

    if not records:
        print("No attendance records found.")
        return

    print(
        f"{'ID':<5}"
        f"{'STUDENT ID':<15}"
        f"{'NAME':<15}"
        f"{'DATE':<15}"
        f"{'TIME':<12}"
        f"{'HOUR':<8}"
        f"{'STATUS':<10}"
        f"{'CONFIDENCE':<12}"
    )

    print("-" * 100)

    for record in records:

        confidence = record["confidence"]

        if confidence is not None:
            confidence = f"{float(confidence):.2f}"
        else:
            confidence = "N/A"

        print(
            f"{record['id']:<5}"
            f"{record['student_id']:<15}"
            f"{record['name']:<15}"
            f"{str(record['attendance_date']):<15}"
            f"{str(record['attendance_time']):<12}"
            f"{record['attendance_hour']:<8}"
            f"{record['status']:<10}"
            f"{confidence:<12}"
        )

    print("=" * 100)

# ========================================
# SEARCH ATTENDANCE
# ========================================

def search_attendance(search_value):

    connection = create_connection()

    if connection is None:
        return

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            a.id,
            s.student_id,
            s.name,
            a.attendance_date,
            a.attendance_time,
            a.attendance_hour,
            a.status,
            a.confidence
        FROM attendance a
        JOIN students s
            ON a.student_id = s.id
        WHERE
            LOWER(s.student_id) = LOWER(%s)
            OR LOWER(s.name) = LOWER(%s)
        ORDER BY a.id DESC
        """

        cursor.execute(
            query,
            (search_value, search_value)
        )

        records = cursor.fetchall()

        cursor.close()
        connection.close()

        if not records:
            print("\nNo attendance records found.")
            return

        print("\n")
        print("=" * 90)
        print("                    SEARCH RESULTS")
        print("=" * 90)

        print(
            f"{'ID':<5}"
            f"{'STUDENT ID':<15}"
            f"{'NAME':<15}"
            f"{'DATE':<15}"
            f"{'TIME':<12}"
            f"{'HOUR':<8}"
            f"{'STATUS':<10}"
        )

        print("-" * 90)

        for record in records:

            print(
                f"{record['id']:<5}"
                f"{record['student_id']:<15}"
                f"{record['name']:<15}"
                f"{str(record['attendance_date']):<15}"
                f"{str(record['attendance_time']):<12}"
                f"{record['attendance_hour']:<8}"
                f"{record['status']:<10}"
            )

        print("=" * 90)

    except Error as e:

        print("Search error:", e)

        if connection.is_connected():
            connection.close()

# ========================================
# VIEW ATTENDANCE BY DATE
# ========================================

def attendance_by_date(selected_date):

    connection = create_connection()

    if connection is None:
        return

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            a.id,
            s.student_id,
            s.name,
            a.attendance_date,
            a.attendance_time,
            a.attendance_hour,
            a.status,
            a.confidence
        FROM attendance a
        INNER JOIN students s
            ON a.student_id = s.id
        WHERE a.attendance_date = %s
        ORDER BY a.attendance_time ASC
        """

        cursor.execute(query, (selected_date,))

        records = cursor.fetchall()

        cursor.close()
        connection.close()

        if not records:
            print(f"\nNo attendance records found for {selected_date}.")
            return

        print("\n")
        print("=" * 100)
        print(f"                 ATTENDANCE FOR {selected_date}")
        print("=" * 100)

        print(
            f"{'ID':<5}"
            f"{'STUDENT ID':<15}"
            f"{'NAME':<15}"
            f"{'DATE':<15}"
            f"{'TIME':<12}"
            f"{'HOUR':<8}"
            f"{'STATUS':<10}"
        )

        print("-" * 100)

        for record in records:

            print(
                f"{record['id']:<5}"
                f"{record['student_id']:<15}"
                f"{record['name']:<15}"
                f"{str(record['attendance_date']):<15}"
                f"{str(record['attendance_time']):<12}"
                f"{record['attendance_hour']:<8}"
                f"{record['status']:<10}"
            )

        print("=" * 100)

    except Error as e:

        print("Date search error:", e)

        if connection.is_connected():
            connection.close()

# ========================================
# STUDENT ATTENDANCE HISTORY
# ========================================

def student_attendance_history(student_value):

    connection = create_connection()

    if connection is None:
        return

    try:
        cursor = connection.cursor(dictionary=True)

        # Find student
        student_query = """
        SELECT
            id,
            student_id,
            name
        FROM students
        WHERE
            student_id LIKE %s
            OR name LIKE %s
        """

        search_pattern = f"%{student_value}%"

        cursor.execute(
            student_query,
            (search_pattern, search_pattern)
        )

        student = cursor.fetchone()

        if student is None:

            print(
                f"\nNo student found for: {student_value}"
            )

            cursor.close()
            connection.close()

            return

        # Get attendance records
        attendance_query = """
        SELECT
            attendance_date,
            attendance_time,
            attendance_hour,
            status
        FROM attendance
        WHERE student_id = %s
        ORDER BY attendance_date DESC,
                 attendance_time DESC
        """

        cursor.execute(
            attendance_query,
            (student["id"],)
        )

        records = cursor.fetchall()

        print("\n")
        print("=" * 70)
        print("             STUDENT ATTENDANCE HISTORY")
        print("=" * 70)

        print(f"Student ID : {student['student_id']}")
        print(f"Name       : {student['name']}")

        print("\n")
        print(
            f"{'DATE':<15}"
            f"{'TIME':<12}"
            f"{'HOUR':<8}"
            f"{'STATUS':<10}"
        )

        print("-" * 50)

        present_count = 0

        for record in records:

            if record["status"] == "Present":
                present_count += 1

            print(
                f"{str(record['attendance_date']):<15}"
                f"{str(record['attendance_time']):<12}"
                f"{record['attendance_hour']:<8}"
                f"{record['status']:<10}"
            )

        total_records = len(records)

        if total_records > 0:

            percentage = (
                present_count / total_records
            ) * 100

        else:

            percentage = 0

        print("-" * 50)

        print(f"Total Records : {total_records}")
        print(f"Present       : {present_count}")
        print(f"Attendance    : {percentage:.2f}%")

        print("=" * 70)

        cursor.close()
        connection.close()

    except Error as e:

        print("Attendance history error:", e)

        if connection.is_connected():
            connection.close()

# ========================================
# ATTENDANCE DASHBOARD
# ========================================

def attendance_dashboard():

    connection = create_connection()

    if connection is None:
        return

    try:
        cursor = connection.cursor(dictionary=True)

        # ----------------------------------------
        # TOTAL STUDENTS
        # ----------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total_students
            FROM students
        """)

        total_students = cursor.fetchone()["total_students"]

        # ----------------------------------------
        # TODAY'S UNIQUE PRESENT STUDENTS
        # ----------------------------------------

        cursor.execute("""
            SELECT COUNT(DISTINCT student_id) AS present_students
            FROM attendance
            WHERE attendance_date = CURDATE()
        """)

        present_students = cursor.fetchone()["present_students"]

        # ----------------------------------------
        # TODAY'S TOTAL ATTENDANCE RECORDS
        # ----------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total_records
            FROM attendance
            WHERE attendance_date = CURDATE()
        """)

        total_records = cursor.fetchone()["total_records"]

        # ----------------------------------------
        # TODAY'S ATTENDANCE PERCENTAGE
        # ----------------------------------------

        if total_students > 0:
            attendance_percentage = (
                present_students / total_students
            ) * 100
        else:
            attendance_percentage = 0

        # ----------------------------------------
        # DISPLAY DASHBOARD
        # ----------------------------------------

        print("\n")
        print("=" * 60)
        print("              ATTENDANCE DASHBOARD")
        print("=" * 60)

        print(f"Total Students       : {total_students}")
        print(f"Today's Present      : {present_students}")
        print(f"Today's Records      : {total_records}")
        print(
            f"Today's Attendance   : "
            f"{attendance_percentage:.2f}%"
        )

        print("=" * 60)

        # ----------------------------------------
        # HOURLY ATTENDANCE
        # ----------------------------------------

        cursor.execute("""
            SELECT
                attendance_hour,
                COUNT(DISTINCT student_id) AS students_present
            FROM attendance
            WHERE attendance_date = CURDATE()
            GROUP BY attendance_hour
            ORDER BY attendance_hour
        """)

        hourly_records = cursor.fetchall()

        print("\n========== HOURLY ATTENDANCE ==========")

        if hourly_records:

            print(
                f"{'HOUR':<10}"
                f"{'STUDENTS PRESENT':<20}"
            )

            print("-" * 30)

            for record in hourly_records:

                print(
                    f"{record['attendance_hour']:<10}"
                    f"{record['students_present']:<20}"
                )

        else:

            print("No attendance recorded today.")

        print("=" * 60)

        cursor.close()
        connection.close()

    except Error as e:

        print("Dashboard error:", e)

        if connection.is_connected():
            connection.close()

# ========================================
# EXPORT ATTENDANCE TO CSV
# ========================================

def export_attendance_csv():

    connection = create_connection()

    if connection is None:
        return

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            s.student_id,
            s.name,
            s.department,
            s.year,
            a.attendance_date,
            a.attendance_time,
            a.attendance_hour,
            a.status,
            a.confidence
        FROM attendance a
        INNER JOIN students s
            ON a.student_id = s.id
        ORDER BY
            a.attendance_date DESC,
            a.attendance_time DESC
        """

        cursor.execute(query)

        records = cursor.fetchall()

        cursor.close()
        connection.close()

        if not records:
            print("\nNo attendance records available to export.")
            return

        filename = "attendance_report.csv"

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            # CSV header
            writer.writerow([
                "Student ID",
                "Name",
                "Department",
                "Year",
                "Date",
                "Time",
                "Hour",
                "Status",
                "Face Distance"
            ])

            # CSV data
            for record in records:

                writer.writerow([
                    record["student_id"],
                    record["name"],
                    record["department"],
                    record["year"],
                    record["attendance_date"],
                    record["attendance_time"],
                    record["attendance_hour"],
                    record["status"],
                    record["confidence"]
                ])

        print("\n========================================")
        print("ATTENDANCE REPORT EXPORTED SUCCESSFULLY")
        print("========================================")
        print(f"File: {filename}")
        print(f"Records exported: {len(records)}")
        print("========================================")

    except Error as e:

        print("Export error:", e)

        if connection.is_connected():
            connection.close()

    except Exception as e:

        print("File error:", e)

# ========================================
# MAIN
# ========================================

if __name__ == "__main__":

    print("\n===== ATTENDANCE MANAGEMENT =====")

    print("\n1. View All Attendance")
    print("2. Search Attendance")
    print("3. View Attendance by Date")
    print("4. Student Attendance History")
    print("5. Attendance Dashboard")
    print("6. Export Attendance to CSV")

    choice = input("\nEnter your choice: ")

    if choice == "1":

        display_all_attendance()

    elif choice == "2":

        search_value = input(
            "Enter Student ID or Student Name: "
        )

        search_attendance(search_value)

    elif choice == "3":

        selected_date = input(
            "Enter date (YYYY-MM-DD): "
        )

        attendance_by_date(selected_date)

    elif choice == "4":

        student_value = input(
            "Enter Student ID or Student Name: "
        )

        student_attendance_history(student_value)

    elif choice == "5":

        attendance_dashboard()

    elif choice == "6":

        export_attendance_csv()

    else:

        print("Invalid choice.")