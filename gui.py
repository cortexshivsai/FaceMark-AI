import customtkinter as ctk

from dashboard import (
    get_total_students,
    get_present_today,
    get_attendance_percentage
)
face_recognition_process = None


# ========================================
# APP SETTINGS
# ========================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ========================================
# MAIN APPLICATION
# ========================================

app = ctk.CTk()

app.title("FaceMark AI - Attendance Management System")
app.geometry("1200x700")
app.minsize(1000, 600)


# ========================================
# SIDEBAR
# ========================================

sidebar = ctk.CTkFrame(
    app,
    width=220,
    corner_radius=0
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)


# ========================================
# LOGO / TITLE
# ========================================

logo = ctk.CTkLabel(
    sidebar,
    text="FaceMark AI",
    font=ctk.CTkFont(
        size=26,
        weight="bold"
    )
)

logo.pack(
    pady=(40, 5)
)


subtitle = ctk.CTkLabel(
    sidebar,
    text="Attendance System",
    font=ctk.CTkFont(size=13)
)

subtitle.pack(
    pady=(0, 40)
)



# ========================================
# PAGE FUNCTIONS
# ========================================

def show_dashboard():
    header.configure(text="Dashboard")
    welcome.configure(
        text="Welcome to FaceMark AI Attendance Management System"
    )

    clear_content()

    stats_frame.pack(
        fill="x",
        pady=10
    )

    status_frame.pack(
        fill="x",
        pady=30
    )


def add_student():

    # Create popup window
    add_window = ctk.CTkToplevel(app)
    add_window.title("Add Student")
    add_window.geometry("450x500")
    add_window.resizable(False, False)

    # Title
    ctk.CTkLabel(
        add_window,
        text="Add New Student",
        font=ctk.CTkFont(size=24, weight="bold")
    ).pack(pady=(30, 25))

    # Student ID
    ctk.CTkLabel(
        add_window,
        text="Student ID",
        font=ctk.CTkFont(size=14)
    ).pack(anchor="w", padx=40)

    student_id_entry = ctk.CTkEntry(
        add_window,
        width=370,
        placeholder_text="e.g. SHIVSAI002"
    )
    student_id_entry.pack(pady=(5, 15))

    # Name
    ctk.CTkLabel(
        add_window,
        text="Name",
        font=ctk.CTkFont(size=14)
    ).pack(anchor="w", padx=40)

    name_entry = ctk.CTkEntry(
        add_window,
        width=370,
        placeholder_text="Enter student name"
    )
    name_entry.pack(pady=(5, 15))

    # Email
    ctk.CTkLabel(
        add_window,
        text="Email",
        font=ctk.CTkFont(size=14)
    ).pack(anchor="w", padx=40)

    email_entry = ctk.CTkEntry(
        add_window,
        width=370,
        placeholder_text="student@example.com"
    )
    email_entry.pack(pady=(5, 15))

    # Message
    message_label = ctk.CTkLabel(
        add_window,
        text="",
        font=ctk.CTkFont(size=13)
    )
    message_label.pack(pady=5)

    # Save student
    def save_student():

        student_id = student_id_entry.get().strip()
        name = name_entry.get().strip()
        email = email_entry.get().strip()

        # Validation
        if not student_id or not name or not email:

            message_label.configure(
                text="Please fill all fields."
            )

            return

        from database import create_connection

        connection = create_connection()

        if connection is None:

            message_label.configure(
                text="Database connection failed."
            )

            return

        try:

            cursor = connection.cursor()

            query = """
                INSERT INTO students
                (student_id, name, email)
                VALUES (%s, %s, %s)
            """

            cursor.execute(
                query,
                (student_id, name, email)
            )

            connection.commit()

            cursor.close()
            connection.close()

            message_label.configure(
                text="Student added successfully!"
            )

            # Refresh students page
            add_window.after(
                800,
                lambda: (
                    add_window.destroy(),
                    show_students()
                )
            )

        except Exception as e:

            print("Error adding student:", e)

            if connection.is_connected():
                connection.rollback()
                connection.close()

            message_label.configure(
                text="Could not add student."
            )

    # Button
    ctk.CTkButton(
        add_window,
        text="➕  Add Student",
        width=370,
        height=45,
        command=save_student
    ).pack(pady=20)


