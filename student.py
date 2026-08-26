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

def capture_student_photo(student_id):

    path = str(IMAGE_DIR)

    # Create folder if it doesn't exist
    if not os.path.exists(path):
        os.makedirs(path)

    # Load OpenCV face detector
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"
    )

    if face_cascade.empty():
        print("Error: Could not load face detector.")
        return False

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return False

    print("\nCamera opened.")
    print("Position one face clearly in front of the camera.")
    print("Press SPACE to capture the photo.")
    print("Press Q to cancel.")

    while True:

        success, frame = cap.read()

        if not success:
            print("Failed to capture frame.")
            break

        # Convert frame to grayscale for face detection
        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(80, 80)
        )

        # Draw face rectangles
        for (x, y, w, h) in faces:

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

        # Display face detection status
        if len(faces) == 0:

            status = "No face detected"

        elif len(faces) == 1:

            status = "Face detected - Ready"

        else:

            status = "Multiple faces detected"

        cv2.putText(
            frame,
            status,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            "SPACE = Capture | Q = Cancel",
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        cv2.imshow(
            "Student Registration",
            frame
        )

        key = cv2.waitKey(1) & 0xFF

        # Capture photo
        if key == ord(' '):

            # Require exactly one face
            if len(faces) == 0:

                print("No face detected. Please try again.")
                continue

            if len(faces) > 1:

                print(
                    "Multiple faces detected. "
                    "Only one student should be visible."
                )
                continue

            filename = os.path.join(
                path,
                f"{student_id}.jpg"
            )

            saved = cv2.imwrite(
                filename,
                frame
            )

            if not saved:

                print("Error: Could not save photo.")

                cap.release()
                cv2.destroyAllWindows()

                return False

            print(
                f"Photo saved successfully: {filename}"
            )

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

def student_exists(student_id):

    connection = create_connection()

    if connection is None:
        return False

    try:

        cursor = connection.cursor()

        query = """
        SELECT id
        FROM students
        WHERE student_id = %s
        LIMIT 1
        """

        cursor.execute(query, (student_id,))

        result = cursor.fetchone()

        return result is not None

    except Exception as e:

        print("Error checking student:", e)

        return False

    finally:

        if connection.is_connected():
            cursor.close()
            connection.close()
            
def register_student():
    print("\n===== REGISTER NEW STUDENT =====")

    student_id = input("Student ID: ").strip()
    name = input("Student Name: ").strip()
    email = input("Email: ").strip()
    department = input("Department: ").strip()

    try:
        year = int(input("Year: "))
    except ValueError:
        print("Invalid year. Please enter a number.")
        return

     
    if not student_id or not name:
        print("Student ID and name are required.")
        return
    if student_exists(student_id):
        print(f"Student ID already exists: {student_id}")
        return    

    print("\nBefore continuing, make sure the student is ready.")

    photo_captured = capture_student_photo(student_id)
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
        photo_path = os.path.join(
        str(IMAGE_DIR),
        f"{student_id}.jpg"
        )

        if os.path.exists(photo_path):
            os.remove(photo_path)
            print("Saved face photo removed.")

        print("Student registration failed.")



if __name__ == "__main__":

    register_student()
