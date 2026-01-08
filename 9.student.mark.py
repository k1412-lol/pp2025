import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import math, pickle, gzip, os, threading, queue

# models
class Student:
    def __init__(self, sid, name, dob):
        self.sid = str(sid)
        self.name = name
        self.dob = dob

class Course:
    def __init__(self, cid, name, credit):
        self.cid = str(cid)
        self.name = name
        self.credit = int(credit)

# Persistence
class PersistenceWorker:
    def __init__(self, filename="students.dat"):
        self.filename = filename
        self.jobs = queue.Queue()
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def save_async(self, data):
        self.jobs.put(data)

    def stop(self):
        self.stop_event.set()
        self.jobs.put(None)
        self.thread.join()

    def run(self):
        while not self.stop_event.is_set():
            job = self.jobs.get()
            if job is None:
                break
            with gzip.open(self.filename, "wb") as f:
                pickle.dump(job, f, protocol=pickle.HIGHEST_PROTOCOL)
            self.jobs.task_done()

# System
class StudentMarkSystem:
    def __init__(self):
        self.students = []
        self.courses = []
        self.marks = {}
        self.worker = PersistenceWorker()
        self.load()

    def snapshot(self):
        return {"students": self.students, "courses": self.courses, "marks": self.marks}

    def save(self):
        self.worker.save_async(self.snapshot())

    def load(self):
        if os.path.exists("students.dat"):
            with gzip.open("students.dat", "rb") as f:
                data = pickle.load(f)
            self.students = data["students"]
            self.courses = data["courses"]
            self.marks = data["marks"]

    def shutdown(self):
        self.save()
        self.worker.stop()

    def add_student(self, sid, name, dob):
        self.students.append(Student(str(sid), name, dob))
        self.save()

    def add_course(self, cid, name, credit):
        self.courses.append(Course(str(cid), name, int(credit)))
        self.save()

    def add_mark(self, cid, sid, mark):
        cid = str(cid)
        sid = str(sid)
        if cid not in self.marks:
            self.marks[cid] = {}
        self.marks[cid][sid] = mark
        self.save()

    def gpa(self, sid):
        sid = str(sid)
        total_credit = 0
        total_score = 0
        for c in self.courses:
            if c.cid in self.marks and sid in self.marks[c.cid]:
                total_credit += c.credit
                total_score += c.credit * self.marks[c.cid][sid]
        return total_score / total_credit if total_credit else 0

    def sort_by_gpa(self):
        self.students.sort(key=lambda s: self.gpa(s.sid), reverse=True)

# GUI
def main():
    sys = StudentMarkSystem()
    root = tk.Tk()
    root.title("PW9 GUI Management System")
    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True)

    # student
    fstu = ttk.Frame(nb)
    nb.add(fstu, text="Students")
    sid = tk.Entry(fstu); name = tk.Entry(fstu); dob = tk.Entry(fstu)
    sid.grid(row=0, column=0); name.grid(row=0, column=1); dob.grid(row=0, column=2)
    treeS = ttk.Treeview(fstu, columns=("ID", "Name", "DoB"), show="headings")
    treeS.grid(row=1, column=0, columnspan=3)
    for c in ("ID", "Name", "DoB"): treeS.heading(c, text=c)

    def refreshS():
        treeS.delete(*treeS.get_children())
        for s in sys.students:
            treeS.insert("", "end", values=(s.sid, s.name, s.dob))

    def addS():
        if sid.get() and name.get() and dob.get():
            sys.add_student(sid.get(), name.get(), dob.get())
            sid.delete(0, tk.END); name.delete(0, tk.END); dob.delete(0, tk.END)
            refreshS(); refreshG(); refreshM()

    tk.Button(fstu, text="Add", command=addS).grid(row=0, column=3)
    refreshS()

    # course
    fco = ttk.Frame(nb)
    nb.add(fco, text="Courses")
    cid = tk.Entry(fco); cname = tk.Entry(fco); credit = tk.Entry(fco)
    cid.grid(row=0, column=0); 
    cname.grid(row=0, column=1); 
    credit.grid(row=0, column=2)
    treeC = ttk.Treeview(fco, columns=("CID", "Name", "Credit"), show="headings")
    treeC.grid(row=1, column=0, columnspan=3)
    for c in ("CID", "Name", "Credit"): treeC.heading(c, text=c)

    # mark
    fma = ttk.Frame(nb)
    nb.add(fma, text="Marks")
    courseVar = tk.StringVar()
    combo = ttk.Combobox(fma, textvariable=courseVar, state="readonly")
    combo.grid(row=0, column=0)
    treeM = ttk.Treeview(fma, columns=("ID", "Name", "Mark"), show="headings")
    treeM.grid(row=1, column=0, columnspan=2)
    for c in ("ID", "Name", "Mark"): treeM.heading(c, text=c)

    # GPA
    fga = ttk.Frame(nb)
    nb.add(fga, text="GPA")
    treeG = ttk.Treeview(fga, columns=("ID", "Name", "GPA"), show="headings")
    treeG.pack()
    for c in ("ID", "Name", "GPA"): treeG.heading(c, text=c)

    def refreshCombo():
        combo["values"] = [c.cid for c in sys.courses]
        if combo["values"] and not courseVar.get():
            courseVar.set(combo["values"][0])

    def refreshM(*_):
        treeM.delete(*treeM.get_children())
        cid_val = str(courseVar.get())
        if not cid_val: return
        marks = sys.marks.get(cid_val, {})
        for s in sys.students:
            sid_val = str(s.sid)
            mark = marks.get(sid_val, "")
            treeM.insert("", "end", values=(sid_val, s.name, mark))

    def refreshG():
        treeG.delete(*treeG.get_children())
        for s in sys.students:
            treeG.insert("", "end", values=(s.sid, s.name, f"{sys.gpa(s.sid):.2f}"))

    def refreshC():
        treeC.delete(*treeC.get_children())
        for c in sys.courses:
            treeC.insert("", "end", values=(c.cid, c.name, c.credit))
        refreshCombo(); refreshM(); refreshG()

    def addC():
        if cid.get() and cname.get() and credit.get().isdigit():
            sys.add_course(cid.get(), cname.get(), int(credit.get()))
            cid.delete(0, tk.END); 
            cname.delete(0, tk.END); 
            credit.delete(0, tk.END)
            refreshC()

    def setM():
        cid_val = str(courseVar.get())
        sel = treeM.selection()
        if cid_val and sel:
            sid_val = str(treeM.item(sel[0])["values"][0])
            name_val = treeM.item(sel[0])["values"][1]
            val = simpledialog.askfloat("Mark", f"Enter mark for {name_val}")
            if val is not None:
                norm = math.floor(val * 10) / 10
                sys.add_mark(cid_val, sid_val, norm)
                refreshM(); refreshG()

    def sortG():
        sys.sort_by_gpa()
        refreshG()

    tk.Button(fco, text="Add", command=addC).grid(row=0, column=3)
    tk.Button(fma, text="Set Mark", command=setM).grid(row=2, column=0)
    tk.Button(fga, text="Refresh", command=refreshG).pack()
    tk.Button(fga, text="Sort", command=sortG).pack()

    refreshS(); 
    refreshC(); 
    refreshCombo(); 
    refreshM(); 
    refreshG()

    root.protocol("WM_DELETE_WINDOW", lambda: (sys.shutdown(), root.destroy()))
    root.mainloop()

if __name__ == "__main__":
    main()
