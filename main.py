from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_button():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols
    shuffle(password_list)
    password = ''.join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_button():
    new_data = {
        website_entry.get().capitalize(): {
            "email": email_user_entry.get(),
            "password": password_entry.get()
        }
    }

    if len(website_entry.get()) == 0 or len(password_entry.get()) == 0:
        messagebox.showinfo(title="Oh no!", message="Please make sure you haven't left any fields empty.")

    elif len(password_entry.get()) < 8:
        messagebox.showinfo(title="Oh no!", message="Please make sure the password is 8 in length.")
        password_entry.focus()
    else:
        try:
            with open('data.json', mode='r') as data_file:
                # Reading the data
                data = json.load(data_file)
        except FileNotFoundError:
            with open('data.json', mode='w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating the old data
            data.update(new_data)

            with open('data.json', mode='w') as data_file:
                # Saving the updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- SEARCH ------------------------------------------- #
def find_password():
    website = website_entry.get().capitalize()
    try:
        with open('data.json') as data_file:
            # Reading the data
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title='Error', message="No Data File Found")
    else:
        if website in data:
            email = data[website]['email']
            password = data[website]['password']
            messagebox.showinfo(title=f'{website}', message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title='Error', message=f"No details for {website} exists")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)

# -- Labels --
website_lbl = Label(text="Website:", font=("Arial", 12, "bold"))
email_user_lbl = Label(text="Email/Username:", font=("Arial", 12, "bold"))
pass_lbl = Label(text="Password:", font=("Arial", 12, "bold"))

# -- Entry --
website_entry = Entry(width=33)
website_entry.focus()
email_user_entry = Entry(width=57)
email_user_entry.insert(0, "jrs.cseworks@gmail.com")
password_entry = Entry(width=33)

# -- Button --
generate_button = Button(text="Generate Password", font=("Arial", 8, "bold"), width=19, highlightthickness=0,
                         command=generate_button)
add_button = Button(text="Add", font=("Arial", 10, "bold"), width=42, highlightthickness=0, command=add_button)
search_button = Button(text='Search', font=("Arial", 8, "bold"), width=19, highlightthickness=0,
                       command=find_password)

# -- Grids --
canvas.grid(column=1, row=0)
website_lbl.grid(column=0, row=1, sticky=E)
website_entry.grid(column=1, row=1, columnspan=1, sticky=W)
email_user_lbl.grid(column=0, row=2, sticky=E)
email_user_entry.grid(column=1, row=2, columnspan=2, sticky=W)
pass_lbl.grid(column=0, row=3, sticky=E)
password_entry.grid(column=1, row=3, columnspan=2, sticky=W)
search_button.grid(column=2, row=1, columnspan=1, stick=W)
generate_button.grid(column=2, row=3, columnspan=1, sticky=W)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()