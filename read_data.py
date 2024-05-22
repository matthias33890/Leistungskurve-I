import json

def load_person_data():
    """A Function that knows where te person Database is and returns a Dictionary with the Persons"""
    file = open("data/person_db.json")
    person_data = json.load(file)
    return person_data

def get_person_list():
    """A Function that returns a List of Persons"""
    person_data = []
    for person in load_person_data():
        person_data.append(person["lastname"] + ", " + person["firstname"])
    return person_data

def find_person_data_by_name(suchstring):
    """ Eine Funktion der Nachname, Vorname als ein String übergeben wird
    und die die Person als Dictionary zurück gibt"""

    person_data = load_person_data()
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

if __name__ == "__main__":
    print(load_person_data())
    print(get_person_list())