def search_students():

    search_window = ctk.CTkToplevel(app)
    search_window.title("Search Students")
    search_window.geometry("650x550")
    search_window.resizable(False, False)

    ctk.CTkLabel(
        search_window,
        text="Search Students",
        font=ctk.CTkFont(size=24, weight="bold")
    ).pack(pady=(25, 15))

    search_entry = ctk.CTkEntry(
        search_window,
        width=500,
        height=40,
        placeholder_text="Enter Student ID or Name"
    )
    search_entry.pack(pady=10)

    results_frame = ctk.CTkScrollableFrame(
        search_window,
        width=550,
        height=350
    )
    results_frame.pack(pady=15)

    def perform_search():

        # Clear previous results
        for widget in results_frame.winfo_children():
            widget.destroy()

        search_text = search_entry.get().strip()

        if not search_text:
            ctk.CTkLabel(
                results_frame,
                text="Enter a Student ID or Name."
            ).pack(pady=20)

            return

        from database import create_connection

        connection = create_connection()

        if connection is None:
            ctk.CTkLabel(
                results_frame,
                text="Database connection failed."
            ).pack(pady=20)

            return

        try:

            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT student_id, name, email
                FROM students
                WHERE student_id LIKE %s
                   OR name LIKE %s
                ORDER BY name
            """

            search_pattern = f"%{search_text}%"

            cursor.execute(
                query,
                (search_pattern, search_pattern)
            )

            students = cursor.fetchall()

            cursor.close()
            connection.close()

            if not students:

                ctk.CTkLabel(
                    results_frame,
                    text="No students found.",
                    font=ctk.CTkFont(size=16)
                ).pack(pady=20)

                return

            for student in students:

                result_card = ctk.CTkFrame(
                    results_frame
                )

                result_card.pack(
                    fill="x",
                    pady=5,
                    padx=5
                )

                ctk.CTkLabel(
                    result_card,
                    text=f"ID: {student['student_id']}",
                    font=ctk.CTkFont(weight="bold")
                ).pack(
                    anchor="w",
                    padx=15,
                    pady=(10, 2)
                )

                ctk.CTkLabel(
                    result_card,
                    text=f"Name: {student['name']}"
                ).pack(
                    anchor="w",
                    padx=15,
                    pady=2
                )

                ctk.CTkLabel(
                    result_card,
                    text=f"Email: {student['email']}"
                ).pack(
                    anchor="w",
                    padx=15,
                    pady=(2, 10)
                )

        except Exception as e:

            print("Search error:", e)

            ctk.CTkLabel(
                results_frame,
                text="Search failed."
            ).pack(pady=20)

    ctk.CTkButton(
        search_window,
        text="🔍 Search",
        width=180,
        height=40,
        command=perform_search
    ).pack(pady=10)

def delete_student():

    delete_window = ctk.CTkToplevel(app)
    delete_window.title("Delete Student")
    delete_window.geometry("450x320")
    delete_window.resizable(False, False)

    ctk.CTkLabel(
        delete_window,
        text="Delete Student",
        font=ctk.CTkFont(
            size=24,
            weight="bold"
        )
    ).pack(pady=(30, 20))

    ctk.CTkLabel(
        delete_window,
        text="Enter Student ID",
        font=ctk.CTkFont(size=14)
    ).pack(anchor="w", padx=40)

    student_id_entry = ctk.CTkEntry(
        delete_window,
        width=370,
        height=40,
        placeholder_text="e.g. TEST002"
    )

    student_id_entry.pack(pady=(5, 15))

    message_label = ctk.CTkLabel(
        delete_window,
        text=""
    )

    message_label.pack(pady=5)

    def confirm_delete():

        student_id = student_id_entry.get().strip()

        if not student_id:

            message_label.configure(
                text="Please enter a Student ID."
            )

            return

        from database import create_connection

        connection = create_connection()

        if connection is None:

            message_label.configure(
                text="Database connection failed."
            )

            return

        try:

            cursor = connection.cursor()

            # Check if student exists
            cursor.execute(
                """
                SELECT id, name
                FROM students
                WHERE student_id = %s
                """,
                (student_id,)
            )

            student = cursor.fetchone()

            if student is None:

                message_label.configure(
                    text="Student not found."
                )

                cursor.close()
                connection.close()

                return

            # Ask for confirmation
            answer = ctk.CTkInputDialog(
                text=f"Delete student: {student[1]}?\nType YES to confirm:",
                title="Confirm Deletion"
            ).get_input()

            if answer is None or answer.upper() != "YES":

                cursor.close()
                connection.close()

                message_label.configure(
                    text="Deletion cancelled."
                )

                return

            # Delete attendance records first
            cursor.execute(
                """
                DELETE FROM attendance
                WHERE student_id = %s
                """,
                (student[0],)
            )

            # Delete student
            cursor.execute(
                """
                DELETE FROM students
                WHERE id = %s
                """,
                (student[0],)
            )

            connection.commit()

            cursor.close()
            connection.close()

            print(
                f"Student {student_id} deleted successfully."
            )

            delete_window.destroy()

            # Refresh Students page
            show_students()

        except Exception as e:

            print("Delete error:", e)

            connection.rollback()
            connection.close()

            message_label.configure(
                text="Could not delete student."
            )

    ctk.CTkButton(
        delete_window,
        text="🗑  Delete Student",
        width=370,
        height=45,
        command=confirm_delete
    ).pack(pady=15)

def show_students():

    # Change header
    header.configure(text="Students")

    welcome.configure(
        text="Manage registered students"
    )

    # Hide dashboard widgets
    stats_frame.pack_forget()
    status_frame.pack_forget()

    # Remove previous page widgets
    for widget in students_page.winfo_children():
        widget.destroy()

    students_page.pack(
        fill="both",
        expand=True,
        pady=20
    )

    # Title
    title = ctk.CTkLabel(
        students_page,
        text="Registered Students",
        font=ctk.CTkFont(
            size=24,
            weight="bold"
        )
    )

    # ========================================
    # STUDENT ACTION BUTTONS
    # ========================================

    actions_frame = ctk.CTkFrame(
    students_page,
    fg_color="transparent"
    )

    actions_frame.pack(
    fill="x",
    pady=(0, 20)
    )


    ctk.CTkButton(
    actions_frame,
    text="➕  Add Student",
    width=160,
    height=40,
    command=add_student
    ).pack(
    side="left"
    )


    ctk.CTkButton(
    actions_frame,
    text="🔍  Search",
    width=160,
    height=40,
    command=search_students
    ).pack(
    side="left",
    padx=10
    )

    ctk.CTkButton(
    actions_frame,
    text="🗑  Delete",
    width=160,
    height=40,
    command=delete_student
    ).pack(
    side="left"
    )


    # Get students from MySQL
    from database import create_connection

    connection = create_connection()

    if connection is None:
        error_label = ctk.CTkLabel(
            students_page,
            text="Database connection failed.",
            font=ctk.CTkFont(size=16)
        )

        error_label.pack(
            pady=30
        )

        return

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            student_id,
            name,
            email
        FROM students
        ORDER BY id ASC
    """)

    students = cursor.fetchall()

    cursor.close()
    connection.close()

    # Header row
    table_header = ctk.CTkFrame(
        students_page
    )

    table_header.pack(
        fill="x",
        pady=(0, 5)
    )

    ctk.CTkLabel(
        table_header,
        text="Student ID",
        width=180,
        anchor="w",
        font=ctk.CTkFont(weight="bold")
    ).pack(
        side="left",
        padx=10
    )

    ctk.CTkLabel(
        table_header,
        text="Name",
        width=180,
        anchor="w",
        font=ctk.CTkFont(weight="bold")
    ).pack(
        side="left",
        padx=10
    )

    ctk.CTkLabel(
        table_header,
        text="Email",
        width=250,
        anchor="w",
        font=ctk.CTkFont(weight="bold")
    ).pack(
        side="left",
        padx=10
    )

    # Student rows
    for student in students:

        row = ctk.CTkFrame(
            students_page
        )

        row.pack(
            fill="x",
            pady=3
        )

        ctk.CTkLabel(
            row,
            text=student["student_id"],
            width=180,
            anchor="w"
        ).pack(
            side="left",
            padx=10
        )

        ctk.CTkLabel(
            row,
            text=student["name"],
            width=180,
            anchor="w"
        ).pack(
            side="left",
            padx=10
        )

        ctk.CTkLabel(
            row,
            text=student["email"],
            width=250,
            anchor="w"
        ).pack(
            side="left",
            padx=10
        )


