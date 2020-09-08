from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json, glob
from datetime import datetime
from pathlib import Path
import random

Builder.load_file('design.kv')

# Starting screen of the app where a user can log in, sign up, or retrieve password
class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"

    def login(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        
        if uname in users and users[uname]['password'] == pword:
            self.manager.current = "login_screen_success"
        else:
            self.ids.login_wrong.text = "Wrong username or password!"

    def forgot_password(self):
        self.manager.current = "forgot_password_screen"


class RootWidget(ScreenManager):
    pass

# User may signup for an account with username, password, 
# and answer to provided security question. Info saved in json file
class SignUpScreen(Screen):
    def add_user(self, uname, pword, answer):
        with open("users.json") as file:
            users = json.load(file)

        users[uname] = {'username': uname, 'password': pword, 'security_question': answer,
            'created':datetime.now().strftime("%Y-%m-%d %H-%M-%S")}

        with open("users.json", 'w') as file:
            json.dump(users, file)

        self.manager.current = "sign_up_screen_success"

# User is directed back to login screen after successfully signing up
class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

# Once user logins in the are brought to the main screen of the app
# where they can input a feeling to recieve a corresponding quote
class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

    # Returns a random quote from the corresponding txt file in the 
    # quotes folder
    def get_quote(self, feel):
        feel = feel.lower()
        available_feelings = glob.glob("quotes/*txt")

        available_feelings = [Path(filename).stem for filename in 
                                available_feelings]

        if feel in available_feelings:
            with open(f"quotes/{feel}.txt", encoding="utf8") as file:
                quotes = file.readlines()
            
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another feeling"

# Provides the hover attirbute of the logout image from the main app screen
class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass

# User can retrieve their password by entering their username and
# correctly answering the security question and return to login page
class ForgotPasswordScreen(Screen):
    def check_security(self, sec_answer, uname):
        with open("users.json") as file:
            users = json.load(file)

        if uname in users and users[uname]['security_question'] == sec_answer:
            self.ids.wrong_creds.text = "Your password is: " + str(users[uname]['password'])
        else:
            self.ids.wrong_creds.text = "Wrong username or answer!"
    
    def back_to_login(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"
           
class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()