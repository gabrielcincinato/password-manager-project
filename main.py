from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
import string


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def password_generate():
    
    password_entry.delete(0, END)
    letters = list(string.ascii_letters)
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    random_letters = [random.choice(letters) for char in range(random.randint(8, 10))]
    random_symbols = [random.choice(symbols) for char in range(random.randint(2, 4))]
    random_numbers = [random.choice(numbers) for char in range(random.randint(2, 4))]

    password_list = random_letters + random_symbols + random_numbers

    random.shuffle(password_list)
    password_entry.insert(index=0, string=''.join(password_list))
    pyperclip.copy(''.join(password_list))


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():

    website = website_entry.get()
    email = email_user_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "Email": email,
            "Password": password
        }
    }
    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="Oops", message="Don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as file:
                # Reading old data
                data = json.load(file)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)
            with open("data.json", "w") as file:
                # Saving updated data
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


def search_website():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            website = website_entry.get()
            message = data[website]
    except FileNotFoundError:
        messagebox.showwarning(title="Error", message="File not found")
    except KeyError:
        messagebox.showwarning(title="Error", message="Website not found")
    else:
        messagebox.showinfo(title="Account details",
                            message=f"Email: {message['Email']}\n"
                                    f"Password: {message['Password']}")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager"),
window.config(padx=50, pady=50, bg="white")

# Image
canvas = Canvas(width=200, height=200, bg='white', highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(100,100, image=logo)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:", bg="white")
website_label.grid(column=0, row=1)

email_user_label = Label(text="Email/Username:", bg="white")
email_user_label.grid(column=0, row=2)

password_label = Label(text="Password:", bg="white")
password_label.grid(column=0, row=3)

# Entries
website_entry = Entry(width=32, bg='white')
website_entry.grid(column=1, row=1, sticky='ew')
website_entry.focus()

email_user_entry = Entry(width=51, bg="white")
email_user_entry.grid(column=1, row=2, columnspan=2, sticky='ew')
email_user_entry.insert(0, "example@example.com")

password_entry = Entry(width=32, bg="white")
password_entry.grid(column=1, row=3, sticky='ew')

# Buttons
generate_password = Button(text="Generate Password", command=password_generate)
generate_password.grid(column=2, row=3, sticky='ew')

add = Button(text="Add", width=43, command=save)
add.grid(column=1, row=4, columnspan=2, sticky='ew')

search_button = Button(text="Search", width=14, command=search_website)
search_button.grid(column=2, row=1, sticky='ew')

window.mainloop()
