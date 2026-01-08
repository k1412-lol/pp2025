import math
from .student import Student
from .course import Course

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

