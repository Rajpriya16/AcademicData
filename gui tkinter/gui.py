from tkinter import *
from tkinter import messagebox as tmsg
import requests
from PIL import Image, ImageTk  # Importing Pillow
import os
from io import BytesIO 

root = Tk()
root.geometry("1800x800")
root.title("Academic Unit")
root.configure(bg="pink")  # Set root window background to pink

# File paths
teacher_file = 'teachers.txt'
ug_student_file = 'ug_students.txt'
pg_student_file = 'pg_students.txt'

# Initialize lists
lt = []   # list of teachers
lu = []   # list of ug students
lp = []   # list of pg students

# Read data from files
def read_data():
    global lt, lu, lp

    if os.path.exists(teacher_file):
        with open(teacher_file, 'r') as file:
            lt = [line.strip().split(',') for line in file.readlines()]

    if os.path.exists(ug_student_file):
        with open(ug_student_file, 'r') as file:
            lu = [line.strip().split(',') for line in file.readlines()]

    if os.path.exists(pg_student_file):
        with open(pg_student_file, 'r') as file:
            lp = [line.strip().split(',') for line in file.readlines()]

# Write data to files
def write_data():
    with open(teacher_file, 'w') as file:
        for data in lt:
            file.write(','.join(data) + '\n')

    with open(ug_student_file, 'w') as file:
        for data in lu:
            file.write(','.join(data) + '\n')

    with open(pg_student_file, 'w') as file:
        for data in lp:
            file.write(','.join(data) + '\n')

class Person:
    count = 0
    def __init__(self, type_of_person):
        self.type = type_of_person
        Person.count += 1

class Teacher:
    count = 0
    def __init__(self, name, id, password, phone_number):
        self.name = name
        self.id = id
        self.password = password
        self.phone_number = phone_number
        lt.append([name, id, password, phone_number])
        Teacher.count += 1
        write_data()

class Student:
    count = 0
    def __init__(self, type_of_student):
        self.type = type_of_student
        Student.count += 1

class UgStudent:
    count = 0
    def __init__(self, name, id, password, phone_number):
        self.name = name
        self.id = id
        self.password = password
        self.phone_number = phone_number
        lu.append([name, id, password, phone_number])
        UgStudent.count += 1
        write_data()

class PgStudent:
    count = 0
    def __init__(self, name, id, password, phone_number):
        self.name = name
        self.id = id
        self.password = password
        self.phone_number = phone_number
        lp.append([name, id, password, phone_number])
        PgStudent.count += 1
        write_data()

def registration():
    Label(frame, text="Enter 1 for teacher, 2 for ug student and 3 for pg student ", bg="pink", fg="black").grid(row=2, column=0)
    Label(frame, text="enter choice", bg="pink", fg="black").grid(row=3, column=0)

    type_var = IntVar()
    type_entry = Entry(frame, textvariable=type_var)
    type_entry.grid(row=3, column=1)

    Label(frame, text="Enter name ", bg="pink", fg="black").grid(row=4, column=0)
    name_var = StringVar()
    name_entry = Entry(frame, textvariable=name_var)
    name_entry.grid(row=4, column=1)

    Label(frame, text="Enter user id ", bg="pink", fg="black").grid(row=5, column=0)
    id_var = StringVar()
    id_entry = Entry(frame, textvariable=id_var)
    id_entry.grid(row=5, column=1)

    Label(frame, text="Enter password ", bg="pink", fg="black").grid(row=6, column=0)
    password_var = StringVar()
    password_entry = Entry(frame, textvariable=password_var, show="*")
    password_entry.grid(row=6, column=1)

    phone_var = StringVar()
    Label(frame, text="Enter phone number", bg="pink", fg="black").grid(row=7, column=0)
    phone_entry = Entry(frame, textvariable=phone_var)
    phone_entry.grid(row=7, column=1)

    def submit():
        valid = 1
        find = 0

        # Check if the password is valid
        if len(password_var.get()) < 8 or len(password_var.get()) > 12:
            valid = 0

        if not any(char in ['!', '@', '#', '$', '%', '&', '*'] for char in password_var.get()):
            valid = 0

        if not any(char.isdigit() for char in password_var.get()):
            valid = 0

        if not any(char.isupper() for char in password_var.get()):
            valid = 0

        if not any(char.islower() for char in password_var.get()):
            valid = 0

        if valid == 0:
            tmsg.showinfo("Error", "Invalid password")
            return

        # Check if the user id is valid
        if not id_var.get().endswith("@gmail.com"):
            tmsg.showinfo("Error", "Invalid id. Does not have '@gmail.com'.")
            return

        if any(char.isupper() for char in id_var.get()):
            tmsg.showinfo("Error", "Invalid id. The id has uppercase letter.")
            return

        # Check if the phone number is exactly 10 digits
        if len(phone_var.get()) != 10 or not phone_var.get().isdigit():
            tmsg.showinfo("Error", "Invalid phone number. Please enter a 10-digit number.")
            return

        if valid == 1 and id_var.get().endswith("@gmail.com") and not any(char.isupper() for char in id_var.get()):
            selected_type = type_var.get()
            if selected_type == 1:
                Person(selected_type)
                Teacher(name_var.get(), id_var.get(), password_var.get(), phone_var.get())
                tmsg.showinfo("Registration", "User registered successfully")

            elif selected_type == 2:
                Person(selected_type)
                Student(selected_type)
                UgStudent(name_var.get(), id_var.get(), password_var.get(), phone_var.get())
                tmsg.showinfo("Registration", "User registered successfully")

            elif selected_type == 3:
                Person(selected_type)
                Student(selected_type)
                PgStudent(name_var.get(), id_var.get(), password_var.get(), phone_var.get())
                tmsg.showinfo("Registration", "User registered successfully")

            else:
                tmsg.showinfo("Error", "Invalid type")

    Button(frame, text="Submit", command=submit, bg="#0078d7", fg="black").grid(row=11, column=0)

