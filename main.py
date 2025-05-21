import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout)
from PyQt5.QtCore import Qt

class WeatherWear(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter Name of City: ", self)
        self.city_input = QLineEdit(self) # Input field for the city name
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temp_label = QLabel(self)
        self.icon_label = QLabel(self)
        self.description_label = QLabel(self)
        self.hightemp_label = QLabel(self)
        self.lowtemp_label = QLabel(self)
        self.initUI()


    def initUI(self):
        self.setWindowTitle("Weather Wear") #Changes window title to name of application


        vbox = QVBoxLayout() # Vertical Layout for all widgets going in main window

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temp_label)
        vbox.addWidget(self.icon_label)
        vbox.addWidget(self.description_label)

        hbox = QHBoxLayout() # Horizontal layout for high and low temperature
        hbox.addWidget(self.hightemp_label)
        hbox.addWidget(self.lowtemp_label)
        vbox.addLayout(hbox)

       
        self.setLayout(vbox) # Set layout of main window to vbox

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.hightemp_label.setAlignment(Qt.AlignLeft)
        self.lowtemp_label.setAlignment(Qt.AlignRight)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temp_label.setObjectName("temp_label")
        self.icon_label.setObjectName("icon_label")
        self.description_label.setObjectName("description_label")
        self.hightemp_label.setObjectName("hightemp_label")
        self.lowtemp_label.setObjectName("lowtemp_label")

        # CSS for Styling of Widgets
        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: Arial, sans-seirif;
            }
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
            }  
            QlineEdit#city_input{
                font-size: 40px;
         }   
            QpushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
        }
            QLable#temp_label{
                     font-size: 60px;
                           }     
            QLabel#icon_label{
                font-size: 60px;
                font-family: Segoe UI emoji
            }  
            QLabel#description_label{
                font-size: 50px;
                font-style: title
                }
            QLabel#hightemp_label{
                font-size: 40px
                font-style: italic
             }
            QLabel#lowtemp_label{
               font-size: 40 px
               font-style: italic            
            }          
        """)

        self.get_weather_button.clicked.connect(self.fetch_weather) # Connect get weather button to function fecth_weather

    def fetch_weather(self): # Define fetch weather function which containts API call
        
        api_key = "587ace0885dc2f1aa299acc6469b6b01"
        city = self.city_input.text() # Fetches text from the input field of city_input
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url) # Sends Get request to the API
            response.raise_for_status() # Raises an Error within try block if requests fails
            data = response.json() # Converts response to JSON formatted data

            if data["cod"] == 200: # If response code is 200(successful) Weather data is fecthed and displayed
                self.weather_display(data)

        except requests.exceptions.HTTPError as http_error: # Error response for codes 400-500
            if response.status_code == 400:
                self.error_page("Bad Request: Recheck Input") 
            elif response.status_code == 401:
                self.error_page("Invalid API: Incorrect API Key")
            elif response.status_code == 404:
                self.error_page("City Invalid: City could not be found")
            elif response.status_code == 500:
                self.error_page("Server Error: Try again later Server down")
            elif response.status_code == 504:
                self.error_page("Gateway Timeout: No Response from server")
            else:
                self.error_page(f"HTTPError occurred: {http_error}")
                
        except requests.exceptions.ConnectionError: # Error when there is no internet connection
            self.error_page("Connection Error: Check Internet Connection")
        except requests.exceptions.Timeout: # Error when request times out
            self.error_page("Timeout Error: Request took too long to respond")
        except requests.exceptions.TooManyRedirects: # Error for too many redirects
            self.error_page("Too many redirects: Check URL")
        except requests.exceptions.RequestException as req_error: # Error response for network, Url issues
            self.error_page(f"Request Error : {req_error}")

    def error_page(self, message):
        self.temp_label.setStyleSheet("font-size: 25px; color: red")
        self.temp_label.setText(message)
        self.icon_label.clear() # Removes icon label when error occurs
        self.description_label.clear() # Removes description label when error occurs
        self.hightemp_label.clear() # Removes high temperature label
        self.lowtemp_label.clear() # Removes low temperature label

    def weather_display(self, data):
        temparature_kelvin = data["main"]["temp"] # Fetches temp in kelvin
        temperature_fahrenheit = (temparature_kelvin - 273.15) * 9/5 + 32 # Converts kelvin to farenheit

        self.temp_label.setText(f"{temperature_fahrenheit: .0f}°F")
        self.temp_label.setStyleSheet("font-size: 45px; color: white")

        self.description_label.setText(data["weather"][0]["description"].title()) # Fetches weather description
        self.description_label.setStyleSheet("font-size: 40px; color: white; font-style: title") 

        icon_id = data["weather"][0]["id"] # Fetches weather code
        self.icon_label.setText(self.get_weather_icon(icon_id, temperature_fahrenheit)) # Uses get weather method to fetch icon id
        self.icon_label.setStyleSheet("font-size: 40px; color: white")

        hightemp_fahrenheit = (data["main"]["temp_max"]-273.15) * 9/5 + 32
        self.hightemp_label.setText(f"High: {hightemp_fahrenheit: .0f}°F")
        self.hightemp_label.setStyleSheet("font-size: 35px; color: white")

        lowtemp_fahrenheit = (data["main"]["temp_min"]-273.15) * 9/5 + 32
        self.lowtemp_label.setText(f"Low: {lowtemp_fahrenheit: .0f}°F")
        self.lowtemp_label.setStyleSheet("font-size: 35px; color: white")



    @staticmethod
    def get_weather_icon(icon_id, temperature_fahrenheit):

        if 200 <= icon_id <= 232 and temperature_fahrenheit < 55: # Thunderstorms
            return "Recommended Wear:\n👒🧥👖🥾"
        elif 200 <= icon_id <= 232 and 70 >= temperature_fahrenheit >= 55:
            return "Recommended Wear:\n👒🧥👖🥾👟"
        elif 200 <= icon_id <= 232 and temperature_fahrenheit > 70:
            return "Recommended Wear:\n👒🧥👕👖🥾👟"
        elif 300 <= icon_id <= 321 and temperature_fahrenheit < 65: # Drizzle
            return "Recommended Wear:\n🧥👖👟 "
        elif 300 <= icon_id <= 321 and temperature_fahrenheit > 75:
            return "Recommended Wear:\n🧥👖👟"
        elif 500 <= icon_id <= 531 and temperature_fahrenheit < 32: # Rain
            return "Recommended Wear:\n👒🧥👖🥾 "
        elif 500 <= icon_id <= 531 and 65 <= temperature_fahrenheit >= 32:
            return "Recommended Wear:\n👒🧥👖🥾👟"
        elif 500 <= icon_id <= 531 and temperature_fahrenheit > 65: 
            return "Recommended Wear:\n🧢🧥👖🥾👟"
        elif 600 <= icon_id <= 622 and temperature_fahrenheit < 37: # Snow
            return "Recommended Wear:\n🥽🧥🎿"
        elif 600 <= icon_id <= 622 and temperature_fahrenheit >= 37:
            return "Recommended Wear:\n🧥👖🥾"
        elif 701 <= icon_id <= 741 and temperature_fahrenheit < 32: # Foggy
            return "Recommended Wear:\n🧥👖🥾👟"
        elif 701 <= icon_id <= 741 and 65 <= temperature_fahrenheit >= 32:
            return "Recommended Wear:\n🧥👖👟🥾"
        elif 701 <= icon_id <= 741 and temperature_fahrenheit > 65: # Foggy
            return "Recommended Wear:\n🧥👕👖👟"
        elif icon_id == 771 and temperature_fahrenheit < 32: # Strong Winds(Squall)
            return "Recommended Wear:\n🥽🧥👖🥾"
        elif icon_id == 771 and 50 <= temperature_fahrenheit >= 32:
            return "Recommended Wear:\n🧥👖🥾"
        elif icon_id == 771 and temperature_fahrenheit > 50: 
            return "Recommended Wear:\n🧥👕👖🥾👟"
        elif icon_id == 781 and temperature_fahrenheit < 54: # Tornado
            return "Recommended Wear:\n🧥👖🥾\t(Tornado Watch: Stay Indoors)"
        elif icon_id == 781 and temperature_fahrenheit >= 54: 
            return "Recommended Wear:\n🧥👕👖🥾\t(Tornado Watch: Stay Indoors)"
        elif icon_id == 800 and temperature_fahrenheit < 32: # Clear Sky
            return "Recommended Wear:\n🧥👖👟"
        elif icon_id == 800 and 75 <= temperature_fahrenheit >= 32: 
            return "Recommended Wear:\n🧥👕👖👟"
        elif icon_id == 800 and temperature_fahrenheit >= 75: 
            return "Recommended Wear:\n👕🩳👟🩴"
        elif 801 <= icon_id <= 804 and temperature_fahrenheit < 32: # Clouds
            return "Recommended Wear:\n🧢👒🧥👖👟🥾"
        elif 801 <= icon_id <= 804 and 75 <= temperature_fahrenheit >= 32: 
            return "Recommended Wear:\n🧢👕🧥👖👟"
        elif 801 <= icon_id <= 804 and temperature_fahrenheit > 75: 
            return "Recommended Wear:\n👕🧥👖🩳👟"
        else:
            return " "
    
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_wear = WeatherWear()
    weather_wear.show()
    sys.exit(app.exec_())