def show_attendance():

    header.configure(text="Attendance")

    welcome.configure(
        text="View and manage attendance records"
    )

    # Hide dashboard widgets
    stats_frame.pack_forget()
    status_frame.pack_forget()

    # Clear previous attendance page
    for widget in attendance_page.winfo_children():
        widget.destroy()

    attendance_page.pack(
        fill="both",
        expand=True,
        pady=20
    )

    # ========================================
    # TITLE
    # ========================================

    title = ctk.CTkLabel(
        attendance_page,
        text="Attendance Records",
        font=ctk.CTkFont(
            size=24,
            weight="bold"
        )
    )

    title.pack(
        anchor="w",
        pady=(0, 15)
    )

    # ========================================
    # FILTER BUTTONS
    # ========================================

    filter_frame = ctk.CTkFrame(
        attendance_page,
        fg_color="transparent"
    )

    filter_frame.pack(
        fill="x",
        pady=(0, 15)
    )

    # ========================================
    # TABLE
    # ========================================

    table_frame = ctk.CTkScrollableFrame(
        attendance_page,
        height=500
    )

    table_frame.pack(
        fill="both",
        expand=True
    )

    def load_attendance(query_type="all"):

        # Clear table
        for widget in table_frame.winfo_children():
            widget.destroy()

        from database import create_connection

        connection = create_connection()

        if connection is None:

            ctk.CTkLabel(
                table_frame,
                text="Database connection failed."
            ).pack(pady=30)

            return

        try:

            cursor = connection.cursor(dictionary=True)

            if query_type == "today":

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
                    WHERE a.attendance_date = CURDATE()
                    ORDER BY a.attendance_time DESC
                """

                cursor.execute(query)

            else:

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
                    ORDER BY
                        a.attendance_date DESC,
                        a.attendance_time DESC
                """

                cursor.execute(query)

            records = cursor.fetchall()

            cursor.close()
            connection.close()

            # ========================================
            # TABLE HEADER
            # ========================================

            header_row = ctk.CTkFrame(
                table_frame
            )

            header_row.pack(
                fill="x",
                pady=(0, 5)
            )

            columns = [
                ("ID", 60),
                ("Student ID", 130),
                ("Name", 130),
                ("Date", 110),
                ("Time", 100),
                ("Hour", 60),
                ("Status", 100),
                ("Confidence", 100)
            ]

            for column_name, width in columns:

                ctk.CTkLabel(
                    header_row,
                    text=column_name,
                    width=width,
                    anchor="w",
                    font=ctk.CTkFont(
                        weight="bold"
                    )
                ).pack(
                    side="left",
                    padx=5
                )

            # ========================================
            # RECORDS
            # ========================================

            if not records:

                ctk.CTkLabel(
                    table_frame,
                    text="No attendance records found.",
                    font=ctk.CTkFont(size=16)
                ).pack(
                    pady=30
                )

                return

            for record in records:

                row = ctk.CTkFrame(
                    table_frame
                )

                row.pack(
                    fill="x",
                    pady=2
                )

                confidence = record["confidence"]

                if confidence is None:
                    confidence_text = "N/A"
                else:
                    confidence_text = f"{confidence:.2f}"

                values = [
                    str(record["id"]),
                    record["student_id"],
                    record["name"],
                    str(record["attendance_date"]),
                    str(record["attendance_time"]),
                    str(record["attendance_hour"]),
                    record["status"],
                    confidence_text
                ]

                for value, (_, width) in zip(
                    values,
                    columns
                ):

                    ctk.CTkLabel(
                        row,
                        text=value,
                        width=width,
                        anchor="w"
                    ).pack(
                        side="left",
                        padx=5
                    )

        except Exception as e:

            print("Attendance loading error:", e)

            ctk.CTkLabel(
                table_frame,
                text="Could not load attendance records."
            ).pack(
                pady=30
            )

    # ========================================
    # BUTTONS
    # ========================================

    ctk.CTkButton(
        filter_frame,
        text="📋 All Records",
        width=150,
        height=40,
        command=lambda: load_attendance("all")
    ).pack(
        side="left"
    )

    ctk.CTkButton(
        filter_frame,
        text="📅 Today",
        width=150,
        height=40,
        command=lambda: load_attendance("today")
    ).pack(
        side="left",
        padx=10
    )

    # Load all records initially
    load_attendance("all")


