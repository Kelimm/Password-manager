import customtkinter as ctk
import os
from PIL import Image
from cryptography.fernet import Fernet
import secrets
import string

# Generate and store the encryption key if it doesn't exist
if not os.path.exists("login_app.txt"):
    key = Fernet.generate_key()
    with open("Key.key", "wb") as key_file:
        key_file.write(key)

# Load the encryption key from the file
def load_key():
    return open("Key.key", "rb").read()

# Decrypt the file with the given name
def decrypt_file(name):
    key = load_key()
    instance = Fernet(key)
    with open(name, "rb") as f:
        encrypted = f.read()
    decrypted = instance.decrypt(encrypted)
    with open(name, "wb") as f:
        f.write(decrypted)
        
# Encrypt the file with the given name
def encrypt_file(name):
    key = load_key()
    instance = Fernet(key)
    with open(name, "rb") as f :
        content = f.read()
    encrypted_content = instance.encrypt(content)
    with open(name, "wb") as f:
        f.write(encrypted_content)

# Configure the grid layout for a frame
def configure_grid(frame, rows, columns):
    for i in range(rows):
        frame.rowconfigure(i, weight=1)
    for j in range(columns):
        frame.columnconfigure(j, weight=1)

# Create a frame with the given parameters
def create_frame(parent, x, y, width, height, border_width=None, fg_color=None):
    frame = ctk.CTkFrame(parent, border_width=border_width, fg_color=fg_color)
    frame.place(relx=x, rely=y, relwidth=width, relheight=height)
    return frame

# Main application class
class App(ctk.CTk):
    # Initialize the app
    def __init__(self):
        super().__init__()
        self.title("Password manager")
        self.geometry("1200x600")
        self.minsize(1200, 600)

        # Create instances of RegisterPage and LoginPage
        self.register_page = RegisterPage(self)
        self.login_page = LoginPage(self)
        self.main_page = MainPage(self)

        self.login_page.place_forget()
        self.main_page.place_forget()
        self.register_page.place_forget()

        # Check if an account already exist
        if os.path.exists("login_app.txt"):
            with open("login_app.txt", "r") as f:
                content = f.read().strip()
                if content:
                    self.show_login_page()
        else:
            self.show_register_page()

        self.mainloop()

    def show_register_page(self):
        self.register_page.place(
            relx=0.5, rely=0.5, anchor="center", relwidth=0.4, relheight=0.65
        )

    def show_login_page(self):
        # Hide the register page and show the login page
        self.register_page.place_forget()
        self.login_page.place(
            relx=0.5, rely=0.5, anchor="center", relwidth=0.4, relheight=0.65
        )

    def show_main_page(self):
        self.login_page.place_forget()
        self.main_page.place(
            relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.95
        )

class RegisterPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.place(
            relx=0.5, rely=0.5, anchor="center", relwidth=0.25, relheight=0.4
        ) 

        self.create_widget()
        self.display_widget()

    def create_widget(self):
        font_title = ctk.CTkFont(family="Outfit", size=26, weight="bold")
        font_label = ctk.CTkFont(family="Outfit", size=22)
        font_input = ctk.CTkFont(family="Outfit", size=17)

        self.title_label = ctk.CTkLabel(self, text="Register", font=font_title)
        self.login_label = ctk.CTkLabel(self, text="Login:", font=font_label)
        self.login_input = ctk.CTkEntry(self, font=font_input, placeholder_text="Login")

        self.pwd1_label = ctk.CTkLabel(self, text="Password:", font=font_label)
        self.pwd1_input = ctk.CTkEntry(self, font=font_input, show="*", placeholder_text="*******")

        self.pwd2_label = ctk.CTkLabel(self, text="Repeat Password:", font=font_label)
        self.pwd2_input = ctk.CTkEntry(self, font=font_input, show="*", placeholder_text="*******")

        self.register_button = ctk.CTkButton(
            self, text="Register", font=font_label, command=self.register
        )

        self.error_label = ctk.CTkLabel(
            self, text="", font=font_label, text_color="red"
        )

    def display_widget(self):
        configure_grid(self, rows=9, columns=1)

        self.title_label.grid(row=0, column=0, pady=10)
        self.login_label.grid(row=1, column=0, sticky="w", pady=5, padx=10)
        self.login_input.grid(row=2, column=0, sticky="ew", pady=5, padx=10)

        self.pwd1_label.grid(row=3, column=0, sticky="w", pady=5, padx=10)
        self.pwd1_input.grid(row=4, column=0, sticky="ew", pady=5, padx=10)

        self.pwd2_label.grid(row=5, column=0, sticky="w", pady=5, padx=10)
        self.pwd2_input.grid(row=6, column=0, sticky="ew", pady=5, padx=10)

        self.register_button.grid(row=7, column=0, pady=20)
        self.error_label.grid(row=8, column=0, pady=5)

    # Handle the registration process
    def register(self):
        # Get the passwords from the input fields
        pwd1 = self.pwd1_input.get()
        pwd2 = self.pwd2_input.get()

        # Check if the passwords match
        if pwd1 != pwd2:
            self.error_label.configure(text="Passwords do not match")
        else:
            self.error_label.configure(text="")
            credentials = {"login": self.login_input.get(), "pwd": pwd1}
            with open("login_app.txt", "a") as f:
                for key, value in credentials.items():
                    f.write(f"\n{key}: {value}")
            
            encrypt_file("login_app.txt")
            self.parent.show_login_page()

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.place(
            relx=0.5, rely=0.5, anchor="center", relwidth=0.3, relheight=0.3
        )  # Place the frame in the center
        self.create_widget()
        self.display_widget()

    def create_widget(self):
        font_title = ctk.CTkFont(family="Outfit", size=26, weight="bold")
        font_label = ctk.CTkFont(family="Outfit", size=22)
        font_input = ctk.CTkFont(family="Outfit", size=17)

        self.title_label = ctk.CTkLabel(self, text="Login", font=font_title)
        self.login_label = ctk.CTkLabel(self, text="Login:", font=font_label)
        self.login_input = ctk.CTkEntry(self, font=font_input, placeholder_text="Login")

        self.pwd_label = ctk.CTkLabel(self, text="Password:", font=font_label)
        self.pwd_input = ctk.CTkEntry(self, font=font_input, show="*", placeholder_text="*******")

        self.login_button = ctk.CTkButton(
            self, text="Login", font=font_label, command=self.login
        )

        self.error_label = ctk.CTkLabel(
            self, text="", font=font_label, text_color="red"
        )

    def display_widget(self):
        configure_grid(self, rows=7, columns=1)

        self.title_label.grid(row=0, column=0, pady=10)
        self.login_label.grid(row=1, column=0, sticky="w", pady=(2,5), padx=10)
        self.login_input.grid(row=2, column=0, sticky="ew", pady=(2,5), padx=10)

        self.pwd_label.grid(row=3, column=0, sticky="w", pady=(2,5), padx=10)
        self.pwd_input.grid(row=4, column=0, sticky="ew", pady=(2,5), padx=10)

        self.login_button.grid(row=5, column=0, pady=(20,10))
        self.error_label.grid(row=6, column=0, pady=5)

    # Handle the login process
    def login(self):
        login = self.login_input.get()
        pwd = self.pwd_input.get()

        decrypt_file("login_app.txt")
            
        with open("login_app.txt", "r") as f:
            credentials = f.readlines()

        credentials_dict = {}
        for line in credentials:
            if line.strip():
                key, value = line.strip().split(": ")
                credentials_dict[key] = value

        if (
            credentials_dict.get("login") == login
            and credentials_dict.get("pwd") == pwd
        ):
            encrypt_file("login_app.txt")
            self.parent.show_main_page()
           
        else:
            self.error_label.configure(
                text="Invalid login or password", text_color="red"
            )

class MainPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.95)

        font_label = ctk.CTkFont(family="Outfit", size=20)
        font_input = ctk.CTkFont(family="Outfit", size=15)

        left_part = create_frame(self, x=0, y=0, width=0.3, height=1, border_width=1)
        right_part = create_frame(self, x=0.3, y=0, width=0.7, height=1)
        right_part_top = create_frame(right_part, x=0, y=0, width=1, height=0.15, fg_color=right_part.cget("fg_color"), border_width=1)

        self.right_part_bot = ctk.CTkScrollableFrame(right_part,)
        self.right_part_bot.place(relx=0, rely=0.15, relwidth=1, relheight=0.85)
        
        configure_grid(right_part_top, rows=1, columns=2)

        self.name_entry, self.login_entry, self.pwd_entry = self.create_site_login_password_fields(left_part, font_label, font_input)
        self.create_button(left_part, font_label)
        self.create_password_generator(left_part, font_label, font_input)
    
        self.create_search_bar(right_part_top, font_input, fg_color=right_part.cget("fg_color"))

        self.site_credentials = []
        
        self.load_credentials()
        

    def create_search_bar(self, parent, font_input, fg_color):
        search_frame = ctk.CTkFrame(parent, fg_color=fg_color)
        search_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        search_bar_logo = ctk.CTkLabel(
            search_frame, image=self.load_image("./search.png", 20, 20), text=""
        )
        search_bar_logo.pack(side="left", padx=5)

        search_bar_entry = ctk.CTkEntry(search_frame, font=font_input, placeholder_text="Search...")
        search_bar_entry.pack(side="left", fill="x", expand=True, padx=5)
        search_bar_entry.bind("<KeyRelease>", self.search_bar_logic)

    def search_bar_logic(self, event):
        name_filter = event.widget.get().lower()
        for site_credential in self.site_credentials :
            site_name = site_credential.website_name.lower()
            if site_name.startswith(name_filter):
                site_credential.pack(side="top", fill="x", padx=10, pady=(10, 5))

            else:
                site_credential.pack_forget()

    def create_button(self, parent, font):
        button_add = ctk.CTkButton(parent, text="Add", font=font, command=lambda : self.button_add_logic(self.right_part_bot))
        button_add.grid(row=4, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

    def button_add_logic(self,parent):
        site_name = self.name_entry.get().strip()
        login = self.login_entry.get().strip()
        pwd = self.pwd_entry.get().strip()
        
        if not site_name or not login or not pwd:
            pass
        else:
            site_credential = SiteCredentials(parent=parent,website_name=self.name_entry.get(), login=self.login_entry.get(), pwd=self.pwd_entry.get()) 
            self.site_credentials.append(site_credential)
            
            if not os.path.exists("credentials.txt"):
                with open("credentials.txt", "a") as f:
                    f.write(f"{site_name},{login},{pwd}\n")
                    encrypt_file("credentials.txt")
                    
            else :
                decrypt_file("credentials.txt")
                with open("credentials.txt", "a") as f:
                    f.write(f"{site_name},{login},{pwd}\n")
                encrypt_file("credentials.txt")

            
            self.clear_entries()


    def clear_entries(self):
        self.name_entry.delete(0, 'end')
        self.login_entry.delete(0, 'end')
        self.pwd_entry.delete(0, 'end')
            
    def create_site_login_password_fields(self, parent, font_label, font_input):
        name_entry = self.create_label_entry_pair(
            parent, "Site Name:", font_label, font_input, 0, pady=(20, 5)
        )
        login_entry = self.create_label_entry_pair(
            parent, "Login:", font_label, font_input, 1, pady=5
        )
        pwd_entry = self.create_label_entry_pair(
            parent, "Password:", font_label, font_input, 2, pady=5, show="*"
        )
        return name_entry, login_entry, pwd_entry

    def create_label_entry_pair(self, parent, label_text, font_label, font_input, row, pady, show=None):
        label = ctk.CTkLabel(parent, text=label_text, font=font_label)
        label.grid(row=row, column=0, padx=10, pady=pady, sticky="w")
        entry = ctk.CTkEntry(parent, font=font_input, show=show)
        entry.grid(row=row, column=1, padx=10, pady=pady, sticky="ew")
        return entry

    def load_image(self, path, x, y):
        image = Image.open(path)
        image = image.resize((20, 20))
        return ctk.CTkImage(image)

    def create_password_generator(self, parent, font_label, font_input):
        self.generated_password_input = ctk.CTkEntry(parent, font=font_input)
        self.generated_password_input.grid(
            row=5, column=0, padx=10, pady=(20, 10), sticky="ew", columnspan=2
        )

        self.generate_password_button = ctk.CTkButton(
            parent, text="Generate Password", font=font_label, command=self.generate_password
        )
        self.generate_password_button.grid(
            row=6, column=0, padx=10, pady=5, sticky="ew", columnspan=2
        )

    def generate_password(self):
        # Define the characters to use in the password
        characters = string.ascii_letters + string.digits + string.punctuation
        # Generate a random password
        password = ''.join(secrets.choice(characters) for i in range(12))
        # Insert the generated password into the input field
        self.generated_password_input.delete(0, 'end')
        self.generated_password_input.insert(0, password)

    def load_credentials(self):
        if os.path.exists("credentials.txt"):
            decrypt_file("credentials.txt")
            with open("credentials.txt", "r") as f:
                lines = f.readlines()
                for line in lines:
                    name, login, pwd = line.strip().split(",")
                    site_credential = SiteCredentials(parent=self.right_part_bot, website_name=name, login=login, pwd=pwd) 
                    self.site_credentials.append(site_credential) 
            encrypt_file("credentials.txt")

                    
class SiteCredentials(ctk.CTkFrame):
    def __init__(self, parent, website_name, login, pwd):
        super().__init__(parent)
        self.website_name = website_name
        self.pack(side="top", fill="x", padx=10, pady=(10, 5))
        
        font = ctk.CTkFont(family="Outfit", size=15)
        
        # Create labels and entries for website name, login, and password
        website_label = ctk.CTkLabel(self, text="Website:", font=font)
        website_label.pack(side="left", padx=10, pady=15)
        website_entry = ctk.CTkEntry(self, font=font)
        website_entry.insert(0, website_name)
        website_entry.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        
        login_label = ctk.CTkLabel(self, text="Login:", font=font)
        login_label.pack(side="left", padx=5, pady=5)
        login_entry = ctk.CTkEntry(self, font=font)
        login_entry.insert(0, login)
        login_entry.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        
        pwd_label = ctk.CTkLabel(self, text="Password:", font=font)
        pwd_label.pack(side="left", padx=5, pady=5)
        pwd_entry = ctk.CTkEntry(self, font=font, show="*")
        pwd_entry.insert(0, pwd)
        pwd_entry.pack(side="left", padx=10, pady=5, fill="x", expand=True)
        
        # Bind events to show/hide password
        pwd_entry.bind("<FocusIn>", lambda e: pwd_entry.configure(show=""))
        pwd_entry.bind("<FocusOut>", lambda e: pwd_entry.configure(show="*"))
        
        delete_button = ctk.CTkButton(self, text="X", width=20, command= lambda : self.delete(website_name, login, pwd))
        delete_button.pack(side="right", padx=5, pady=5)

    def delete(self, website_name, login, pwd):
        # Destroy the current SiteCredentials widget
        self.destroy()
        decrypt_file("credentials.txt")
        with open("credentials.txt", "r") as f:
            lines = f.readlines()
            
           # Open the credentials file in write mode to overwrite it
        with open("credentials.txt", "w") as f:
            for line in lines:
                # Split each line into name, login, and password
                name_file, login_file, pwd_file = line.strip().split(",")
                # Write the line back to the file if it does not match the credentials to be deleted
                if (name_file, login, pwd) != (website_name, login_file, pwd_file):
                    f.write(line)
        encrypt_file("credentials.txt")

        

app = App()
