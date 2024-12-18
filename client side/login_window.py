from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from settings_window import SettingsWindow
import webbrowser
import requests
import json
import traceback

class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        loadUi('UI/login_window.ui', self)

        self.register_button.clicked.connect(self.go_to_register_page)
        self.login_button.clicked.connect(self.login)
        
        self.popup = QMessageBox()
        self.popup.setWindowTitle("Failed")

        self.show()

    def go_to_register_page(self):
        webbrowser.open('http://127.0.0.1:8000/register/')

    def login(self):
        try:
            url = 'http://127.0.0.1:8000/api/get_auth_token/'
            response = requests.post(url, data={'username': self.username_input.text(), 'password': self.password_input.text()})
            json_response = response.json()  # Simplified JSON response parsing
            
            print(response.status_code)  # Print the status code for debugging
            
            if response.ok:  # Check if the request was successful
                self.open_settings_window(json_response['token'])
            else:
                error_message = json_response.get('non_field_errors', ["Username or Password is not correct"])[0]
                self.popup.setText(error_message)
                self.popup.exec_()

        except requests.exceptions.RequestException as req_err:  # Catches HTTP-related errors
            print(f"HTTP request failed: {req_err}")
            traceback.print_exc()
            self.popup.setText("Unable to access server")
            self.popup.exec_()

        except KeyError as key_err:  # Catches missing keys in the JSON response
            print(f"Key error: {key_err}")
            traceback.print_exc()
            self.popup.setText("Unexpected server response. Please try again later.")
            self.popup.exec_()

        except Exception as e:  # Catches all other exceptions
            print(f"An error occurred: {e}")
            traceback.print_exc()
            self.popup.setText("An unexpected error occurred.")
            self.popup.exec_()

    def open_settings_window(self, token):
        self.settings_window = SettingsWindow(token)
        self.settings_window.displayInfo()
        self.close()