def show_reports():

    header.configure(text="Reports")

    welcome.configure(
        text="Attendance reports and analytics"
    )

    # Hide other pages
    stats_frame.pack_forget()
    status_frame.pack_forget()
    students_page.pack_forget()
    attendance_page.pack_forget()

    # Clear reports page
    for widget in reports_page.winfo_children():
        widget.destroy()

    reports_page.pack(
        fill="both",
        expand=True,
        pady=20
    )

    # ========================================
    # TITLE
    # ========================================

    title = ctk.CTkLabel(
        reports_page,
        text="Attendance Reports",
        font=ctk.CTkFont(
            size=24,
            weight="bold"
        )
    )

    title.pack(
        anchor="w",
        pady=(0, 20)
    )

    # ========================================
    # DATABASE
    # ========================================

    from database import create_connection

    connection = create_connection()

    if connection is None:

        ctk.CTkLabel(
            reports_page,
            text="Database connection failed."
        ).pack(pady=30)

        return

    try:

        cursor = connection.cursor(dictionary=True)

        # Total students
        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM students
            """
        )

        total_students = cursor.fetchone()["total"]

        # Total attendance records
        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM attendance
            """
        )

        total_attendance = cursor.fetchone()["total"]

        # Present today
        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM attendance
            WHERE attendance_date = CURDATE()
            """
        )

        present_today = cursor.fetchone()["total"]

        # Overall attendance percentage
        if total_students > 0:

            attendance_percentage = (
                total_attendance /
                (total_students * 24)
            ) * 100

        else:

            attendance_percentage = 0

        # ========================================
        # SUMMARY CARDS
        # ========================================

        cards_frame = ctk.CTkFrame(
            reports_page,
            fg_color="transparent"
        )

        cards_frame.pack(
            fill="x",
            pady=10
        )

        # Total students
        card1 = ctk.CTkFrame(
            cards_frame,
            height=120
        )

        card1.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        card1.pack_propagate(False)

        ctk.CTkLabel(
            card1,
            text="👥 Total Students",
            font=ctk.CTkFont(size=15)
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            card1,
            text=str(total_students),
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20
        )

        # Attendance records
        card2 = ctk.CTkFrame(
            cards_frame,
            height=120
        )

        card2.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )

        card2.pack_propagate(False)

        ctk.CTkLabel(
            card2,
            text="📋 Attendance Records",
            font=ctk.CTkFont(size=15)
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            card2,
            text=str(total_attendance),
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20
        )

        # Present today
        card3 = ctk.CTkFrame(
            cards_frame,
            height=120
        )

        card3.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )

        card3.pack_propagate(False)

        ctk.CTkLabel(
            card3,
            text="📅 Present Today",
            font=ctk.CTkFont(size=15)
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            card3,
            text=str(present_today),
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20
        )

        # Percentage
        card4 = ctk.CTkFrame(
            cards_frame,
            height=120
        )

        card4.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        card4.pack_propagate(False)

        ctk.CTkLabel(
            card4,
            text="📊 Attendance Rate",
            font=ctk.CTkFont(size=15)
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            card4,
            text=f"{attendance_percentage:.1f}%",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20
        )

        # ========================================
        # STUDENT SUMMARY
        # ========================================

        ctk.CTkLabel(
            reports_page,
            text="Student Attendance Summary",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            anchor="w",
            pady=(30, 10)
        )

        summary_frame = ctk.CTkScrollableFrame(
            reports_page,
            height=300
        )

        summary_frame.pack(
            fill="both",
            expand=True
        )

        cursor.execute(
            """
            SELECT
                s.student_id,
                s.name,
                COUNT(a.id) AS attendance_count
            FROM students s
            LEFT JOIN attendance a
                ON s.id = a.student_id
            GROUP BY s.id, s.student_id, s.name
            ORDER BY attendance_count DESC
            """
        )

        student_summary = cursor.fetchall()

        # Header
        header_row = ctk.CTkFrame(
            summary_frame
        )

        header_row.pack(
            fill="x",
            pady=(0, 5)
        )

        columns = [
            ("Student ID", 180),
            ("Name", 180),
            ("Attendance Records", 180)
        ]

        for column_name, width in columns:

            ctk.CTkLabel(
                header_row,
                text=column_name,
                width=width,
                anchor="w",
                font=ctk.CTkFont(
                    weight="bold"
                )
            ).pack(
                side="left",
                padx=10
            )

        # Rows
        for student in student_summary:

            row = ctk.CTkFrame(
                summary_frame
            )

            row.pack(
                fill="x",
                pady=2
            )

            values = [
                student["student_id"],
                student["name"],
                str(student["attendance_count"])
            ]

            for value, (_, width) in zip(
                values,
                columns
            ):

                ctk.CTkLabel(
                    row,
                    text=value,
                    width=width,
                    anchor="w"
                ).pack(
                    side="left",
                    padx=10
                )

        cursor.close()
        connection.close()

    except Exception as e:

        print("Reports loading error:", e)

        if connection.is_connected():
            connection.close()

        ctk.CTkLabel(
            reports_page,
            text="Could not load reports."
        ).pack(
            pady=30
        )

face_recognition_process = None


def start_face_recognition():

    global face_recognition_process

    import subprocess
    import sys
    import os

    # Check if already running
    if (
        face_recognition_process is not None
        and face_recognition_process.poll() is None
    ):
        print("Face Recognition is already running.")

        return

    project_folder = os.path.dirname(
        os.path.abspath(__file__)
    )

    main_file = os.path.join(
        project_folder,
        "main.py"
    )

    if not os.path.exists(main_file):

        print("main.py not found!")

        return

    face_recognition_process = subprocess.Popen(
        [
            sys.executable,
            main_file
        ],
        cwd=project_folder
    )

    print("Face Recognition started.")

def stop_face_recognition():

    global face_recognition_process

    if (
        face_recognition_process is not None
        and face_recognition_process.poll() is None
    ):

        face_recognition_process.terminate()

        print("Face Recognition stopped.")

        face_recognition_process = None

    else:

        print("Face Recognition is not running.")


def show_recognition():
    header.configure(text="Face Recognition")
    welcome.configure(
        text="Start the AI face recognition system"
    )

    clear_content()

    recognition_page = ctk.CTkLabel(
        main_frame,
        text="Face Recognition",
        font=ctk.CTkFont(size=24, weight="bold")
    )

    recognition_page.pack(
        anchor="w",
        pady=30
    )

def show_face_recognition():

    header.configure(
        text="Face Recognition"
    )

    welcome.configure(
        text="Start the camera to recognize registered students"
    )

    # Hide other pages
    stats_frame.pack_forget()
    status_frame.pack_forget()
    students_page.pack_forget()
    attendance_page.pack_forget()
    reports_page.pack_forget()

    # Clear page
    for widget in face_page.winfo_children():
        widget.destroy()

    face_page.pack(
        fill="both",
        expand=True,
        pady=20
    )

    # ========================================
    # TITLE
    # ========================================

    ctk.CTkLabel(
        face_page,
        text="Face Recognition",
        font=ctk.CTkFont(
            size=28,
            weight="bold"
        )
    ).pack(
        pady=(30, 10)
    )

    # ========================================
    # DESCRIPTION
    # ========================================

    ctk.CTkLabel(
        face_page,
        text=(
            "Recognize registered students and "
            "automatically record attendance."
        ),
        font=ctk.CTkFont(size=15)
    ).pack(
        pady=(0, 20)
    )

    # ========================================
    # START BUTTON
    # ========================================

    ctk.CTkButton(
        face_page,
        text="📷  Start Face Recognition",
        width=300,
        height=50,
        font=ctk.CTkFont(
            size=16,
            weight="bold"
        ),
        command=start_face_recognition
    ).pack(
        pady=8
    )

    # ========================================
    # STOP BUTTON
    # ========================================

    ctk.CTkButton(
        face_page,
        text="⏹  Stop Face Recognition",
        width=300,
        height=50,
        font=ctk.CTkFont(
            size=16,
            weight="bold"
        ),
        command=stop_face_recognition
    ).pack(
        pady=8
    )

    # ========================================
    # HOW IT WORKS
    # ========================================

    info_frame = ctk.CTkScrollableFrame(
    face_page,
    height=300
    )

    info_frame.pack(
    fill="both",
    expand=True,
    padx=80,
    pady=(25, 10)
    )

    ctk.CTkLabel(
    info_frame,
    text="How It Works",
    font=ctk.CTkFont(
        size=20,
        weight="bold"
    )
    ).pack(
    pady=(15, 15)
    )

    instructions = [
    "1. Click Start Face Recognition",
    "2. The webcam opens automatically",
    "3. The system detects and recognizes faces",
    "4. Student information is retrieved from MySQL",
    "5. Attendance is automatically recorded",
    "6. A student can be marked once per hour",
    "7. Click Stop Face Recognition when finished"
    ]

    for instruction in instructions:

      ctk.CTkLabel(
        info_frame,
        text=instruction,
        font=ctk.CTkFont(size=14),
        anchor="w"
        ).pack(
        anchor="w",
        padx=30,
        pady=5
        )
    ctk.CTkLabel(
       info_frame,
       text="✓ Attendance is securely stored in MySQL",
       font=ctk.CTkFont(
       size=14,
       weight="bold"
      )
      ).pack(
      anchor="w",
      padx=30,
      pady=(15, 20)
     )


def refresh_dashboard():

    print("Refreshing dashboard...")

    show_dashboard()

    print("Dashboard refreshed.")

def exit_application():

    global face_recognition_process

    # Stop face recognition if running
    if (
        face_recognition_process is not None
        and face_recognition_process.poll() is None
    ):
        face_recognition_process.terminate()

        print("Face Recognition stopped.")

    print("Closing FaceMark AI...")

    app.destroy()


# ========================================
# SIDEBAR BUTTONS
# ========================================

dashboard_button = ctk.CTkButton(
    sidebar,
    text="🏠  Dashboard",
    height=45,
    command=show_dashboard
)
dashboard_button.pack(
    padx=20,
    pady=8,
    fill="x"
)


students_button = ctk.CTkButton(
    sidebar,
    text="👥  Students",
    height=45,
    command=show_students
)
students_button.pack(
    padx=20,
    pady=8,
    fill="x"
)


attendance_button = ctk.CTkButton(
    sidebar,
    text="📋  Attendance",
    height=45,
    command=show_attendance
)

attendance_button.pack(
    padx=20,
    pady=8,
    fill="x"
)


reports_button = ctk.CTkButton(
    sidebar,
    text="📊  Reports",
    height=45,
    command=show_reports
)

reports_button.pack(
    padx=20,
    pady=8,
    fill="x"
)


recognition_button = ctk.CTkButton(
    sidebar,
    text="📷  Face Recognition",
    height=45,
    command=show_face_recognition
)

recognition_button.pack(
    padx=20,
    pady=8,
    fill="x"
)
ctk.CTkButton(
    sidebar,
    text="🔄  Refresh",
    height=45,
    command=refresh_dashboard
).pack(
    fill="x",
    padx=15,
    pady=5
)
ctk.CTkButton(
    sidebar,
    text="❌  Exit",
    height=45,
    command=exit_application
).pack(
    fill="x",
    padx=15,
    pady=5
)



# ========================================
# MAIN CONTENT AREA
# ========================================

main_frame = ctk.CTkFrame(
    app,
    corner_radius=0,
    fg_color="transparent"
)

main_frame.pack(
    side="right",
    fill="both",
    expand=True,
    padx=25,
    pady=25
)


# ========================================
# STUDENTS PAGE
# ========================================

students_page = ctk.CTkFrame(
    main_frame,
    fg_color="transparent"
)

# ========================================
# ATTENDANCE PAGE
# ========================================

attendance_page = ctk.CTkFrame(
    main_frame,
    fg_color="transparent"
)

# ========================================
# REPORTS PAGE
# ========================================

reports_page = ctk.CTkFrame(
    main_frame,
    fg_color="transparent"
)

# ========================================
# FACE RECOGNITION PAGE
# ========================================

face_page = ctk.CTkFrame(
    main_frame,
    fg_color="transparent"
)

# ========================================
# FACE RECOGNITION PAGE
# ========================================

face_page = ctk.CTkFrame(
    main_frame,
    fg_color="transparent"
)

# ========================================
# HEADER
# ========================================

header = ctk.CTkLabel(
    main_frame,
    text="Dashboard",
    font=ctk.CTkFont(
        size=32,
        weight="bold"
    )
)

header.pack(
    anchor="w",
    pady=(5, 3)
)

welcome = ctk.CTkLabel(
    main_frame,
    text="Welcome back! Here's what's happening with FaceMark AI today.",
    font=ctk.CTkFont(
        size=14
    )
)

welcome.pack(
    anchor="w",
    pady=(0, 20)
)


# ========================================
# CLEAR CONTENT
# ========================================

def clear_content():

    stats_frame.pack_forget()
    status_frame.pack_forget()

    for widget in main_frame.winfo_children():

        if widget not in [
            header,
            welcome,
            footer
        ]:
            widget.pack_forget()



# ========================================
# DASHBOARD STATISTICS
# ========================================

stats_frame = ctk.CTkFrame(
    main_frame,
    fg_color="transparent"
)

stats_frame.pack(
    fill="x",
    pady=(10, 20)
)

# ========================================
# TOTAL STUDENTS CARD
# ========================================

students_card = ctk.CTkFrame(
    stats_frame,
    height=150,
    corner_radius=15
)

students_card.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 10)
)

students_card.pack_propagate(False)

ctk.CTkLabel(
    students_card,
    text="👥  Total Students",
    font=ctk.CTkFont(
        size=16,
        weight="bold"
    )
).pack(
    anchor="w",
    padx=22,
    pady=(20, 5)
)

students_value = ctk.CTkLabel(
    students_card,
    text="--",
    font=ctk.CTkFont(
        size=36,
        weight="bold"
    )
)

students_value.pack(
    anchor="w",
    padx=22
)

ctk.CTkLabel(
    students_card,
    text="Registered students",
    font=ctk.CTkFont(size=12)
).pack(
    anchor="w",
    padx=22,
    pady=(0, 10)
)


# ========================================
# PRESENT STUDENTS CARD
# ========================================

present_card = ctk.CTkFrame(
    stats_frame,
    height=150,
    corner_radius=15
)

present_card.pack(
    side="left",
    fill="both",
    expand=True,
    padx=10
)

present_card.pack_propagate(False)

ctk.CTkLabel(
    present_card,
    text="✅  Present Today",
    font=ctk.CTkFont(
        size=16,
        weight="bold"
    )
).pack(
    anchor="w",
    padx=22,
    pady=(20, 5)
)

present_value = ctk.CTkLabel(
    present_card,
    text="--",
    font=ctk.CTkFont(
        size=36,
        weight="bold"
    )
)

present_value.pack(
    anchor="w",
    padx=22
)

ctk.CTkLabel(
    present_card,
    text="Students present today",
    font=ctk.CTkFont(size=12)
).pack(
    anchor="w",
    padx=22,
    pady=(0, 10)
)


# ========================================
# ATTENDANCE PERCENTAGE CARD
# ========================================

percentage_card = ctk.CTkFrame(
    stats_frame,
    height=150,
    corner_radius=15
)

percentage_card.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(10, 0)
)

percentage_card.pack_propagate(False)

ctk.CTkLabel(
    percentage_card,
    text="📊  Attendance Rate",
    font=ctk.CTkFont(
        size=16,
        weight="bold"
    )
).pack(
    anchor="w",
    padx=22,
    pady=(20, 5)
)

percentage_value = ctk.CTkLabel(
    percentage_card,
    text="--%",
    font=ctk.CTkFont(
        size=36,
        weight="bold"
    )
)

percentage_value.pack(
    anchor="w",
    padx=22
)

ctk.CTkLabel(
    percentage_card,
    text="Today's attendance",
    font=ctk.CTkFont(size=12)
).pack(
    anchor="w",
    padx=22,
    pady=(0, 10)
)


# ========================================
# SYSTEM STATUS
# ========================================

status_frame = ctk.CTkFrame(
    main_frame,
    height=170,
    corner_radius=15
)

status_frame.pack(
    fill="x",
    pady=(10, 20)
)

status_frame.pack_propagate(False)

# Title
ctk.CTkLabel(
    status_frame,
    text="System Status",
    font=ctk.CTkFont(
        size=20,
        weight="bold"
    )
).pack(
    anchor="w",
    padx=25,
    pady=(20, 10)
)

# Face Recognition Status
face_status_frame = ctk.CTkFrame(
    status_frame,
    fg_color="transparent"
)

face_status_frame.pack(
    fill="x",
    padx=25,
    pady=3
)

ctk.CTkLabel(
    face_status_frame,
    text="●",
    font=ctk.CTkFont(size=16)
).pack(
    side="left",
    padx=(0, 10)
)

ctk.CTkLabel(
    face_status_frame,
    text="Face Recognition System",
    font=ctk.CTkFont(size=14)
).pack(
    side="left"
)

ctk.CTkLabel(
    face_status_frame,
    text="READY",
    font=ctk.CTkFont(
        size=13,
        weight="bold"
    )
).pack(
    side="right"
)

# MySQL Status
database_status_frame = ctk.CTkFrame(
    status_frame,
    fg_color="transparent"
)

database_status_frame.pack(
    fill="x",
    padx=25,
    pady=3
)

ctk.CTkLabel(
    database_status_frame,
    text="●",
    font=ctk.CTkFont(size=16)
).pack(
    side="left",
    padx=(0, 10)
)

ctk.CTkLabel(
    database_status_frame,
    text="MySQL Database",
    font=ctk.CTkFont(size=14)
).pack(
    side="left"
)

ctk.CTkLabel(
    database_status_frame,
    text="CONNECTED",
    font=ctk.CTkFont(
        size=13,
        weight="bold"
    )
).pack(
    side="right"
)


# ========================================
# FOOTER
# ========================================

footer = ctk.CTkLabel(
    main_frame,
    text="FaceMark AI • AI-Powered Face Recognition Attendance System",
    font=ctk.CTkFont(size=12)
)

footer.pack(
    side="bottom",
    pady=10
)


# ========================================
# UPDATE DASHBOARD
# ========================================

def update_dashboard():

    try:
        total_students = get_total_students()
        present_today = get_present_today()
        percentage = get_attendance_percentage()

        students_value.configure(
            text=str(total_students)
        )

        present_value.configure(
            text=str(present_today)
        )

        percentage_value.configure(
            text=f"{percentage:.1f}%"
        )

        print(
            f"Dashboard updated: "
            f"{total_students} students, "
            f"{present_today} present, "
            f"{percentage:.1f}% attendance"
        )

    except Exception as e:

        print("Dashboard update error:", e)

update_dashboard()

# ========================================
# START APPLICATION
# ========================================

app.mainloop()