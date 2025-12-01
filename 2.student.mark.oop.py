class Student:
    def __init__(self, sid, name, dob):
        self.id = sid
        self.name = name
        self.dob = dob

class Course:
    def __init__(self, cid, name):
        self.id = cid
        self.name = name

class School:
    def __init__(self):
        self.students = []
        self.courses = []
        self.marks = {}

    def input_students(self):
        n = int(input("Enter number of students: "))
        for _ in range(n):
            sid = input("Student id: ")
            name = input("Name: ")
            dob = input("Date of birth: ")
            self.students.append(Student(sid, name, dob))

    def input_courses(self):
        n = int(input("Enter number of courses: "))
        for _ in range(n):
            cid = input("Course id: ")
            name = input("Course name: ")
            self.courses.append(Course(cid, name))

    def input_marks(self):
        if not self.students or not self.courses:
            print("Invalid")
            return

        print("\nAvailable courses:")
        for c in self.courses:
            print(f"{c.id} - {c.name}")

        cid = input("Enter course id: ")

        if cid not in self.marks:
            self.marks[cid] = {}

        print(f"\nEntering marks for course {cid}")
        for s in self.students:
            mark = float(input(f"Mark for {s.name}: "))
            self.marks[cid][s.id] = mark

    def list_students(self):
        print("\nStudents:")
        for s in self.students:
            print(f"ID: {s.id}, Name: {s.name}, DoB: {s.dob}")

    def list_courses(self):
        print("\nCourses:")
        for c in self.courses:
            print(f"ID: {c.id}, Name: {c.name}")

    def show_marks(self):
        cid = input("Enter course id: ")

        if cid not in self.marks:
            print("Invalid")
            return

        print(f"\nMarks for course {cid}:")
        for s in self.students:
            mark = self.marks[cid].get(s.id, "No mark")
            print(f"{s.name}: {mark}")

def main():
    school = School()
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
            school.input_students()
        elif choice == "2":
            school.input_courses()
        elif choice == "3":
            school.input_marks()
        elif choice == "4":
            school.list_courses()
        elif choice == "5":
            school.list_students()
        elif choice == "6":
            school.show_marks()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option")
main()
