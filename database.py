import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()



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

def get_student_by_id(student_id):

    connection = create_connection()

    if connection is None:
        return None

    try:

        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT *
        FROM students
        WHERE student_id = %s
        LIMIT 1
        """

        cursor.execute(query, (student_id,))

        student = cursor.fetchone()

        cursor.close()
        connection.close()

        return student

    except Error as e:

        print("Error fetching student by ID:", e)

        if connection.is_connected():
            connection.close()

        return None

def get_student_by_name(name):
    connection = create_connection()

    if connection is None:
        return None

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT *
        FROM students
        WHERE LOWER(name) = LOWER(%s)
        """

        cursor.execute(query, (name,))

        student = cursor.fetchone()

        cursor.close()
        connection.close()

        return student

    except Error as e:
        print("Error fetching student:", e)

        if connection.is_connected():
            connection.close()

        return None

def mark_attendance_by_name(name, confidence=None):
    """
    Find a student by name and mark their attendance.
    """

    student = get_student_by_name(name)

    if student is None:
        print(f"Student '{name}' not found in database.")
        return False

    print(
        f"Recognized: {student['name']} "
        f"({student['student_id']})"
    )

    return mark_attendance(
        student["id"],
        confidence
    )    

def mark_attendance_by_id(student_id, confidence=None):
    """
    Find a student by student ID and mark their attendance.
    """

    student = get_student_by_id(student_id)

    if student is None:
        print(
            f"Student ID '{student_id}' not found in database."
        )
        return False

    print(
        f"Recognized: {student['name']} "
        f"({student['student_id']})"
    )

    return mark_attendance(
        student["id"],
        confidence
    )

def mark_attendance(student_id, confidence=None):
    connection = create_connection()

    if connection is None:
        return False

    try:
        cursor = connection.cursor()

        query = """
        INSERT INTO attendance
        (
            student_id,
            attendance_date,
            attendance_time,
            attendance_hour,
            status,
            confidence
        )
        VALUES
        (
            %s,
            CURDATE(),
            CURTIME(),
            HOUR(CURTIME()),
            'Present',
            %s
        )
        """

        cursor.execute(query, (student_id, confidence))

        connection.commit()

        print("Attendance marked successfully!")

        cursor.close()
        connection.close()

        return True

    except mysql.connector.IntegrityError:
        print("Already marked for this hour.")

        connection.rollback()
        connection.close()

        return False

    except Error as e:
        print("Attendance error:", e)

        connection.rollback()
        connection.close()

        return False

if __name__ == "__main__":

    print("Testing attendance by name...")

    mark_attendance_by_name(
        "Alok",
        confidence=0.38
    )
