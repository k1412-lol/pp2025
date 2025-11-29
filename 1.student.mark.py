students = []
courses = []
marks = {}

def input_students():
    n = int(input("Enter number of students: "))
    for i in range(n):
        sid = input("Student id: ")
        name = input("Name: ")
        dob = input("Date of birth: ")
        students.append({"id": sid, "name": name, "dob": dob})


def input_courses():
    n = int(input("Enter number of courses: "))
    for i in range(n):
        cid = input("Course id: ")
        name = input("Course name: ")
        courses.append({"id": cid, "name": name})


def input_marks():
    if not students or not courses:
        print("Invalid")
        return

    print("\nAvailable courses:")
    for c in courses:
        print(f"{c['id']} - {c['name']}")

    cid = input("Enter course id to input marks: ")

    if cid not in marks:
        marks[cid] = {}

    print(f"\nEntering marks for course {cid}")
    for s in students:
        sid = s["id"]
        mark = float(input(f"Mark for {s['name']}: "))
        marks[cid][sid] = mark

def list_students():
    print("\nStudents")
    for s in students:
        print(f"ID: {s['id']}, Name: {s['name']}, DoB: {s['dob']}")


def list_courses():
    print("\nCourses")
    for c in courses:
        print(f"ID: {c['id']}, Name: {c['name']}")


def show_marks():
    cid = input("Enter course id to view marks: ")

    if cid not in marks:
        print("No mark")
        return

    print(f"\nMarks for course {cid}:")
    for s in students:
        sid = s["id"]
        mark = marks[cid].get(sid, "No mark")
        print(f"{s['name']}: {mark}")

def main():
    while True:
        print("1. Input students")
        print("2. Input courses")
        print("3. Input marks")
        print("4. List courses")
        print("5. List students")
        print("6. Show marks")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            input_students()
        elif choice == "2":
            input_courses()
        elif choice == "3":
            input_marks()
        elif choice == "4":
            list_courses()
        elif choice == "5":
            list_students()
        elif choice == "6":
            show_marks()
        elif choice == "0":
            print("Goodbye")
            break
        else:
            print("Try again")
main()