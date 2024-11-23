import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
from tkinter import messagebox
from Admin_class import Admin
from Doctor_class import Doctor
from Patient_class import Patient
import pickle


class AdminLoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Admin Login")
        self.geometry("300x300")
        self.admin = Admin('admin', '123', 'B1 1AB')
        self.create_widgets()

    def create_widgets(self):
        menu_label = tk.Label(self, text="Admin Login")
        menu_label.pack(pady=10)

        username_label = tk.Label(self, text="Username:")
        username_label.pack(pady=5)
        self.username_var = tk.StringVar()
        username_entry = tk.Entry(self, textvariable=self.username_var)
        username_entry.pack(pady=5)

        password_label = tk.Label(self, text="Password:")
        password_label.pack(pady=5)
        self.password_var = tk.StringVar()
        password_entry = tk.Entry(self, textvariable=self.password_var, show="*")
        password_entry.pack(pady=5)

        login_button = tk.Button(self, text="Login", command=self.login_action)
        login_button.pack(pady=10)

    def login_action(self):
        entered_username = self.username_var.get()
        entered_password = self.password_var.get()

        try:
            if self.admin.login(entered_username, entered_password):
                self.destroy()
                app = MedicalApp(self.admin)
                app.mainloop()
            else:
                messagebox.showerror("Error", "Incorrect username or password. Please try again.")

        except Exception as e:
            messagebox.showerror("Error", f"Error during login: {e}")


class AdminUpdateWindow(tk.Toplevel):
    def __init__(self, admin):
        super().__init__()

        self.title("Update Admin Details")
        self.geometry("300x200")

        self.admin = admin

        self.create_widgets()

    def create_widgets(self):
        menu_label = tk.Label(self, text="Update Admin Details")
        menu_label.pack(pady=10)

        labels = ["Update Username", "Update Password", "Update Address"]
        entry_vars = [tk.StringVar() for _ in range(3)]

        for label, var in zip(labels, entry_vars):
            label_entry = tk.Entry(self, textvariable=var)
            label_entry.insert(0, getattr(self.admin, f"get_{label.split(' ')[1].lower()}")())
            label_entry.pack(pady=5)

        update_button = tk.Button(self, text="Update", command=lambda: self.update_action(entry_vars))
        update_button.pack(pady=10)

    def update_action(self, entry_vars):
        try:
            new_username = entry_vars[0].get()
            new_password = entry_vars[1].get()
            new_address = entry_vars[2].get()

            # Update admin details
            if new_username:
                self.admin.set_username(new_username)
            if new_password:
                self.admin.set_password(new_password)
            if new_address:
                self.admin.set_address(new_address)

            messagebox.showinfo("Success", "Admin details updated successfully.")
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Error updating admin details: {e}")


