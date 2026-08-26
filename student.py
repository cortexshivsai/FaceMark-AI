from database import create_connection
import cv2
from config import IMAGE_DIR
import os

def add_student(student_id, name, email=None, department="AIML", year=3):

    connection = create_connection()

    if connection is None:
        return False

    try:
        cursor = connection.cursor()

        query = """
        INSERT INTO students
        (student_id, name, email, department, year)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            student_id,
            name,
            email,
            department,
            year
        )

        cursor.execute(query, values)

        connection.commit()

        print(f"Student added successfully: {name}")

        return True

    except Exception as e:

        print("Error adding student:", e)

        connection.rollback()

        return False

    finally:

        if connection.is_connected():
            cursor.close()
            connection.close()


def get_all_students():

    connection = create_connection()

    if connection is None:
        return []

    try:

        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            id,
            student_id,
            name,
            email,
            department,
            year
        FROM students
        ORDER BY id
        """

        cursor.execute(query)

        students = cursor.fetchall()

        return students

    except Exception as e:

        print("Error fetching students:", e)

        return []

    finally:

        if connection.is_connected():
            cursor.close()
            connection.close()

def capture_student_photo(name):
    
    path = str(IMAGE_DIR)
    # Create folder if it doesn't exist
    if not os.path.exists(path):
        os.makedirs(path)

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return False

    print("\nCamera opened.")
    print("Position your face in front of the camera.")
    print("Press SPACE to capture the photo.")
    print("Press Q to cancel.")

    while True:

        success, frame = cap.read()

        if not success:
            print("Failed to capture frame.")
            break

        cv2.putText(
            frame,
            "Press SPACE to Capture | Q to Cancel",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.imshow("Student Registration", frame)

        key = cv2.waitKey(1) & 0xFF

        # Capture photo
        if key == ord(' '):

            filename = os.path.join(path, f"{name}.jpg")

            cv2.imwrite(filename, frame)

            print(f"Photo saved successfully: {filename}")

            cap.release()
            cv2.destroyAllWindows()

            return True

        # Cancel
        elif key == ord('q'):

            print("Photo capture cancelled.")

            cap.release()
            cv2.destroyAllWindows()

            return False

    cap.release()
    cv2.destroyAllWindows()

    return False            

def register_student():

    print("\n===== REGISTER NEW STUDENT =====")

    student_id = input("Student ID: ")
    name = input("Student Name: ")
    email = input("Email: ")
    department = input("Department: ")
    year = int(input("Year: "))

    print("\nBefore continuing, make sure the student is ready.")

    photo_captured = capture_student_photo(name)

    if not photo_captured:

        print("Registration cancelled.")

        return

    # Add student to MySQL
    success = add_student(
        student_id,
        name,
        email,
        department,
        year
    )

    if success:

        print("\n================================")
        print("STUDENT REGISTERED SUCCESSFULLY")
        print("================================")
        print(f"Student ID : {student_id}")
        print(f"Name       : {name}")
        print(f"Department : {department}")
        print(f"Year       : {year}")
        print("Face Photo : Saved")
        print("================================")

    else:

        print("Student registration failed.")



if __name__ == "__main__":

    register_student()
