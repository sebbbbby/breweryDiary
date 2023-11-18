import re
import requests
import smtplib
import ssl
from email.message import EmailMessage

class Cocktail:
    @staticmethod
    def get_random_cocktail():
        response = requests.get(
            "https://thecocktaildb.com/api/json/v1/1/random.php")
        response = response.json()
        cocktail_name = response["drinks"][0]["strDrink"]
        cocktail_recipe = response["drinks"][0]["strInstructions"]
        return cocktail_name, cocktail_recipe

    @staticmethod
    def validate_email(email):
        pattern = r'^\S+@\S+\.\S+$'
        return re.match(pattern, email)

    @staticmethod
    def send_cocktail_email(sender_email, sender_password, recipient_email):

        if Cocktail.validate_email(recipient_email):
            cocktail_name, cocktail_recipe = Cocktail.get_random_cocktail()
            subject = "Cocktail Recipe"
            body = f"Name: {cocktail_name}\nRecipe: {cocktail_recipe}"

            em = EmailMessage()
            em["From"] = sender_email
            em["To"] = recipient_email
            em["Subject"] = subject
            em.set_content(body)

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(sender_email, sender_password)
                smtp.sendmail(sender_email, recipient_email, em.as_string())
                smtp.quit()
        else:
            print("Invalid email addresses provided. Please check your email addresses.")
