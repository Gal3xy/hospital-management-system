import tkinter as tk
from tkinter import messagebox, ttk
import os
from datetime import datetime

# ================= FILES =================
USERS_FILE = "users.txt"
PATIENTS_FILE = "patients.txt"
DOCTORS_FILE = "doctors.txt"      # doctor_name,status
APPOINTMENTS_FILE = "appointments.txt"

for f in [USERS_FILE, PATIENTS_FILE, DOCTORS_FILE, APPOINTMENTS_FILE]:
    if not os.path.exists(f):
        open(f, "w").close()

# ================= ROOT =================
root = tk.Tk()
root.title("Clinic Management System")
root.geometry("1000x600")
root.configure(bg="#2e2e2e")
root.resizable(False, False)

# ================= UTIL =================
def clear():
    for w in root.winfo_children():
        w.destroy()

def read_file(file):
    try:
        with open(file, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []

def write_file(file, lines):
    with open(file, "w") as f:
        f.write("\n".join(lines))

def generate_patient_id():
    return str(len(read_file(PATIENTS_FILE)) + 1)

def get_available_doctors():
    return [d.split(",")[0] for d in read_file(DOCTORS_FILE) if d.endswith("available")]

def get_all_doctors():
    doctors = []
    for d in read_file(DOCTORS_FILE):
        parts = d.split(",")
        if parts[0].strip():
            doctors.append(parts[0])
    return doctors

# ================= ALGORITHM =================
def is_doctor_available(doctor, date, time):
    appointments = read_file(APPOINTMENTS_FILE)
    for a in appointments:
        try:
            parts = a.split(",")
            if len(parts) != 4:
                continue
            pid, d, booked_date, booked_time = parts
            if d == doctor and booked_date == date and booked_time == time:
                return False
        except:
            continue
    return True

# ================= REGISTER =================
def register_screen():
    clear()

    tk.Label(root, text="Register", fg="white",
             bg="#2e2e2e", font=("Arial", 24)).pack(pady=30)

    form = tk.Frame(root, bg="#2e2e2e")
    form.pack()

    entries = {}
    for i, label in enumerate(["Username", "Password", "Confirm Password"]):
        tk.Label(form, text=label, fg="white",
                 bg="#2e2e2e", width=18, anchor="e").grid(row=i, column=0, pady=8)
        e = tk.Entry(form, show="*" if "Password" in label else "", width=30)
        e.grid(row=i, column=1)
        entries[label] = e

    def register():
        if entries["Password"].get() != entries["Confirm Password"].get():
            messagebox.showerror("Error", "Passwords do not match")
            return
        users = read_file(USERS_FILE)
        users.append(f"{entries['Username'].get()},{entries['Password'].get()}")
        write_file(USERS_FILE, users)
        messagebox.showinfo("Success", "Account created")
        login_screen()

    tk.Button(root, text="Register", width=15, command=register).pack(pady=10)
    tk.Button(root, text="Back", command=login_screen).pack()

# ================= LOGIN =================
def login_screen():
    clear()

    tk.Label(root, text="Clinic Login", fg="white",
             bg="#2e2e2e", font=("Arial", 24)).pack(pady=40)

    form = tk.Frame(root, bg="#2e2e2e")
    form.pack()

    tk.Label(form, text="Username", fg="white",
             bg="#2e2e2e", width=18, anchor="e").grid(row=0, column=0, pady=10)
    user = tk.Entry(form, width=30)
    user.grid(row=0, column=1)

    tk.Label(form, text="Password", fg="white",
             bg="#2e2e2e", width=18, anchor="e").grid(row=1, column=0, pady=10)
    pw = tk.Entry(form, show="*", width=30)
    pw.grid(row=1, column=1)

    def login():
        for u in read_file(USERS_FILE):
            name, p = u.split(",")
            if name == user.get() and p == pw.get():
                dashboard()
                return
        messagebox.showerror("Error", "Invalid credentials")

    tk.Button(root, text="Login", width=15, command=login).pack(pady=10)
    tk.Button(root, text="Register", width=15, command=register_screen).pack()

# ================= DASHBOARD =================
def dashboard():
    clear()

    sidebar = tk.Frame(root, bg="#1e1e1e", width=220)
    sidebar.pack(side="left", fill="y")

    main = tk.Frame(root, bg="#2e2e2e")
    main.pack(expand=True, fill="both")

    def btn(text, cmd):
        tk.Button(sidebar, text=text, width=25, command=cmd).pack(pady=6)

    btn("Add Patient", add_patient)
    btn("Search Patient", search_patient)
    btn("Available Doctors", doctors_screen)
    btn("Book Appointment", appointments_screen)
    btn("Search by Doctor", doctor_appointments)
    btn("Logout", login_screen)

    tk.Label(main, text="Dashboard", fg="white",
             bg="#2e2e2e", font=("Arial", 28)).pack(pady=40)

    clock = tk.Label(main, fg="white",
                     bg="#2e2e2e", font=("Arial", 18))
    clock.pack()

    def update_clock():
        clock.config(text="Current Time: " +
                     datetime.now().strftime("%I:%M:%S %p"))
        clock.after(1000, update_clock)

    update_clock()

# ================= PATIENT =================
def add_patient():
    clear()

    tk.Label(root, text="Add Patient", fg="white",
             bg="#2e2e2e", font=("Arial", 22)).pack(pady=20)

    form = tk.Frame(root, bg="#2e2e2e")
    form.pack()

    pid = generate_patient_id()
    tk.Label(form, text="Patient ID", fg="white",
             bg="#2e2e2e", width=18, anchor="e").grid(row=0, column=0)
    tk.Label(form, text=pid, fg="white",
             bg="#2e2e2e").grid(row=0, column=1)

    fields = ["Name", "Age", "Phone", "Email", "Address"]
    entries = {}

    for i, f in enumerate(fields, start=1):
        tk.Label(form, text=f, fg="white",
                 bg="#2e2e2e", width=18, anchor="e").grid(row=i, column=0)
        e = tk.Entry(form, width=30)
        e.grid(row=i, column=1)
        entries[f] = e

    def save():
        data = read_file(PATIENTS_FILE)
        data.append(
            f"{pid},{entries['Name'].get()},{entries['Age'].get()},"
            f"{entries['Phone'].get()},{entries['Email'].get()},"
            f"{entries['Address'].get()}"
        )
        write_file(PATIENTS_FILE, data)
        dashboard()

    tk.Button(root, text="Save", command=save).pack(pady=10)
    tk.Button(root, text="Back", command=dashboard).pack()

# ================= SEARCH PATIENT =================
def search_patient():
    clear()

    tk.Label(root, text="Search Patient", fg="white",
             bg="#2e2e2e", font=("Arial", 22)).pack(pady=20)

    q = tk.Entry(root, width=40)
    q.pack()

    res = tk.Text(root, width=90, height=18)
    res.pack()

    def search():
        res.delete("1.0", tk.END)
        for p in read_file(PATIENTS_FILE):
            if q.get() in p:
                res.insert(tk.END, p + "\n")

    tk.Button(root, text="Search", command=search).pack()
    tk.Button(root, text="Back", command=dashboard).pack()

# ================= DOCTORS =================
def doctors_screen():
    clear()

    tk.Label(root, text="Available Doctors", fg="white",
             bg="#2e2e2e", font=("Arial", 22)).pack(pady=20)

    box = tk.Listbox(root, width=50)
    box.pack()

    for d in read_file(DOCTORS_FILE):
        box.insert(tk.END, d)

    entry = tk.Entry(root)
    entry.pack()

    def add():
        docs = read_file(DOCTORS_FILE)
        docs.append(f"{entry.get()},available")
        write_file(DOCTORS_FILE, docs)
        doctors_screen()

    tk.Button(root, text="Add Doctor", command=add).pack()
    tk.Button(root, text="Back", command=dashboard).pack()

# ================= APPOINTMENTS =================
def appointments_screen():
    clear()

    tk.Label(
        root,
        text="Book Appointment",
        fg="white",
        bg="#2e2e2e",
        font=("Arial", 22)
    ).pack(pady=20)

    form = tk.Frame(root, bg="#2e2e2e")
    form.pack(pady=20)

    # ================= FIELDS =================
    tk.Label(form, text="Patient ID", fg="white",
             bg="#2e2e2e", width=18, anchor="e").grid(row=0, column=0, pady=8)
    pid_entry = tk.Entry(form, width=30)
    pid_entry.grid(row=0, column=1, pady=8)

    tk.Label(form, text="Doctor", fg="white",
             bg="#2e2e2e", width=18, anchor="e").grid(row=1, column=0, pady=8)
    doctor_box = ttk.Combobox(
        form,
        values=get_all_doctors(),
        state="readonly",
        width=28
    )
    doctor_box.grid(row=1, column=1, pady=8)

    tk.Label(form, text="Date (DD-MM-YYYY)", fg="white",
             bg="#2e2e2e", width=18, anchor="e").grid(row=2, column=0, pady=8)
    date_entry = tk.Entry(form, width=30)
    date_entry.insert(0, "03-02-2026")
    date_entry.grid(row=2, column=1, pady=8)

    tk.Label(form, text="Time (HH:MM)", fg="white",
             bg="#2e2e2e", width=18, anchor="e").grid(row=3, column=0, pady=8)
    time_entry = tk.Entry(form, width=30)
    time_entry.insert(0, "10:00")
    time_entry.grid(row=3, column=1, pady=8)

    # ================= BOOK LOGIC =================
    def book():
        pid = pid_entry.get().strip()
        doctor = doctor_box.get().strip()
        date = date_entry.get().strip()
        time = time_entry.get().strip()

        if not pid:
            messagebox.showerror("Error", "Patient ID is required")
            return
        
        if not doctor:
            messagebox.showerror("Error", "Please select a doctor")
            return
        
        if not date:
            messagebox.showerror("Error", "Date is required")
            return
        
        if not time:
            messagebox.showerror("Error", "Time is required")
            return

        if not is_doctor_available(doctor, date, time):
            messagebox.showerror(
                "Unavailable",
                f"{doctor} is already booked at {time} on {date}"
            )
            return

        data = read_file(APPOINTMENTS_FILE)
        data.append(f"{pid},{doctor},{date},{time}")
        write_file(APPOINTMENTS_FILE, data)

        messagebox.showinfo("Success", "Appointment booked successfully")
        dashboard()

    tk.Button(root, text="Book Appointment", width=20,
              command=book).pack(pady=10)
    tk.Button(root, text="Back",
              command=dashboard).pack()
# ================= SEARCH BY DOCTOR =================
def doctor_appointments():
    clear()

    tk.Label(root, text="Appointments by Doctor", fg="white",
             bg="#2e2e2e", font=("Arial", 22)).pack(pady=20)

    d = ttk.Combobox(
        root,
        values=[x.split(",")[0] for x in read_file(DOCTORS_FILE)],
        state="readonly"
    )
    d.pack()

    res = tk.Text(root, width=90, height=18)
    res.pack()

    def search():
        res.delete("1.0", tk.END)
        for a in read_file(APPOINTMENTS_FILE):
            if d.get() in a:
                res.insert(tk.END, a + "\n")

    tk.Button(root, text="Search", command=search).pack()
    tk.Button(root, text="Back", command=dashboard).pack()

# ================= START =================
login_screen()
root.mainloop()
