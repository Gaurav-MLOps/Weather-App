import sys
import requests
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from API import api_key_real




class SimpleWeather(QWidget):
    def __init__(self):
        super().__init__()
        self.city_text = QLabel("City:", self)
        self.city_input = QLineEdit(self)
        self.check_button = QPushButton("Check Weather", self)
        self.temp_display = QLabel(self)
        self.icon_display = QLabel(self)
        self.info_display = QLabel(self)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Weather Checker")

        layout = QVBoxLayout()
        layout.addWidget(self.city_text)
        layout.addWidget(self.city_input)
        layout.addWidget(self.check_button)
        layout.addWidget(self.temp_display)
        layout.addWidget(self.icon_display)
        layout.addWidget(self.info_display)

        self.setLayout(layout)

        for widget in [self.city_text, self.city_input, self.temp_display, self.icon_display, self.info_display]:
            widget.setAlignment(Qt.AlignCenter)

        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: Calibri;
            }
            QLabel#city_text {
                font-size: 30px;
                font-style: italic;
            }
            QLineEdit {
                font-size: 28px;
            }
            QPushButton {
                font-size: 25px;
                font-weight: bold;
            }
            QLabel#temp_display {
                font-size: 70px;
            }
            QLabel#icon_display {
                font-size: 90px;
            }
            QLabel#info_display {
                font-size: 40px;
            }
        """)

        self.city_text.setObjectName("city_text")
        self.temp_display.setObjectName("temp_display")
        self.icon_display.setObjectName("icon_display")
        self.info_display.setObjectName("info_display")

        self.check_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = api_key_real
        city = self.city_input.text().strip()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            r = requests.get(url)
            r.raise_for_status()
            weather = r.json()

            if weather["cod"] == 200:
                self.show_weather(weather)
        except Exception as e:
            self.show_error(str(e))

    def show_error(self, message):
        self.temp_display.setText("Error")
        self.icon_display.setText("⚠️")
        self.info_display.setText(message)

    def show_weather(self, data):
        kelvin = data["main"]["temp"]
        temps = np.array([kelvin])
        celsius = temps - 273.15
        fahrenheit = (temps * 9/5) - 459.67

        weather_id = data["weather"][0]["id"]
        description = data["weather"][0]["description"]

        self.temp_display.setText(f"{celsius[0]:.0f}° | {fahrenheit[0]:.0f}°F")
        self.icon_display.setText(self.pick_icon(weather_id))
        self.info_display.setText(description.capitalize())

    @staticmethod
    def pick_icon(code):
        if 200 <= code <= 232: 
            return "⛈️" 
        elif 300 <= code <= 321: 
            return "🌩️" 
        elif 500 <= code <= 531:
             return "🌧️"
        elif 600 <= code <= 622: 
            return "❄️" 
        elif 701 <= code <= 741: 
            return "🌫️" 
        elif code == 762: 
            return "🌋" 
        elif code == 771: 
            return "💨" 
        elif code == 781: 
            return "🌪️" 
        elif code == 800: 
            return "☀️" 
        elif 801 <= code <= 804: 
            return "☁️" 
        else: return ""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleWeather()
    window.show()
    sys.exit(app.exec_())