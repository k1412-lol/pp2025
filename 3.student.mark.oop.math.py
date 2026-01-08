import math

class Student:
    def __init__(self, sid, name, dob):
        self.__sid = sid
        self.__name = name
        self.__dob = dob

    def set_sid(self, sid): 
        self.__sid = sid
    def get_sid(self): 
        return self.__sid

    def set_name(self, name): 
        self.__name = name
    def get_name(self): 
        return self.__name

    def set_dob(self, dob): 
        self.__dob = dob
    def get_dob(self): 
        return self.__dob


class Course:
    def __init__(self, cid, name, credit):
        self.__cid = cid
        self.__name = name
        self.__credit = credit

    def set_cid(self, cid): 
        self.__cid = cid
    def get_cid(self): 
        return self.__cid

    def set_name(self, name): 
        self.__name = name
    def get_name(self): 
        return self.__name

    def set_credit(self, credit): 
        self.__credit = credit
    def get_credit(self): 
        return self.__credit


class StudentMarkSystem:
    def __init__(self):
        self.__students = []
        self.__courses = []
        self.__marks = {}

    # input num
    def input_student_count(self):
        return int(input("Enter number of students: "))

    def input_course_count(self):
        return int(input("Enter number of courses: "))

    # input student
    def input_students(self, n):
        for i in range(n):
            print(f"\nStudent {i+1}")
            sid = input("ID: ")
            name = input("Name: ")
            dob = input("DoB: ")
            self.__students.append(Student(sid, name, dob))

    def show_students(self):
        if not self.__students:
            print("\nNo student")
            return
        print("\nStudents:")
        for s in self.__students:
            print(f"{s.get_sid()} - {s.get_name()} - {s.get_dob()}")

    # input course
    def input_courses(self, n):
        for i in range(n):
            print(f"\nCourse {i+1}")
            cid = input("Course ID: ")
            name = input("Course name: ")
            credit = int(input("Credit: "))
            self.__courses.append(Course(cid, name, credit))

    def show_courses(self):
        if not self.__courses:
            print("\nNo course")
            return
        print("\nCourses:")
        for c in self.__courses:
            print(f"{c.get_cid()} - {c.get_name()} - credit {c.get_credit()}")

    # input mark
    def input_marks(self):
        if not self.__students or not self.__courses:
            print("\nNo course or student")
            return

        print("\nCourses:")
        for c in self.__courses:
            print(f"{c.get_cid()} - {c.get_name()}")

        cid = input("Enter course ID: ")
        course_ids = [c.get_cid() for c in self.__courses]
        if cid not in course_ids:
            print("\nNo course")
            return

        self.__marks[cid] = {}

        for s in self.__students:
            raw = float(input(f"Mark for {s.get_name()}: "))
            mark = math.floor(raw * 10) / 10
            self.__marks[cid][s.get_sid()] = mark

    def show_marks(self):
        cid = input("Course ID: ")
        if cid not in self.__marks:
            print("\nNo marks")
            return
        for s in self.__students:
            sid = s.get_sid()
            mark = self.__marks[cid].get(sid, "No mark")
            print(f"{s.get_name()}: {mark}")

    # GPA
    def calculate_gpa(self, student_id):
        total_credit = 0
        total_score = 0

        for c in self.__courses:
            cid = c.get_cid()
            credit = c.get_credit()

            if cid in self.__marks and student_id in self.__marks[cid]:
                total_credit += credit
                total_score += credit * self.__marks[cid][student_id]

        if total_credit == 0:
            return 0
        return total_score / total_credit

    def show_gpa_list(self):
        if not self.__students:
            print("\nNo student")
            return
        print("\nGPA list:")
        for s in self.__students:
            gpa = self.calculate_gpa(s.get_sid())
            print(f"{s.get_name()} | GPA: {gpa:.2f}")

    def sort_by_gpa(self):
        if not self.__students:
            print("\nNo student")
            return
        self.__students.sort(
            key=lambda s: self.calculate_gpa(s.get_sid()),
            reverse=True
        )
        print("\nSorted students by GPA")


# Menu
def main():
    system = StudentMarkSystem()
    while True:
        print("\nMENU")
        print("1. Input students")
        print("2. Input courses")
        print("3. Input marks")
        print("4. Show students")
        print("5. Show courses")
        print("6. Show marks")
        print("7. Show GPA list")
        print("8. Sort by GPA")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            n = system.input_student_count()
            system.input_students(n)
        elif choice == "2":
            n = system.input_course_count()
            system.input_courses(n)
        elif choice == "3":
            system.input_marks()
        elif choice == "4":
            system.show_students()
        elif choice == "5":
            system.show_courses()
        elif choice == "6":
            system.show_marks()
        elif choice == "7":
            system.show_gpa_list()
        elif choice == "8":
            system.sort_by_gpa()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")

main()