def signin():
    global attempt
    attempt = 0
    Label(frame, text="Enter user id ", bg="pink", fg="black").grid(row=4, column=0)
    id_var = StringVar()
    id_entry = Entry(frame, textvariable=id_var)
    id_entry.grid(row=4, column=1)

    Label(frame, text="Enter password ", bg="pink", fg="black").grid(row=5, column=0)
    password_var = StringVar()
    password_entry = Entry(frame, textvariable=password_var, show="*")
    password_entry.grid(row=5, column=1)

    def submit():
        global attempt, lt, lu, lp
        user_id = id_var.get()
        user_password = password_var.get()
        found = 0
        user_details = ""

        # Check if the user exists and the password is correct
        for data in lt:
            if len(data) >= 3 and user_id == data[1] and user_password == data[2]:
                found = 1
                user_details = f"Name: {data[0]}\nUser ID: {data[1]}\nPhone: {data[3]}"
                break

        if not found:
            for data in lu:
                if len(data) >= 3 and user_id == data[1] and user_password == data[2]:
                    found = 1
                    user_details = f"Name: {data[0]}\nUser ID: {data[1]}\nPhone: {data[3]}"
                    break

        if not found:
            for data in lp:
                if len(data) >= 3 and user_id == data[1] and user_password == data[2]:
                    found = 1
                    user_details = f"Name: {data[0]}\nUser ID: {data[1]}\nPhone: {data[3]}"
                    break
        if found == 1:
            tmsg.showinfo("Success", f"Login successful!")
            show_user_page(user_details)
        else:
            attempt += 1
            if attempt == 3:
                tmsg.showinfo("Error", "You have exhausted all attempts to log in.")
            else:
                tmsg.showinfo("Error", "Invalid username or password")

    Button(frame, text="Submit", command=submit, bg="#0078d7", fg="black").grid(row=6, column=0)

def show_user_page(user_details):
    global frame

    for widget in frame.winfo_children():
        widget.destroy()

    user_info_frame = Frame(frame, padx=10, pady=10, bg="pink")
    user_info_frame.grid(row=0, column=0, sticky="nsew")

    Label(user_info_frame, text="User Details", font=("Helvetica", 16), bg="pink", fg="black").grid(row=0, column=0, columnspan=2, pady=10)
    Label(user_info_frame, text=user_details, font=("Helvetica", 12), bg="pink", fg="black").grid(row=1, column=0, columnspan=2, pady=5)

    logout_button = Button(user_info_frame, text="Logout", command=lambda: show_option("Option 2"), bg="#0078d7", fg="black")
    logout_button.grid(row=2, column=0, columnspan=2, pady=10)

def edit():
    Label(frame, text="Enter user id ", bg="pink", fg="black").grid(row=4, column=0)
    id_var1 = StringVar()
    id_entry1 = Entry(frame, textvariable=id_var1)
    id_entry1.grid(row=4, column=1)

    Label(frame, text="Enter password ", bg="pink", fg="black").grid(row=5, column=0)
    password_var1 = StringVar()
    password_entry1 = Entry(frame, textvariable=password_var1,show='*')
    password_entry1.grid(row=5, column=1)

    def submit():
        global lt, lu, lp
        user_id1 = id_var1.get()
        user_password1 = password_var1.get()
        found_t = 0
        found_u = 0
        found_p = 0
        lt_new = []
        lu_new = []
        lp_new = []

        for data in lt:
            if len(data) >= 3 and user_id1 == data[1] and user_password1 == data[2]:
                found_t = 1
            else:
                lt_new.append(data)
        lt = lt_new.copy()

        for data in lu:
            if len(data) >= 3 and user_id1 == data[1] and user_password1 == data[2]:
                found_u = 1
            else:
                lu_new.append(data)
        lu = lu_new.copy()

        for data in lp:
            if len(data) >= 3 and user_id1 == data[1] and user_password1 == data[2]:
                found_p = 1
            else:
                lp_new.append(data)
        lp = lp_new.copy()

        if found_t == 0 and found_u == 0 and found_p == 0:
            tmsg.showerror("Error", "Invalid username or password")
        else:

            def edit_details():
                if found_t == 1:
                    lt.append([name1_var.get(), user_id1, password1_var.get(), phone1_var.get()])
                if found_u == 1:
                    lu.append([name1_var.get(), user_id1, password1_var.get(), phone1_var.get()])
                if found_p == 1:
                    lp.append([name1_var.get(), user_id1, password1_var.get(), phone1_var.get()])
                write_data()
                tmsg.showinfo("edit", "details updated successfully")

            phone1_var = StringVar()
            Label(frame, text="Enter edited phone number", bg="pink", fg="black").grid(row=7, column=0)
            phone1_entry = Entry(frame, textvariable=phone1_var)
            phone1_entry.grid(row=7, column=1)
            name1_var = StringVar()
            Label(frame, text="Enter edited name", bg="pink", fg="black").grid(row=8, column=0)
            name1_entry = Entry(frame, textvariable=name1_var)
            name1_entry.grid(row=8, column=1)
            password1_var = StringVar()
            Label(frame, text="Enter edited password", bg="pink", fg="black").grid(row=9, column=0)
            password1_entry = Entry(frame, textvariable=password1_var, show="*")
            password1_entry.grid(row=9, column=1)
            Button(frame, text="edit_details", command=edit_details, bg="#0078d7", fg="black").grid(row=10, column=0)

    Button(frame, text="Submit", command=submit, bg="#0078d7", fg="black").grid(row=6, column=0)

