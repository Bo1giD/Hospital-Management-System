import pickle

from Doctor_class import Doctor


class Admin:
    """A class that deals with the Admin operations"""

    def __init__(self, username, password, address=''):
        """
        Args:
            username (string): Username
            password (string): Password
            address (string, optional): Address Defaults to ''
        """

        self.__username = username
        self.__password = password
        self.__address = address
        self.__patients_by_family = {}

    def login(self, username, password):
        """
        A method that deals with the login
        Raises:
            Exception: returned when the username and the password ...
                    ... don`t match the data registered
        Returns:
            string: the username
        """

        if username == self.__username and password == self.__password:
            return True
        else:
            return False

    def get_username(self):
        return self.__username

    def set_username(self, un):
        self.__username = un

    def get_password(self):
        return self.__password

    def set_password(self, pw):
        self.__password = pw

    def get_address(self):
        return self.__address

    def set_address(self, add):
        self.__address = add

    def find_index(self, index, doctors):
        # check that the doctor id exists
        if index in range(0, len(doctors)):
            return True
        # if the id is not in the list of doctors
        else:
            return False

    def view_doctors(self, doctors):
        print("-----List of Doctors-----")
        list_of_doctors = range(len(doctors))
        for i in list_of_doctors:
            doctors_tuple = doctors[i]
            name = doctors[i].get_first_name()
            surname = doctors[i].get_surname()
            print(f"{str(i + 1) : <5}{name : ^15}{surname : >10}")

    def view(self, a_list):
        """
        print a list
        Args:
            a_list (list): a list of printables
        """
        for index, item in enumerate(a_list):
            print(f'{index + 1:3}|{item}')

    def get_doctor_details(self):
        name = input("Please add a Doctor's first name: ")
        surname = input("Please add the Doctor's surname: ")
        speciality = input("Doctor's specialty: ")
        new_doctor = name + surname + speciality
        # doctors.append(new_doctor)
        print(name + "," + surname + "," "specialty:" + speciality)
        """
        Get the details needed to add a doctor
        Returns:
            first name, surname and ...
                            ... the speciality of the doctor in that order.
        """
        return f'{name} {surname} {speciality}'

    def view_discharge(self, discharged_patients):
        """
        Prints the list of all discharged patients
        Args:
            discharge_patients (list<Patients>): the list of all the non-active patients
        """

        print("-----Discharged Patients-----")
        print('ID |          Full Name           |      Doctor`s Full Name      | Age |    Mobile     | Postcode ')

        for idx, patient in enumerate(discharged_patients):
            print(
                f'{idx + 1} | {patient.full_name():<30} | {patient.get_assigned_doctor().full_name() if patient.get_assigned_doctor() else "Not Assigned":<28} | {patient.get_age():<3} | {patient.get_mobile():<14} | {patient.get_postcode():<8}')

    def discharge(self, patients, discharge_patients):
        """
        Allow the admin to discharge a patient when treatment is done
        Args:
            patients (list<Patients>): the list of all the active patients
            discharge_patients (list<Patients>): the list of all the non-active patients
        """
        print("-----Discharge Patient-----")

        while True:
            # Print list of patients
            print('ID |          Full Name           |      Doctor`s Full Name      | Age |    Mobile     | Postcode ')
            for idx, patient in enumerate(patients):
                print(
                    f'{idx + 1} | {patient.full_name():<30} | {patient.get_assigned_doctor().full_name() if patient.get_assigned_doctor() else "Not Assigned":<28} | {patient.get_age():<3} | {patient.get_mobile():<14} | {patient.get_postcode():<8}')

            discharge_option = input("Do you want to discharge a patient? (Y/N): ").upper()

            if discharge_option == "N":
                print("Exiting discharge procedure. ")
                break  # Exit the loop if the user enters "N"

            elif discharge_option == "Y":
                patient_index = input("Please enter the patient ID: ")

                try:
                    # patient_index is the patient ID minus one (-1)
                    patient_index = int(patient_index) - 1

                    # check if the id is not in the list of patients
                    if patient_index not in range(len(patients)):
                        print("The id entered was not found. ")
                        continue  # Continue to the next iteration of the loop

                    # Move the patient from the active list to the discharged list
                    discharged_patient = patients.pop(patient_index)
                    discharge_patients.append(discharged_patient)

                    print("Patient discharged successfully. ")

                except ValueError:  # the entered id could not be changed into an int
                    print("The id entered is incorrect. ")

            else:
                print("Invalid option. Please enter Y or N. ")

    def assign_doctor_to_patient(self, doctor, patient):
        patient.link(doctor)
        doctor.add_patient(patient)

    def update_details(self):
        """
        Allows the user to update and change username, password and address
        """

        print('Choose the field to be updated:')
        print(' 1 Username')
        print(' 2 Password')
        print(' 3 Address')
        op = int(input('Input: '))

        if op == 1:
            new_username = input("Enter a new username: ")
            self.__username = new_username
            print("Username updated successfully. ")

        elif op == 2:
            password = input('Enter the new password: ')
            # validate the password
            if password == input('Enter the new password again: '):
                self.__password = password
                print("Password updates successfully. ")

        elif op == 3:
            new_adress = input("Enter the new address: ")
            self.__adress = new_adress
            print("Adress updates successfully. ")

        else:
            print("Invalid option. Please choose 1,2, or 3. ")

    def add_patient_to_family(self, patient):
        family = patient.get_family()
        if family not in self.__patients_by_family:
            self.__patients_by_family[family] = [patient]
        else:
            self.__patients_by_family[family].append(patient)

    def relocate_patient(self, patient, old_doctor, new_doctor):
        try:
            patient.link(new_doctor)
            new_doctor.add_patient(patient)
            old_doctor.remove_patient(patient)
            return True
        except ValueError:
            return False

    def store_data_to_file(self, file_path, data):
        try:
            with open(file_path, 'wb') as file:
                pickle.dump(data, file)
            return True
        except Exception as e:
            print(f"Error storing data to {file_path}: {e}")
            return False

