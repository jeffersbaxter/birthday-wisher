import smtplib
import datetime as dt
import random
import pandas
from hush_secrets import SECRET_EMAIL, SECRET_PASSWORD

email = SECRET_EMAIL
password = SECRET_PASSWORD
now = dt.datetime.now()

try:
    birthday_data = pandas.read_csv("birthdays.csv")
except FileNotFoundError:
    birthdays_to_remember = []
    user_input_birthdays = True
    while user_input_birthdays:
        birth_name = input("Who's birthday would you like to remember? ")
        birth_email = input("What is their email? ")
        birth_month = int(input(f"In what month is {birth_name}'s birthday - in numerical form? (e.g. February -> 2) "))
        birth_day = int(input(f"On what day is {birth_name}'s birthday? "))
        birth_year = int(input(f"In what year was {birth_name} born? "))
        birthdays_to_remember.append({
            "name": birth_name,
            "email": birth_email,
            "year": birth_year,
            "month": birth_month,
            "day": birth_day
        })
        if input("Would you like to add another birthday recipient? yes/no ") == "no":
            user_input_birthdays = False
    df = pandas.DataFrame(birthdays_to_remember)
    df.to_csv("birthdays.csv", index=False)
    birthday_data = pandas.read_csv("birthdays.csv")
finally:
    birthdays = birthday_data.to_dict(orient="records")

for birthday in birthdays:
    if now.day == birthday["day"] and now.month == birthday["month"]:
        letter_int = random.randint(1, 3)
        try:
            with open(f"letter_templates/letter_{letter_int}.txt", "r") as letter_template:
                letter = letter_template.read()
                letter = letter.replace("[NAME]", birthday["name"])
        except FileNotFoundError:
            print(f"Could not find file of letter_templates/letter_{letter_int}.txt")
        else:
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=email, password=password)
                connection.sendmail(
                    from_addr=email,
                    to_addrs=birthday["email"],
                    msg=f"Subject:Happy Birthday\n\n{letter}"
                )