def dereg():
    global lt, lu, lp

    Label(frame, text="Enter user id ", bg="pink", fg="black").grid(row=4, column=0)
    id_var1 = StringVar()
    id_entry1 = Entry(frame, textvariable=id_var1)
    id_entry1.grid(row=4, column=1)

    Label(frame, text="Enter password ", bg="pink", fg="black").grid(row=5, column=0)
    password_var1 = StringVar()
    password_entry1 = Entry(frame, textvariable=password_var1, show="*")
    password_entry1.grid(row=5, column=1)

    def submit():
        global lt, lu, lp
        user_id1 = id_var1.get()
        user_password1 = password_var1.get()
        found_t = 0
        found_u = 0
        found_p = 0
        lt_new = []
        lu_new = []
        lp_new = []

        for data in lt:
            if len(data)>=3 and user_id1 == data[1] and user_password1 == data[2]:
                found_t = 1
            else:
                lt_new.append(data)
        lt = lt_new.copy()

        for data in lu:
            if len(data)>=3 and user_id1 == data[1] and user_password1 == data[2]:
                found_u = 1
            else:
                lu_new.append(data)
        lu = lu_new.copy()

        for data in lp:
            if len(data)>=3 and user_id1 == data[1] and user_password1 == data[2]:
                found_p = 1
            else:
                lp_new.append(data)
        lp = lp_new.copy()

        if found_t == 0 and found_u == 0 and found_p == 0:
            tmsg.showerror("Error", "Invalid username or password")
        else:
            write_data()
            tmsg.showinfo("Deregister", "User deregistered successfully")

    Button(frame, text="Submit", command=submit, bg="#0078d7", fg="black").grid(row=6, column=0)

def show_option(option):
    for widget in frame.winfo_children():
        widget.destroy()

    if option == "Option 1":
        registration()
        label = Label(frame, text="USER REGISTRATION", bg="pink", fg="black")
        label.grid(row=1, column=1)
    elif option == "Option 2":
        signin()
        label = Label(frame, text="SIGN IN", bg="pink", fg="black")
        label.grid(row=1, column=1)
    elif option == "Option 3":
        edit()
        label = Label(frame, text="EDIT/UPDATE DETAILS", bg="pink", fg="black")
        label.grid(row=1, column=1)
    elif option == "Option 4":
        dereg()
        label = Label(frame, text="DEREGISTRATION REQUEST", bg="pink", fg="black")
        label.grid(row=1, column=1)

mymenu = Menu(root)
frame = Frame(root, padx=10, pady=10, bg="pink")
frame.grid(row=0, column=0, sticky="nsew")

menu = Menu(root)
root.config(menu=menu)

submenu = Menu(menu, tearoff=0, bg="yellow", fg="black")
menu.add_cascade(label="Options", menu=submenu)

submenu.add_command(label="registration", command=lambda: show_option("Option 1"))
submenu.add_command(label="Sign-in", command=lambda: show_option("Option 2"))
submenu.add_command(label="Edit/ Update", command=lambda: show_option("Option 3"))
submenu.add_command(label="Deregistration", command=lambda: show_option("Option 4"))

# Load the background image using Pillow
try:
    response = requests.get("https://raghavfoundation.org.in/wp-content/uploads/2023/05/school-image.jpg")
    response.raise_for_status()  # Check if the request was successful
    img_data = BytesIO(response.content)
    bg_image = Image.open(img_data)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
except Exception as e:
    tmsg.showerror("Error", f"Failed to load background image: {e}")

# Raise the frame above the background image
frame.lift()

# Read existing data from files
read_data()

root.mainloop()