class DoctorManagementWindow(tk.Toplevel):
    def __init__(self, admin, doctors):
        super().__init__()

        self.title("Doctor Management")
        self.geometry("400x300")

        self.admin = admin
        self.doctors = doctors

        self.create_widgets()

    def create_widgets(self):
        menu_label = tk.Label(self, text="Doctor Management")
        menu_label.pack(pady=10)

        buttons = [
            ("Register Doctor", self.register_doctor),
            ("View Doctors", self.view_doctors),
            ("Update Doctor", self.update_doctor),
            ("Delete Doctor", self.delete_doctor),
            ("Total Doctors", self.total_doctors),
            ("Close", self.destroy)
        ]

        for text, command in buttons:
            button = tk.Button(self, text=text, command=command)
            button.pack(pady=5)

    def register_doctor(self):
        register_window = tk.Toplevel(self)
        register_window.title("Register Doctor")
        register_window.geometry("300x300")

        # Create input fields
        first_name_label = tk.Label(register_window, text="First Name:")
        first_name_label.pack(pady=5)
        first_name_entry = tk.Entry(register_window)
        first_name_entry.pack(pady=5)

        surname_label = tk.Label(register_window, text="Surname:")
        surname_label.pack(pady=5)
        surname_entry = tk.Entry(register_window)
        surname_entry.pack(pady=5)

        speciality_label = tk.Label(register_window, text="Speciality:")
        speciality_label.pack(pady=5)
        speciality_entry = tk.Entry(register_window)
        speciality_entry.pack(pady=5)

        # Create button to register the doctor
        register_button = tk.Button(register_window, text="Register", command=lambda: self.register_doctor_action(
            first_name_entry.get(), surname_entry.get(), speciality_entry.get(), register_window))
        register_button.pack(pady=10)

    def register_doctor_action(self, first_name, surname, speciality, register_window):
        new_doctor = Doctor(first_name, surname, speciality)
        self.doctors.append(new_doctor)
        print(f"Doctor {first_name} {surname} registered successfully.")
        register_window.destroy()
        self.focus_force()

    def view_doctors(self):
        view_window = tk.Toplevel(self)
        view_window.title("View Doctors")
        view_window.geometry("400x300")

        doctors_label = tk.Label(view_window, text="List of Doctors:")
        doctors_label.pack(pady=10)

        doctors_listbox = tk.Listbox(view_window, width=50, height=15)
        doctors_listbox.pack(pady=10)

        for doctor in self.doctors:
            doctors_listbox.insert(tk.END, f"{doctor.get_fullname()} | {doctor.get_speciality()}")

    def update_doctor(self):
        update_window = tk.Toplevel(self)
        update_window.title("Update Doctor")
        update_window.geometry("300x300")

        # Create input fields
        id_label = tk.Label(update_window, text="Doctor ID:")
        id_label.pack(pady=5)
        id_entry = tk.Entry(update_window)
        id_entry.pack(pady=5)

        choice_label = tk.Label(update_window, text="Choose Field to Update:")
        choice_label.pack(pady=5)

        choice_var = tk.StringVar(update_window)
        choices = ["First Name", "Surname", "Speciality"]
        choice_var.set(choices[0])
        choice_dropdown = tk.OptionMenu(update_window, choice_var, *choices)
        choice_dropdown.pack(pady=5)

        new_value_label = tk.Label(update_window, text="Enter New Value:")
        new_value_label.pack(pady=5)
        new_value_entry = tk.Entry(update_window)
        new_value_entry.pack(pady=5)

        # Create button to update the doctor
        update_button = tk.Button(update_window, text="Update", command=lambda: self.update_doctor_action(
            id_entry.get(), choice_var.get(), new_value_entry.get(), update_window))
        update_button.pack(pady=10)

    def update_doctor_action(self, doctor_id, field, new_value, update_window):
        try:
            doctor_id = int(doctor_id)
            selected_doctor = self.doctors[doctor_id - 1]

            if field == "First Name":
                selected_doctor.set_first_name(new_value)
            elif field == "Surname":
                selected_doctor.set_surname(new_value)
            elif field == "Speciality":
                selected_doctor.set_speciality(new_value)
            messagebox.showinfo('Success', f"Doctor {selected_doctor.get_fullname()} updated successfully.")
            update_window.destroy()
            self.focus_force()

        except ValueError:
            messagebox.showerror("Error", "Invalid Doctor ID. Please enter a numeric value.")
        except IndexError:
            messagebox.showerror('Error', 'Doctor not found. Please enter a valid Doctor ID.')

    def delete_doctor(self):
        delete_window = tk.Toplevel(self)
        delete_window.title("Delete Doctor")
        delete_window.geometry("300x200")

        # Create input fields
        id_label = tk.Label(delete_window, text="Doctor ID:")
        id_label.pack(pady=5)
        id_entry = tk.Entry(delete_window)
        id_entry.pack(pady=5)

        # Create button to delete the doctor
        delete_button = tk.Button(delete_window, text="Delete", command=lambda: self.delete_doctor_action(
            id_entry.get(), delete_window))
        delete_button.pack(pady=10)

    def delete_doctor_action(self, doctor_id, delete_window):
        try:
            doctor_id = int(doctor_id)
            deleted_doctor = self.doctors.pop(doctor_id - 1)

            messagebox.showinfo("Info", f"Doctor {deleted_doctor.get_fullname()} deleted successfully.")
            delete_window.destroy()
            self.focus_force()

        except ValueError:
            messagebox.showerror("Error", "Invalid Doctor ID. Please enter a numeric value.")
        except IndexError:
            messagebox.showerror("Error", "Doctor not found. Please enter a valid Doctor ID.")

    def total_doctors(self):
        messagebox.showinfo("Info", f"Total Doctors: {len(self.doctors)}")
        self.focus_force()


