# ===============================
# FACE RECOGNITION ATTENDANCE SYSTEM (FIXED)
# ===============================

import cv2
import numpy as np
import face_recognition
from database import mark_attendance_by_name
from datetime import datetime
from config import IMAGE_DIR
import os
# Keep track of attendance already processed
attendance_cache = set()

path = str(IMAGE_DIR)
images = []
classNames = []

for file_name in os.listdir(path):

    if file_name.lower().endswith(('.jpg', '.png', '.jpeg')):

        img_path = os.path.join(path, file_name)

        current_img = cv2.imread(img_path)

        if current_img is None:
            print(f"Could not load image: {file_name}")
            continue

        # Convert to RGB
        rgb_img = cv2.cvtColor(current_img, cv2.COLOR_BGR2RGB)

        encodings = face_recognition.face_encodings(rgb_img)

        if encodings:
            images.append(current_img)

            name = os.path.splitext(file_name)[0]

            classNames.append(name)

        else:
            print(f"No face found in: {file_name}")


print("Loaded known faces:", classNames)


# ========================================
# ENCODE KNOWN FACES
# ========================================

def find_encodings(images_list):

    encode_list = []

    for img in images_list:

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        encodes = face_recognition.face_encodings(img_rgb)

        if encodes:
            encode_list.append(encodes[0])

    return encode_list


print("Encoding known faces...")

encodeListKnown = find_encodings(images)

print(f"Encoding complete! {len(encodeListKnown)} faces encoded.")



# STEP 3: ACCESS CAMERA AND RECOGNIZE FACES 📹
if encodeListKnown: # Only proceed if faces were encoded
    cap = cv2.VideoCapture(0)  # 0 for default camera

    while True:
        success, img = cap.read()
        
        # Check if frame read successfully
        if not success:
            print("Failed to grab frame.")
            break
            
        # Reduce image size for faster processing (1/4th size)
        img_small = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)

        # Find faces and encodings in the current frame
        faces_current_frame = face_recognition.face_locations(img_small)
        encodes_current_frame = face_recognition.face_encodings(img_small, faces_current_frame)

        for encode_face, face_loc in zip(encodes_current_frame, faces_current_frame):# Compare face with known faces
            matches = face_recognition.compare_faces(encodeListKnown, encode_face)
            
            # Calculate distance to find the best match (lower distance is better)
            face_distances = face_recognition.face_distance(encodeListKnown, encode_face)
            match_index = np.argmin(face_distances) # Get index of the smallest distance

            # Only proceed if the best match is actually a match (based on compare_faces or a distance threshold)
            if matches[match_index] and face_distances[match_index] < 0.5:
              # Get original name from image filename
              name = classNames[match_index]

              # Name displayed on camera
              display_name = name.upper()

              # Scale back face location
              y1, x2, y2, x1 = face_loc
              y1 *= 4
              x2 *= 4
              y2 *= 4
              x1 *= 4

    

              # Draw green box around face
              cv2.rectangle(
              img,
              (x1, y1),
              (x2, y2),
              (0, 255, 0),
              2
              ) 

              # Draw green name background
              cv2.rectangle(
              img,
              (x1, y2 - 35),
              (x2, y2),
              (0, 255, 0),
              cv2.FILLED
              )

              # Display name
              cv2.putText(
              img,
              display_name,
              (x1 + 6, y2 - 6),
              cv2.FONT_HERSHEY_SIMPLEX,
              1,
              (255, 255, 255),
              2
              )

              # ========================================
              # ATTENDANCE CACHE
              # ========================================

              now = datetime.now()

              attendance_key = (
              name,
              now.strftime("%Y-%m-%d"),
              now.strftime("%H")
              )

              # Call MySQL only once per student per hour
              if attendance_key not in attendance_cache:

                print(f"Recognized: {name}")

                # Face recognition distance
                confidence = face_distances[match_index]

                print(f"Face distance: {confidence:.4f}")

                mark_attendance_by_name(
                 name,
                  confidence=confidence
                )

                attendance_cache.add(attendance_key)

            else:
                # Face detected but not recognized as a known person
                name = 'UNKNOWN'
                y1, x2, y2, x1 = face_loc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


        cv2.imshow('Webcam Attendance System', img)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
else:
    print("Execution stopped because no faces were successfully encoded.")
