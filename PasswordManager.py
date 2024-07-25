# 100 DAYS OF CODE USING PYTHON
# INSTRUCTOR: ANGELA YU
# Project 29 : Password Manager using Tkinter
# BY HOULAYMATOU B. | @code_techhb
# January 19, 2024

from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

BACKGROUND = "#CEDE48"
LARGE_ENTRY = 40
FONT = ("Arial", 12, "bold")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    # Password Generator Project
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 12)
    nr_symbols = random.randint(2, 6)
    nr_numbers = random.randint(2, 7)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_numbers + password_letters + password_symbols

    random.shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    # TODO let's get hold of each entry
    website = site_name_entry.get()
    email = email_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
            "Email": email,
            "Username": username,
            "Password": password,
        }
    }
    if len(email) == 0 or len(password) == 0 or len(website) == 0:
        messagebox.showerror(title="Error", message=f"Please make sure to fill in all the fields")
    else:
        # TOdo add a pop up message
        is_ok = messagebox.askokcancel(title="Confirm", message=f"Are you sure you want to save: Email: {email}\n"
                                                                f"Username: {username}\nPassword: {password}\nfor {website}?")
        if is_ok:
            # TODO format the data and write in the datafile
            try:
                # Open and write to json file
                with open("confidential.json", "r") as password_manager:
                    # how to read a json file
                    data = json.load(password_manager)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                with open("confidential.json", "w") as password_manager:
                    json.dump(new_data, password_manager, indent=4)
            else:
                # how to update a json file
                data.update(new_data)
                with open("confidential.json", "w") as password_manager:
                    # saving updated data
                    json.dump(data, password_manager, indent=4)
            finally:
                # TODO clear the entries once added to the datafile
                site_name_entry.delete(0, END)
                email_entry.delete(0, END)
                username_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- Find data in the JSON file ------------------------------- #
def find_data():
    website = site_name_entry.get()
    try:
        # find site in the json file
        with open("confidential.json") as database:
            current_data = json.load(database)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        messagebox.showerror(title="Error", message=f"Sorry! You haven't saved such data.")
    else:
        # get hold of the email, pass, username value in a nested dico
        if website in current_data:
            # let's check if the data is in the database
            email = current_data[website]["Email"]
            username = current_data[website]["Username"]
            password = current_data[website]["Password"]
            messagebox.showinfo(
                title=website,
                message=f"Your data for {website}\n\nEmail: {email}\nUsername: {username}\npassword:{password}")
        else:
            messagebox.showerror(message=f"Sorry! You haven't saved any data for {website}.")


# ---------------------------- UI SETUP ------------------------------- #

# Window
window = Tk()
window.title("Password Manager")
window.config(bg=BACKGROUND, padx=50, pady=50)

# Canvas for logo
canvas = Canvas(width=210, height=210, bg=BACKGROUND, highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(150, 100, image=logo)
canvas.grid(column=1, row=0)

# Labels, Entries and Buttons
site_name_label = Label(text="Webiste:", bg=BACKGROUND, font=FONT)
site_name_label.grid(column=0, row=1)
email_label = Label(text="Email:", bg=BACKGROUND, font=FONT)
email_label.grid(column=0, row=2)
username_label = Label(text="Username:", bg=BACKGROUND, font=FONT)
username_label.grid(column=0, row=3)
password_label = Label(text="Password:", bg=BACKGROUND, font=FONT)
password_label.grid(column=0, row=4)

site_name_entry = Entry(window, width=23, highlightthickness=0)
site_name_entry.grid(column=1, row=1, columnspan=1, pady=10, sticky=W)
site_name_entry.focus()

email_entry = Entry(window, width=LARGE_ENTRY, highlightthickness=0)
email_entry.grid(column=1, row=2, columnspan=2, pady=10, sticky=W)

username_entry = Entry(window, width=LARGE_ENTRY, highlightthickness=0)
username_entry.grid(column=1, row=3, columnspan=2, pady=10, sticky=W)

password_entry = Entry(window, width=23, highlightthickness=0)
password_entry.grid(column=1, row=4, pady=10, sticky=W)

generate_pass = Button(text="Generate Password", command=password_generator, highlightbackground=BACKGROUND)
generate_pass.grid(column=2, row=4)
add_button = Button(text="Secure", command=save, width=36, highlightbackground=BACKGROUND, )
add_button.grid(column=1, row=5, columnspan=3)

search_button = Button(text="Search", highlightbackground=BACKGROUND, width=13, command=find_data)
search_button.grid(column=2, row=1)

window.mainloop()
