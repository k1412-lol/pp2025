students = []
courses = []
marks = {}

def input_student_count():
    n = int(input("Enter number of students: "))
    return n

def input_student_info(n):
    for i in range(n):
        print(f"\nStudent {i+1}")
        sid = input("Student id: ")
        name = input("Name: ")
        dob = input("DoB: ")
        students.append({"id": sid, "name": name, "dob": dob})

def input_course_count():
    n = int(input("Enter number of courses: "))
    return n

def input_course_info(n):
    for i in range(n):
        print(f"\nCourse {i+1}")
        cid = input("Course id: ")
        name = input("Course name: ")
        courses.append({"id": cid, "name": name})

def input_marks():
    if not students:
        print("\nNo students")
        return
    if not courses:
        print("\nNo courses")
        return
    print("\nAvailable courses:")
    for c in courses:
        print(f"{c['id']} - {c['name']}")

    cid = input("Enter course id to input marks: ")

    course_ids = [c["id"] for c in courses]
    if cid not in course_ids:
        print("\nNo courses")
        return
    if cid not in marks:
        marks[cid] = {}
    print(f"\nEntering marks for course {cid}")
    for s in students:
        sid = s["id"]
        mark = float(input(f"Mark for {s['name']}: "))
        marks[cid][sid] = mark

def list_students():
    if not students:
        print("\nNo students")
        return

    print("\nStudents:")
    for s in students:
        print(f"ID: {s['id']}, Name: {s['name']}, DoB: {s['dob']}")

def list_courses():
    if not courses:
        print("\nNo courses")
        return

    print("\nCourses:")
    for c in courses:
        print(f"ID: {c['id']}, Name: {c['name']}")


def show_marks():
    if not marks:
        print("\nNo marks")
        return

    cid = input("Enter course id to view marks: ")

    if cid not in marks:
        print("\nNo marks")
        return
    print(f"\nMarks for course {cid}:")
    for s in students:
        sid = s["id"]
        mark = marks[cid].get(sid, "\nNo mark")
        print(f"{s['name']}: {mark}")

def main():
    while True:
        print("\nMENU")
        print("1. Input students")
        print("2. Input courses")
        print("3. Input marks")
        print("4. List courses")
        print("5. List students")
        print("6. Show marks")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            n = input_student_count()
            input_student_info(n)
        elif choice == "2":
            n = input_course_count()
            input_course_info(n)
        elif choice == "3":
            input_marks()
        elif choice == "4":
            list_courses()
        elif choice == "5":
            list_students()
        elif choice == "6":
            show_marks()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid")
main()
