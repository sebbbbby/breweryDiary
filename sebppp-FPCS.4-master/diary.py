import json
from prettytable import PrettyTable
import uuid

class Diary:
    def __init__(self) -> None:
        self.JSON_FILE = 'data/diary.json'
        self.brewery_data = []

    def load_diary_data(self):
        try:
            with open(self.JSON_FILE, 'r') as json_file:
                data = json.load(json_file)
                if 'seb' in data:
                    seb_data = data['seb']
                    self.brewery_data = seb_data.get('breweries', [])
                else:
                    print("User 'seb' not found in the diary.")
        except FileNotFoundError:
            print("Diary file not found. Creating a new diary.")

    def save_diary_data(self):
        data = {'seb': {'breweries': self.brewery_data}}
        with open(self.JSON_FILE, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def view_diary(self):
        while True:
            self.load_diary_data()
            brewery_table = self.create_brewery_table()
            print(brewery_table)

            edit_diary = input(
                "Do you want to edit your diary (y/n)? ").lower()
            if edit_diary == 'n':
                break
            elif edit_diary == 'y':
                self.edit_diary_entry()
                brewery_table = self.create_brewery_table()
                print(brewery_table)

    def create_brewery_table(self):
        table = PrettyTable()
        table.field_names = ["#", "Brewery Name", "City", "Review", "Visited"]

        for idx, brewery in enumerate(self.brewery_data, 1):
            brewery_name = brewery['name']
            city = brewery['city']
            review = brewery.get('review', 'No review available')
            visited = 'Yes' if brewery.get('visited', False) else 'No'

            table.add_row([idx, brewery_name, city, review, visited])

        return table

    def edit_diary_entry(self):
        try:
            brewery_num = int(input("Enter the number of the brewery you want to edit or delete: "))
            if 1 <= brewery_num <= len(self.brewery_data):
                brewery = self.brewery_data[brewery_num - 1]
                print(f"Editing brewery #{brewery_num}: {brewery['name']}")
                
                edit_action = input("Do you want to edit (E) or delete (D) this brewery entry? ").lower()
                
                if edit_action.lower() == 'e':
                    new_review = input("Enter the new review: ")
                    new_visited = input("Has it been visited (y/n)? ").lower() == 'y'
                    brewery['review'] = new_review
                    brewery['visited'] = new_visited
                    print("Brewery entry updated.")
                elif edit_action.lower() == 'd':
                    confirm = input("Are you sure you want to delete this brewery entry (y/n)? ").lower()
                    if confirm.lower() == 'y':
                        del self.brewery_data[brewery_num - 1]
                        print(f"Brewery entry #{brewery_num} deleted.")
                    else:
                        print("Deletion canceled.")
                
                self.save_diary_data()
            else:
                print("Invalid brewery number. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def add_brewery_to_diary(self, brewery_info):
        self.load_diary_data() 
        new_brewery = {
            'id': brewery_info['id'],
            'name': brewery_info['name'],
            'brewery_type': brewery_info['brewery_type'],
            'address_1': brewery_info['address_1'],
            'address_2': brewery_info['address_2'],
            'address_3': brewery_info['address_3'],
            'city': brewery_info['city'],
            'state_province': brewery_info['state_province'],
            'postal_code': brewery_info['postal_code'],
            'country': brewery_info['country'],
            'longitude': brewery_info['longitude'],
            'latitude': brewery_info['latitude'],
            'phone': brewery_info['phone'],
            'website_url': brewery_info['website_url'],
            'state': brewery_info['state'],
            'street': brewery_info['street'],
            'review': 'no',
            'visited': False,
        }

        self.brewery_data.append(new_brewery) 
        self.save_diary_data() 

    def add_brewery_manually(self):
        self.load_diary_data()
        unique_id = str(uuid.uuid4())
        new_brewery = {
            'id': unique_id,
            'name': input("Enter the brewery name: ") or None,
            'address_1': input("Enter the brewery address (no City): ") or None,
            'phone': input("Enter the phone number: ") or None,
            'state_province': input("Enter the state or province: ") or None,
            'city': input("Enter the city: ") or None,
            'website_url': input("Enter the website URL: ") or None,
            'brewery_type': input("Enter the brewery type: ") or None,
            'address_2': None,
            'address_3': None,
            'postal_code': None,
            'country': None,
            'longitude': None,
            'latitude': None,
            'street': None,
            'review': 'none',
            'visited': False,
        }
        print(f"{new_brewery['name']} has been added to your diary.")
        self.brewery_data.append(new_brewery)
        self.save_diary_data()
