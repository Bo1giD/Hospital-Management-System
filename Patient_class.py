class Patient:
    """Patient class"""

    def __init__(self, first_name, surname, age, mobile, postcode, symptoms, family):
        """
        Args:
            first_name (string): First name
            surname (string): Surname
            age (int): Age
            mobile (string): the mobile number
            address (string): address
        """

        self.__first_name = first_name
        self.__surname = surname
        self.__age = age
        self.__mobile = mobile
        self.__postcode = postcode
        self.__symptoms = symptoms
        self.__family = family
        self.__doctor = 'None'

    def full_name(self):
        """full name is first_name and surname"""
        return self.__first_name + " " + self.__surname

    def get_doctor(self):
        return self.__doctor

    def link(self, doctor):
        """Args: doctor(string): the doctor full name"""
        self.__doctor = doctor

    def get_symptoms(self):
        return self.__symptoms

    def print_symptoms(self):
        print(self.__symptoms)

    def get_family(self):
        return self.__family

    def __str__(self):
        return f'{self.full_name():^30}|{self.__doctor:^30}|{self.__age:^5}|{self.__mobile:^15}|{self.__postcode:^10}'
