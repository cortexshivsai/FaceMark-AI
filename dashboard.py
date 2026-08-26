from mysql.connector import Error

from database import create_connection

load_dotenv()


# ========================================
# GET TOTAL STUDENTS
# ========================================

def get_total_students():

    connection = create_connection()

    if connection is None:
        return 0

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM students
        """)

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result[0]

    except Error as e:

        print("Error getting total students:", e)

        connection.close()

        return 0


# ========================================
# GET TODAY'S PRESENT STUDENTS
# ========================================

def get_present_today():

    connection = create_connection()

    if connection is None:
        return 0

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT COUNT(DISTINCT student_id)
            FROM attendance
            WHERE attendance_date = CURDATE()
        """)

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result[0]

    except Error as e:

        print("Error getting today's attendance:", e)

        connection.close()

        return 0


# ========================================
# GET TODAY'S ATTENDANCE PERCENTAGE
# ========================================

def get_attendance_percentage():

    total_students = get_total_students()

    present_today = get_present_today()

    if total_students == 0:
        return 0

    percentage = (
        present_today / total_students
    ) * 100

    return percentage


