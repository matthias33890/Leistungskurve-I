import json
from datetime import date
import ekgdata

class Person:
    def __init__(self, person_dict) -> None:
        """
        Initialize the Person object with the given dictionary containing person data.
        
        Parameters:
        - person_dict: Dictionary containing person's details.
        """
        self.id = person_dict["id"]
        self.firstname = person_dict["firstname"]
        self.lastname = person_dict["lastname"]
        self.date_of_birth = person_dict["date_of_birth"]
        self.picture_path = person_dict["picture_path"]
        
        # Calculate the age of the person
        self.age = Person.calc_age(self, self.date_of_birth)
        
        # Estimate the maximum heart rate for the person
        self.max_heartrate = ekgdata.EKGdata.estimate_max_hr(self.age, "male")
        
        # Load the person's data by their ID
        self.person_dict = Person.load_by_id(self, self.id)

    def calc_age(self, date_of_birth):
        """
        Calculate the age of the person based on their date of birth.
        
        Parameters:
        - date_of_birth: Year of birth as an integer.
        
        Returns:
        - Age of the person as an integer.
        """
        today = date.today()
        return today.year - date_of_birth
    
    def load_by_id(self, id):
        """
        Load the person's data by their ID.
        
        Parameters:
        - id: Unique identifier for the person as a string.
        
        Returns:
        - Dictionary containing person's details if the ID is found, otherwise an empty dictionary.
        """
        person_data = Person.load_person_data()
        
        if id == "None":
            return {}

        for eintrag in person_data:
            if eintrag["id"] == id:
                return eintrag
        
        return {}
    
    @staticmethod
    def find_person_data_by_name(suchstring):
        """
        Find a person's data by their name.
        
        Parameters:
        - suchstring: String containing the person's last name and first name separated by a comma.
        
        Returns:
        - Dictionary containing person's details if the name is found, otherwise an empty dictionary.
        """
        person_data = Person.load_person_data()
        
        if suchstring == "None":
            return {}

        two_names = suchstring.split(", ")
        vorname = two_names[1]
        nachname = two_names[0]

        for eintrag in person_data:
            if eintrag["lastname"] == nachname and eintrag["firstname"] == vorname:
                return eintrag
        
        return {}
    
    @staticmethod
    def load_person_data():
        """
        Load the person database and return it as a dictionary.
        
        Returns:
        - Dictionary containing all person records.
        """
        with open("data/person_db.json") as file:
            person_data = json.load(file)
        return person_data
    
    @staticmethod
    def get_person_list(person_data):
        """
        Get a list of all person names from the person data dictionary.
        
        Parameters:
        - person_data: Dictionary containing all person records.
        
        Returns:
        - List of strings with the format 'lastname, firstname' for each person.
        """
        list_of_names = []

        for eintrag in person_data:
            list_of_names.append(eintrag["lastname"] + ", " +  eintrag["firstname"])
        
        return list_of_names

if __name__ == "__main__":
    print("This is a module with some functions to read the person data")
    
    # Load all person data
    persons = Person.load_person_data()
    
    # Get a list of all person names
    person_names = Person.get_person_list(persons)
    print(person_names)
    
    # Find a specific person's data by name
    print(Person.find_person_data_by_name("Huber, Julian"))
