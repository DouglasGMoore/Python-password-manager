from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(symbols) for sym in range(nr_symbols)]
    password_list += [random.choice(letters) for let in range(nr_letters)]
    password_list += [random.choice(numbers) for num in range(nr_numbers)]

    random.shuffle(password_list)

    gen_password = "".join(password_list)
    password_input.insert(0, gen_password)
    pyperclip.copy(gen_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    username = name_input.get()
    psswrd = password_input.get()
    site = website_input.get()
    new_data = {site: {
        "email": username,
        "password": psswrd,
    }}

    if len(psswrd) == 0 or len(username) == 0 or len(site) == 0:
        messagebox.showinfo(title="Error", message="Do not leave any fields blank!", )
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)

        finally:
            password_input.delete(0, END)
            website_input.delete(0, END)


# ----------------------------Search-----------------------------------#
def find_password():
    site = website_input.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
                username = data[site]["email"]
                psswrd = data[site]["password"]
        except:
            messagebox.showinfo(title="Error", message=f"No details for the site {site} found")
        else:
            messagebox.showinfo(title=f"{site}", message=f"Username: {username}\nPassword: {psswrd}")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=205, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(140, 100, image=logo)
canvas.grid(column=1, row=0)

# Labels
website = Label(text="website", fg="black")
name = Label(text="name", fg="black")
password = Label(text="password", fg="black")

# Label placement
website.grid(column=0, row=1)
name.grid(column=0, row=2)
password.grid(column=0, row=3)

# Entries creation, placement, and configs
website_input = Entry(width=30)
website_input.grid(column=1, row=1, sticky="W")
website_input.focus()

name_input = Entry(width=35)
name_input.grid(column=1, row=2, columnspan=2, sticky="EW")
name_input.insert(0, "douglasg.moore@gmail.com")

password_input = Entry(width=30)
password_input.grid(column=1, row=3, sticky="W")


# Button creation placement and configs
search = Button(text="Search", command=find_password)
search.grid(column=2, row=1, sticky="EW")

generate_psw = Button(text="Generate Password", command=generator)
generate_psw.grid(column=2, row=3, sticky="EW")

save_psw = Button(text="Save", width=44, command=save_data)
save_psw.grid(column=1, row=4, columnspan=2)

window.mainloop()
