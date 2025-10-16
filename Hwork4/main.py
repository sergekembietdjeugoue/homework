# Data storage of school data base
# Data storage
students = {}  # { "First Last": {"class": "3C"} }
teachers = {}  # { "First Last": {"subject": "Math", "classes": ["3C", "2B"]} }
homeroom_teachers = {}  # { "First Last": {"class": "3C"} }


def main_menu():
    print("\nAvailable commands: create, manage, end")


def create_user():
    while True:
        print("\nCreate menu: student, teacher, homeroom teacher, end")
        choice = input("What do you want to create? ").strip().lower()

        if choice == "student":
            name = input("Enter student's first and last name: ").strip()
            class_name = input("Enter class name (e.g., 3C): ").strip().upper()
            students[name] = {"class": class_name}
            print(f"Student {name} added to class {class_name}.")

        elif choice == "teacher":
            name = input("Enter teacher's first and last name: ").strip()
            subject = input("Enter subject: ").strip()
            class_list = []
            print("Enter class names (leave empty to stop):")
            while True:
                cls = input("Class: ").strip().upper()
                if cls == "":
                    break
                class_list.append(cls)
            teachers[name] = {"subject": subject, "classes": class_list}
            print(f"Teacher {name} added, teaching {subject} in classes {', '.join(class_list)}.")

        elif choice == "homeroom teacher":
            name = input("Enter homeroom teacher's first and last name: ").strip()
            class_name = input("Enter class they lead (e.g., 3C): ").strip().upper()
            homeroom_teachers[name] = {"class": class_name}
            print(f"Homeroom teacher {name} assigned to class {class_name}.")

        elif choice == "end":
            break
        else:
            print("Invalid choice, try again.")


def manage_user():
    while True:
        print("\nManage menu: class, student, teacher, homeroom teacher, end")
        choice = input("What do you want to manage? ").strip().lower()

        if choice == "class":
            class_name = input("Enter class name (e.g., 3C): ").strip().upper()
            print(f"\nClass {class_name}:")
            # Students
            found_students = [name for name, data in students.items() if data["class"] == class_name]
            if found_students:
                print("Students:")
                for s in found_students:
                    print(f" - {s}")
            else:
                print("No students found.")

            # Homeroom teacher
            found_ht = [name for name, data in homeroom_teachers.items() if data["class"] == class_name]
            if found_ht:
                print(f"Homeroom Teacher: {found_ht[0]}")
            else:
                print("No homeroom teacher found.")

        elif choice == "student":
            name = input("Enter student's first and last name: ").strip()
            if name in students:
                cls = students[name]["class"]
                print(f"\nStudent {name} is in class {cls}.")
                # Find teachers teaching this class
                teacher_list = [t for t, data in teachers.items() if cls in data["classes"]]
                if teacher_list:
                    print("Teachers:")
                    for t in teacher_list:
                        print(f" - {t} ({teachers[t]['subject']})")
                else:
                    print("No teachers found for this class.")
            else:
                print("Student not found.")

        elif choice == "teacher":
            name = input("Enter teacher's first and last name: ").strip()
            if name in teachers:
                print(f"\nTeacher {name} teaches {teachers[name]['subject']} in classes:")
                for cls in teachers[name]["classes"]:
                    print(f" - {cls}")
            else:
                print("Teacher not found.")

        elif choice == "homeroom teacher":
            name = input("Enter homeroom teacher's first and last name: ").strip()
            if name in homeroom_teachers:
                cls = homeroom_teachers[name]["class"]
                print(f"\nHomeroom teacher {name} leads class {cls}.")
                # List students of this class
                found_students = [s for s, data in students.items() if data["class"] == cls]
                if found_students:
                    print("Students:")
                    for s in found_students:
                        print(f" - {s}")
                else:
                    print("No students in this class.")
            else:
                print("Homeroom teacher not found.")

        elif choice == "end":
            break
        else:
            print("Invalid choice, try again.")


# Main program loop
def main():
    while True:
        main_menu()
        command = input("Enter command: ").strip().lower()

        if command == "create":
            create_user()
        elif command == "manage":
            manage_user()
        elif command == "end":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid command, try again.")


if __name__ == "__main__":
    main()