class PatientManagementWindow(tk.Toplevel):
    def __init__(self, admin, patients, discharged_patients):
        super().__init__()

        self.title("Patient Management")
        self.geometry("400x300")

        self.admin = admin
        self.patients = patients
        self.discharged_patients = discharged_patients

        self.create_widgets()

    def create_widgets(self):
        menu_label = tk.Label(self, text="Patient Management")
        menu_label.pack(pady=10)

        buttons = [
            ("Register Patient", self.register_patient),
            ("View Patients", self.view_patients),
            ("Discharge Patient", self.discharge_patient),
            ("View Discharged Patient", self.view_discharged_patients),
            ("View Patients by Family", self.open_family_view_window),
            ("Close", self.destroy)
        ]

        for text, command in buttons:
            button = tk.Button(self, text=text, command=command)
            button.pack(pady=5)

    def register_patient(self):
        register_window = tk.Toplevel(self)
        register_window.title("Register Patient")
        register_window.geometry("300x500")

        # Create input fields
        first_name_label = tk.Label(register_window, text="First Name:")
        first_name_label.pack(pady=5)
        first_name_entry = tk.Entry(register_window)
        first_name_entry.pack(pady=5)

        surname_label = tk.Label(register_window, text="Surname:")
        surname_label.pack(pady=5)
        surname_entry = tk.Entry(register_window)
        surname_entry.pack(pady=5)

        age_label = tk.Label(register_window, text="Age:")
        age_label.pack(pady=5)
        age_entry = tk.Entry(register_window)
        age_entry.pack(pady=5)

        mobile_label = tk.Label(register_window, text="Mobile:")
        mobile_label.pack(pady=5)
        mobile_entry = tk.Entry(register_window)
        mobile_entry.pack(pady=5)

        postcode_label = tk.Label(register_window, text="Postcode:")
        postcode_label.pack(pady=5)
        postcode_entry = tk.Entry(register_window)
        postcode_entry.pack(pady=5)

        symptoms_label = tk.Label(register_window, text="Symptoms:")
        symptoms_label.pack(pady=5)
        symptoms_entry = tk.Entry(register_window)
        symptoms_entry.pack(pady=5)

        family_label = tk.Label(register_window, text="Family:")
        family_label.pack(pady=5)
        family_entry = tk.Entry(register_window)
        family_entry.pack(pady=5)

        # Create button to register the patient
        register_button = tk.Button(register_window, text="Register", command=lambda: self.register_patient_action(
            first_name_entry.get(), surname_entry.get(), age_entry.get(), mobile_entry.get(),
            postcode_entry.get(), symptoms_entry.get(), family_entry.get(), register_window))
        register_button.pack(pady=10)

    def register_patient_action(self, first_name, surname, age, mobile, postcode, symptoms, family, register_window):
        try:
            age = int(age)
            new_patient = Patient(first_name, surname, age, mobile, postcode, symptoms, family)
            self.admin.add_patient_to_family(new_patient)
            self.patients.append(new_patient)

            messagebox.showinfo("Success", f"Patient {new_patient.full_name()} registered successfully.")
            register_window.destroy()
            self.focus_force()

        except ValueError:
            messagebox.showerror("Error", "Invalid Age. Please enter a numeric value.")

    def view_patients(self):
        view_window = tk.Toplevel(self)
        view_window.title("View Patients")
        view_window.geometry("500x300")

        patients_label = tk.Label(view_window, text="List of Active Patients")
        patients_label.pack(pady=10)

        # Create a text widget to display the list of patients
        patients_text = tk.Text(view_window, height=10, width=50)
        patients_text.pack(pady=10)

        # Display the list of patients in the text widget
        for idx, patient in enumerate(self.patients, start=1):
            patients_text.insert(tk.END, f"{idx}. {patient.full_name()}\n")

    def view_discharged_patients(self):
        view_window = tk.Toplevel(self)
        view_window.title("View Discharged Patients")
        view_window.geometry("500x300")

        patients_label = tk.Label(view_window, text="List of Discharged Patients")
        patients_label.pack(pady=10)

        # Create a text widget to display the list of patients
        patients_text = tk.Text(view_window, height=10, width=50)
        patients_text.pack(pady=10)

        # Display the list of patients in the text widget
        for idx, patient in enumerate(self.discharged_patients, start=1):
            patients_text.insert(tk.END, f"{idx}. {patient.full_name()}\n")

    def discharge_patient(self):
        discharge_window = tk.Toplevel(self)
        discharge_window.title("Discharge Patient")
        discharge_window.geometry("300x150")

        # Create input fields
        id_label = tk.Label(discharge_window, text="Patient ID:")
        id_label.pack(pady=5)
        id_entry = tk.Entry(discharge_window)
        id_entry.pack(pady=5)

        # Create button to discharge the patient
        discharge_button = tk.Button(discharge_window, text="Discharge", command=lambda: self.discharge_patient_action(
            id_entry.get(), discharge_window))
        discharge_button.pack(pady=10)

    def discharge_patient_action(self, patient_id, discharge_window):
        try:
            patient_id = int(patient_id)
            discharged_patient = self.patients.pop(patient_id - 1)
            self.discharged_patients.append(discharged_patient)

            messagebox.showinfo("Success", f"Patient {discharged_patient.full_name()} discharged successfully.")
            discharge_window.destroy()
            self.focus_force()

        except ValueError:
            messagebox.showerror("Error", "Invalid Patient ID. Please enter a numeric value.")
        except IndexError:
            messagebox.showerror("Error", "Patient not found. Please enter a valid Patient ID.")

    def open_family_view_window(self):
        family_view_window = tk.Toplevel(self)
        family_view_window.title("View Patients by Family")
        family_view_window.geometry("500x300")

        # Create a label and a dropdown for family selection
        family_label = tk.Label(family_view_window, text="Select Family:")
        family_label.pack(pady=5)
        family_var = tk.StringVar(family_view_window)
        family_dropdown = ttk.Combobox(family_view_window, textvariable=family_var)

        # Get unique families from patients
        unique_families = set(patient.get_family() for patient in self.patients)
        family_dropdown['values'] = list(unique_families)
        family_dropdown.pack(pady=5)

        # Create a button to display patients for the selected family
        display_button = tk.Button(family_view_window, text="Display Patients",
                                   command=lambda: self.display_family_patients(
                                       family_var.get(), family_view_window))
        display_button.pack(pady=10)

    def display_family_patients(self, selected_family, family_view_window):
        family_patients_window = tk.Toplevel(family_view_window)
        family_patients_window.title(f"Patients in Family: {selected_family}")
        family_patients_window.geometry("500x300")

        # Create a text widget to display patients in the selected family
        family_patients_text = tk.Text(family_patients_window, height=10, width=50)
        family_patients_text.pack(pady=10)

        # Display the list of patients in the selected family
        for patient in self.patients:
            if patient.get_family() == selected_family:
                family_patients_text.insert(tk.END, f"{patient.full_name()} | {patient.get_symptoms()}\n")


