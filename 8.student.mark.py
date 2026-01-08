import math
import pickle
import gzip
import os
import threading
import queue
import time

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

class PersistenceWorker:
    """
    Background worker that writes compressed
    """
    def __init__(self, filename="students.dat"):
        self._filename = filename
        self._jobs = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._last_status = "idle"
        self._lock = threading.Lock()

    def start(self):
        self._thread.start()

    def stop(self, wait=True):
        self._stop_event.set()
        self._jobs.put(None)
        if wait:
            self._thread.join()

    def save_async(self, data: dict):
        """
        Enqueue a save job
        """
        self._jobs.put(data)

    def status(self):
        with self._lock:
            return self._last_status

    def _run(self):
        while not self._stop_event.is_set():
            job = self._jobs.get()
            if job is None:
                break
            try:
                with self._lock:
                    self._last_status = "saving"
                with gzip.open(self._filename, "wb") as f:
                    pickle.dump(job, f, protocol=pickle.HIGHEST_PROTOCOL)
                with self._lock:
                    self._last_status = "saved"
            except Exception as e:
                with self._lock:
                    self._last_status = f"error: {e}"
            finally:
                self._jobs.task_done() 

class StudentMarkSystem:
    def __init__(self, autosave=True):
        self.__students = []
        self.__courses = []
        self.__marks = {}
        self.__autosave = autosave

        self._worker = PersistenceWorker("students.dat")
        self._worker.start()
        self.load_data()

    def _snapshot(self):
        return {
            "students": self.__students,
            "courses": self.__courses,
            "marks": self.__marks
        }

    def save_data_async(self):
        self._worker.save_async(self._snapshot())
        print("Save")

    def load_data(self):
        if os.path.exists("students.dat"):
            try:
                with gzip.open("students.dat", "rb") as f:
                    data = pickle.load(f)
                self.__students = data.get("students", [])
                self.__courses = data.get("courses", [])
                self.__marks = data.get("marks", {})
                print("Data loaded")
            except Exception as e:
                print(f"Failed to load data: {e}")
        else:
            print("No saved data found")

    def shutdown(self):
        """
        Flush pending saves
        """
        self.save_data_async()
        time.sleep(0.1)
        self._worker.stop(wait=True)
        print("Background stopped.")

    # input
    def input_student_count(self):
        return int(input("Enter number of students: "))

    def input_course_count(self):
        return int(input("Enter number of courses: "))

    def input_students(self, n):
        for i in range(n):
            print(f"\nStudent {i+1}")
            sid = input("ID: ")
            name = input("Name: ")
            dob = input("DoB: ")
            self.__students.append(Student(sid, name, dob))
        if self.__autosave:
            self.save_data_async()

    def input_courses(self, n):
        for i in range(n):
            print(f"\nCourse {i+1}")
            cid = input("Course ID: ")
            name = input("Course name: ")
            credit = int(input("Credit: "))
            self.__courses.append(Course(cid, name, credit))
        if self.__autosave:
            self.save_data_async()

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

        if cid not in self.__marks:
            self.__marks[cid] = {}

        for s in self.__students:
            raw = float(input(f"Mark for {s.get_name()}: "))
            mark = math.floor(raw * 10) / 10
            self.__marks[cid][s.get_sid()] = mark
        if self.__autosave:
            self.save_data_async()

    # output
    def show_students(self):
        if not self.__students:
            print("\nNo student")
            return
        print("\nStudents:")
        for s in self.__students:
            print(f"{s.get_sid()} - {s.get_name()} - {s.get_dob()}")

    def show_courses(self):
        if not self.__courses:
            print("\nNo course")
            return
        print("\nCourses:")
        for c in self.__courses:
            print(f"{c.get_cid()} - {c.get_name()} - credit {c.get_credit()}")

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

# menu
def main():
    system = StudentMarkSystem(autosave=True)
    try:
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
            print("9. Save (background)")
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
            elif choice == "9":
                system.save_data_async()
            elif choice == "0":
                print("Saving and exiting...")
                break
            else:
                print("Invalid choice")
    finally:
        system.shutdown()
        print("Goodbye!")

if __name__ == "__main__":
    main()
