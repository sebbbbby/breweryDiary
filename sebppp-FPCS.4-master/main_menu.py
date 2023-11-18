import sys
from diary import Diary
from cocktail import Cocktail
from dotenv import load_dotenv
import os
import requests
from prettytable import PrettyTable

class main_menu:
    modes = {
        1: "Check Diary",
        2: "Search breweries by city",
        3: "Manually Add Brewery",
        4: "Send Cocktail Recipe",
    }

    def __init__(self, mode=None) -> None:
        self.mode = mode
        self.diary = Diary()

    def welcome(self):
        print('Welcome to my Brewery Diary!')
        for key, value in self.modes.items():
            print(f"{key}. {value}")

    def mode_select(self):
        self.mode = None
        while self.mode is None:
            self.welcome()
            try:
                choice = input(
                    "Enter your choice: (Type 'exit' to quit) ").lower()
                if choice == "exit":
                    print("Goodbye")
                    sys.exit()
                self.mode = int(choice)
                if 1 <= self.mode <= 4:
                    return self.mode
                else:
                    print("Please enter a number between 1 and 4")
            except ValueError:
                print("Please enter a number between 1 and 4")

    def menu_diary(self):
        self.diary.view_diary()

    def search_by_city(self):
        while True:
            city = input('Enter a city: ')
            BREW_LIMIT = 20
            try:
                api_url = f'https://api.openbrewerydb.org/v1/breweries?by_city={city}&per_page={BREW_LIMIT}'
                response = requests.get(api_url)

                if response.status_code == 200:
                    data = response.json()
                    if not data:
                        print('No Brewery Data Available, Please Try Another City')
                        continue
                    else:
                        table = PrettyTable()
                        table.field_names = [
                            "#", "Brewery Name", "Brewery Type"]

                        for idx, brewery in enumerate(data, 1):
                            brewery_name = brewery['name']
                            brewery_type = brewery['brewery_type']
                            table.add_row([idx, brewery_name, brewery_type])

                        print(table)
                        self.show_brewery_info(data)
                        break
                else:
                    print('Error: API request unsuccessful.')
            except requests.exceptions.RequestException as e:
                print('Error: API request unsuccessful.')
                print(e)

    def show_brewery_info(self, data):
        while True:
            choice = input(
                "Enter the number of the brewery you want to know more about (or 'n' to exit): ")
            if choice.lower() == 'n':
                break
            elif choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(data):
                    brewery_info = data[idx - 1]

                    brewery_table = PrettyTable()
                    brewery_table.field_names = ["", "Brewery"]
                    brewery_table.add_row(["Name", brewery_info['name']])
                    brewery_table.add_row(
                        ["Address", f"{brewery_info['address_1']}, {brewery_info['city']}, {brewery_info['state_province']} {brewery_info['postal_code']}"])
                    brewery_table.add_row(
                        ["Website", brewery_info['website_url']])

                    print(brewery_table)

                    add_to_diary = input(
                        "Do you want to add this brewery to your diary (y/n)? ").lower()
                    if add_to_diary == 'y':
                        self.diary.add_brewery_to_diary(brewery_info)
                        print(f"{brewery_info['name']} added to your diary.")
                else:
                    print("Invalid number. Please enter a valid number.")
            else:
                print("Invalid input. Please enter a number or 'n' to exit.")

    def menu_send_cocktail(self):
        load_dotenv('.env')
        sender_email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")
        cocktail = Cocktail()
        recipient_email = input("Enter your email address: ")
        if cocktail.validate_email(recipient_email):
            cocktail.send_cocktail_email(
                sender_email, password, recipient_email)
        else:
            print("Invalid recipient email address. Please check the email address.")
    
    def manually_add_brewery(self):
        self.diary.add_brewery_manually()
