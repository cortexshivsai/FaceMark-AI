from datetime import datetime

file = r"C:\Users\shivs\OneDrive\Desktop\Shivsai Python\shivsai\Self_Project1\attendance.csv"

with open(file, "a") as f:
    f.write(f"TEST,{datetime.now()}\n")

print("Done")