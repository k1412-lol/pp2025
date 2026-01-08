from domains.system import StudentMarkSystem
from input import menu

def main(): 
    system = StudentMarkSystem() 
    
    while True: 
        menu()
        choice = input("Choose: ")
        if choice == "1": 
            n = system.input_student_count()
            system.input_students() 
        elif choice == "2": 
            n = system.input_course_count()
            system.input_courses() 
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
            system.save_data() 
            print("Goodbye!") 
            break 
        else: 
            print("Invalid choice") 
            
main()
