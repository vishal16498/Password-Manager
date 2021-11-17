import json
import random
from tkinter import *
from tkinter import messagebox

import pyperclip  # copy/paste to clipboard


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_passwords():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letters_list = [random.choice(letters) for _ in range(random.randint(8, 10))]     # 8-10 letter password
    symbol_list = [random.choice(symbols) for _ in range(random.randint(2, 4))]       # 2-4 symbols
    number_list = [random.choice(numbers) for _ in range(random.randint(2, 4))]       # 2- 4 numbers
    password_list = letters_list + symbol_list + number_list
    random.shuffle(password_list)
    password_string = "".join(password_list)
    password_entry.insert(0, password_string)
    pyperclip.copy(password_string)     # copies password to clipboard
# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website_ = website_entry.get().title()
    username_ = username_entry.get()
    password_ = password_entry.get()
    credentials = {
        website_: {
            "Email": username_,
            "Password": password_
        }
    }   # json format/ dictionary

    if len(website_) == 0 or len(username_) == 0 or len(password_) == 0:
        messagebox.showerror(title="Error", message="Please fill the blank field")
    else:
        is_ok = messagebox.askokcancel(title="Are you sure?", message=f" {website_}\nUsername/Email: {username_}\n "
                                                                      f"Password: {password_}")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
                    # update old data to new/append to end of the file
                    data.update(credentials)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                data = credentials
                # creating a new file and dump to the file
            finally:
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)

        website_entry.delete(0, END)
        username_entry.delete(0, END)
        password_entry.delete(0, END)


def search():
    site_name = website_entry.get().title()
    try:
        with open("data.json", "r") as search_data:
            database = json.load(search_data)
            if site_name in database:
                messagebox.showinfo(title=f"Your credentials for {site_name} are: ", message=f" Username: {database[site_name]['Email']}, \n Password: {database[site_name]['Password']}")
            else:
                messagebox.showinfo(title="Oops", message="Doesn't exist")
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        messagebox.showerror(title="Error", message="Please add your first credential to create the file")
# ---------------------------- UI SETUP ------------------------------- #


DEFAULT_FONT = ("Sans serif", 10, "normal")
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)
lock_image = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200, highlightthickness=0)
canvas.create_image(100, 100, image=lock_image)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:", font=DEFAULT_FONT)
website_label.grid(column=0, row=1)

username_label = Label(text="Email/Username:", font=DEFAULT_FONT)
username_label.grid(column=0, row=2)

password_label = Label(text="Password:", font=DEFAULT_FONT)
password_label.grid(column=0, row=3)

website_entry = Entry(width=38)
website_entry.grid(column=1, row=1, columnspan=2)
website_entry.focus()
website_name = website_entry.get()

search_button = Button(text="Search", font=DEFAULT_FONT, command=search)
search_button.grid(column=4, row=1)

username_entry = Entry(width=38)
username_entry.grid(column=1, row=2, columnspan=2)
username = username_entry.get()

password_entry = Entry(width=38)
password_entry.grid(column=1, row=3, columnspan=2)
password = password_entry.get()

generate_password = Button(text="Generate Password", font=DEFAULT_FONT, command=generate_passwords)
generate_password.grid(column=4, row=3)

add_button = Button(text="Add", width=20, font=DEFAULT_FONT, command=save)
add_button.grid(column=1, row=4)

window.mainloop()
