import json
from datetime import date
import datetime
import ekgdata

class Person:
    def __init__(self, person_dict) -> None:
        self.id = person_dict["id"]
        self.firstname = person_dict["firstname"]
        self.lastname = person_dict["lastname"]
        self.date_of_birth = person_dict["date_of_birth"]
        self.picture_path = person_dict["picture_path"]
        self.age = Person.calc_age(self, self.date_of_birth)
        self.max_heartrate = ekgdata.EKGdata.estimate_max_hr(self.age, "male")
        self.person_dict = Person.load_by_id(self, self.id) # oder mit der Methode find_person_data_by_name

    def calc_age(self, date_of_birth):
        """Eine Funktion die das Alter einer Person berechnet und zurück gibt"""
        today = date.today()
        return today.year - date_of_birth
    
    def load_by_id(self, id):
        """ Eine Funktion der ID als ein String übergeben wird
        und die die Person als Dictionary zurück gibt"""
        person_data = Person.load_person_data()
        #print(suchstring)
        if id == "None":
            return {}

        for eintrag in person_data:
            print(eintrag)
            if eintrag["id"] == id:
                print()
                return eintrag
        else:
            return {}
    @staticmethod
    def find_person_data_by_name(suchstring):
        """ Eine Funktion der Nachname, Vorname als ein String übergeben wird
        und die die Person als Dictionary zurück gibt"""
        person_data = Person.load_person_data()
        #print(suchstring)
        if suchstring == "None":
            return {}

        two_names = suchstring.split(", ")
        vorname = two_names[1]
        nachname = two_names[0]

        for eintrag in person_data:
            print(eintrag)
            if (eintrag["lastname"] == nachname and eintrag["firstname"] == vorname):
                print()

                return eintrag
        else:
            return {}
    @staticmethod
    def load_person_data():
        """A Function that knows where te person Database is and returns a Dictionary with the Persons"""
        file = open("data/person_db.json")
        person_data = json.load(file)
        return person_data
    
    @staticmethod
    def get_person_list(person_data):
        """A Function that takes the persons-dictionary and returns a list auf all person names"""
        list_of_names = []

        for eintrag in person_data:
            list_of_names.append(eintrag["lastname"] + ", " +  eintrag["firstname"])
        return list_of_names


if __name__ == "__main__":
    print("This is a module with some functions to read the person data")
    persons = Person.load_person_data()
    person_names = Person.get_person_list(persons)
    print(person_names)
    print(Person.find_person_data_by_name("Huber, Julian"))