class MedicalApp(tk.Tk):
    def __init__(self, admin):
        super().__init__()

        self.title("Medical Management System")
        self.geometry("600x400")

        self.admin = admin
        self.doctors = self.load_data_from_file('doctors.pkl')
        self.patients = self.load_data_from_file('patients.pkl')
        self.discharged_patients = self.load_data_from_file('discharged.pkl')
        self.create_widgets()

    def create_widgets(self):
        menu_label = tk.Label(self, text="Choose the operation:")
        menu_label.pack(pady=10)

        buttons = [
            ("Doctor Management", self.open_doctor_management_window),
            ("Patient Management", self.open_patient_management_window),
            ("Assign Doctor to a Patient", self.assign_doctor_to_patient),
            ("Relocate Patient", self.open_relocation_window),
            ("Update Admin Details", self.update_admin_details),
            ("Generate Report", self.generate_report_window),
            ("Save Data", self.store_data),
            ("Quit", self.quit_program)
        ]

        for text, command in buttons:
            button = tk.Button(self, text=text, command=command)
            button.pack(pady=5)

    def open_doctor_management_window(self):
        doctor_management_window = DoctorManagementWindow(self.admin, self.doctors)

    def open_patient_management_window(self):
        patient_management_window = PatientManagementWindow(self.admin, self.patients, self.discharged_patients)

    def view_discharged_patients(self):
        self.admin.view_discharge(self.discharged_patients)

    def assign_doctor_to_patient(self):
        # self.admin.assign_doctor_to_patient(self.patients, self.doctors)

        assign_window = tk.Toplevel(self)
        assign_window.title("Assign Doctor to Patient")
        assign_window.geometry("300x200")

        # Create labels and dropdowns for patient and doctor selection
        patient_label = tk.Label(assign_window, text="Select Patient:")
        patient_label.pack(pady=5)
        patient_var = tk.StringVar(assign_window)
        patient_dropdown = ttk.Combobox(assign_window, textvariable=patient_var)
        patient_dropdown['values'] = [patient.full_name() for patient in self.patients]
        patient_dropdown.pack(pady=5)

        doctor_label = tk.Label(assign_window, text="Select Doctor:")
        doctor_label.pack(pady=5)
        doctor_var = tk.StringVar(assign_window)
        doctor_dropdown = ttk.Combobox(assign_window, textvariable=doctor_var)
        doctor_dropdown['values'] = [doctor.full_name() for doctor in self.doctors]
        doctor_dropdown.pack(pady=5)

        # Create button to assign the selected doctor to the selected patient
        assign_button = tk.Button(assign_window, text="Assign Doctor", command=lambda: self.assign_doctor_action(
            patient_var.get(), doctor_var.get(), assign_window))
        assign_button.pack(pady=10)

    def assign_doctor_action(self, selected_patient, selected_doctor, assign_window):
        try:
            # Find the selected patient and doctor objects
            patient_object = next(patient for patient in self.patients if patient.full_name() == selected_patient)
            doctor_object = next(doctor for doctor in self.doctors if doctor.full_name() == selected_doctor)

            # Assign the selected doctor to the selected patient
            self.admin.assign_doctor_to_patient(doctor_object, patient_object)

            messagebox.showinfo("Success", f"Doctor {selected_doctor} assigned to Patient {selected_patient}.")
            assign_window.destroy()
            self.focus_force()

        except StopIteration:
            messagebox.showerror("Error", "Invalid Patient or Doctor selection.")
        except Exception as e:
            messagebox.showerror("Error", f"Error assigning doctor to patient: {e}")

    def update_admin_details(self):
        admin_management_window = AdminUpdateWindow(self.admin)

    def open_relocation_window(self):
        relocation_window = tk.Toplevel(self)
        relocation_window.title("Relocate Patient")
        relocation_window.geometry("400x400")

        # Create labels and dropdowns for patient and doctor selection
        patient_label = tk.Label(relocation_window, text="Select Patient:")
        patient_label.pack(pady=5)
        patient_var = tk.StringVar(relocation_window)
        patient_dropdown = ttk.Combobox(relocation_window, textvariable=patient_var)
        patient_dropdown['values'] = [patient.full_name() for patient in self.patients]
        patient_dropdown.pack(pady=5)

        old_doctor_label = tk.Label(relocation_window, text="Select Old Doctor:")
        old_doctor_label.pack(pady=5)
        old_doctor_var = tk.StringVar(relocation_window)
        old_doctor_dropdown = ttk.Combobox(relocation_window, textvariable=old_doctor_var)
        old_doctor_dropdown['values'] = [doctor.full_name() for doctor in self.doctors]
        old_doctor_dropdown.pack(pady=5)

        new_doctor_label = tk.Label(relocation_window, text="Select New Doctor:")
        new_doctor_label.pack(pady=5)
        new_doctor_var = tk.StringVar(relocation_window)
        new_doctor_dropdown = ttk.Combobox(relocation_window, textvariable=new_doctor_var)
        new_doctor_dropdown['values'] = [doctor.full_name() for doctor in self.doctors]
        new_doctor_dropdown.pack(pady=5)

        # Create button to relocate the selected patient to the new doctor
        relocate_button = tk.Button(relocation_window, text="Relocate", command=lambda: self.relocate_patient_action(
            patient_var.get(), old_doctor_var.get(), new_doctor_var.get(), relocation_window))
        relocate_button.pack(pady=10)

    def relocate_patient_action(self, selected_patient, old_doctor, new_doctor, relocation_window):
        try:
            # Find the selected patient, old doctor, and new doctor objects
            patient_object = next(patient for patient in self.patients if patient.full_name() == selected_patient)
            old_doctor_object = next(doctor for doctor in self.doctors if doctor.full_name() == old_doctor)
            new_doctor_object = next(doctor for doctor in self.doctors if doctor.full_name() == new_doctor)

            # Relocate the selected patient to the new doctor
            self.admin.relocate_patient(patient_object, old_doctor_object, new_doctor_object)

            messagebox.showinfo("Success", f"Patient {selected_patient} relocated successfully to {new_doctor}.")
            relocation_window.destroy()
            self.focus_force()

        except StopIteration:
            messagebox.showerror("Error", "Invalid Patient, Old Doctor, or New Doctor selection.")
        except Exception as e:
            messagebox.showerror("Error", f"Error relocating patient: {e}")

    def quit_program(self):
        self.destroy()

    def store_data(self):
        self.admin.store_data_to_file('doctors.pkl', self.doctors)
        self.admin.store_data_to_file('patients.pkl', self.patients)
        self.admin.store_data_to_file('discharged.pkl', self.discharged_patients)

    def load_data_from_file(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                data = pickle.load(file)
            return data
        except Exception as e:
            print(f"Error loading data from {file_path}: {e}")
            return None

    def generate_report_window(self):
        report_window = tk.Toplevel(self)
        report_window.title("System Report")
        report_window.geometry("400x300")

        # Display total number of doctors
        total_doctors_label = tk.Label(report_window, text=f"Total Doctors: {len(self.doctors)}")
        total_doctors_label.pack(pady=10)

        # Display total number of patients per doctor
        doctors_patients_label = tk.Label(report_window, text="Total Patients per Doctor:")
        doctors_patients_label.pack(pady=5)

        for doctor in self.doctors:
            patients_count = sum(1 for patient in self.patients if patient.get_doctor() == doctor)
            doctor_patients_info = f"{doctor.full_name()}: {patients_count} patients"
            doctor_patients_label = tk.Label(report_window, text=doctor_patients_info)
            doctor_patients_label.pack()

        # Display total number of patients on each illness type
        illness_types_label = tk.Label(report_window, text="Total Patients per Illness Type:")
        illness_types_label.pack(pady=5)

        illness_types_count = {}
        for patient in self.patients:
            illness_type = patient.get_symptoms()
            illness_types_count[illness_type] = illness_types_count.get(illness_type, 0) + 1

        for illness_type, count in illness_types_count.items():
            illness_label = tk.Label(report_window, text=f"{illness_type}: {count} patients")
            illness_label.pack()

        # Create a button to close the report window
        close_button = tk.Button(report_window, text="Close", command=report_window.destroy)
        close_button.pack(pady=10)

if __name__ == "__main__":
    login_window = AdminLoginWindow()
    login_window.mainloop()
