import sys
import requests
import numpy as np
import pandas as pd
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit
from PyQt5.QtCore import Qt
from API import api_key_real


class SimpleWeather(QWidget):
    def __init__(self):
        super().__init__()
        self.weather_log = pd.DataFrame(columns=["City", "Celsius", "Fahrenheit", "Description", "Time"])
        

        self.city_text = QLabel("City:", self)
        self.city_input = QLineEdit(self)
        self.check_button = QPushButton("Check Weather", self)
        self.history_button = QPushButton("Show History", self)
        self.temp_display = QLabel(self)
        self.icon_display = QLabel(self)
        self.info_display = QLabel(self)
        
 
        self.history_display = QTextEdit(self)
        self.history_display.setReadOnly(True)
        self.history_display.hide()
        
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Weather Checker")


        left_layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.city_text)
        input_layout.addWidget(self.city_input)
        input_layout.addWidget(self.history_button)
        left_layout.addLayout(input_layout)
        left_layout.addWidget(self.check_button)
        left_layout.addWidget(self.temp_display)
        left_layout.addWidget(self.icon_display)
        left_layout.addWidget(self.info_display)
        left_layout.addStretch()  

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.history_display)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, 3)
        main_layout.addLayout(right_layout, 2)
        self.setLayout(main_layout)

 
        for widget in [self.city_text, self.city_input, self.temp_display, self.icon_display, self.info_display]:
            widget.setAlignment(Qt.AlignCenter)
        self.info_display.setWordWrap(True)

        self.check_button.clicked.connect(self.get_weather)
        self.history_button.clicked.connect(self.toggle_history)


        self.setFixedWidth(600)
        self.setMinimumHeight(480)
        self.setStyleSheet("""
        QWidget {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #6B7280, stop:0.5 #3B82F6, stop:1 #1E3A8A);
            color: #F3F4F6;
            border-radius: 15px;
            padding: 10px;
        }
        QLabel, QPushButton, QTextEdit {
            font-family: 'Poppins', 'Segoe UI', Calibri, sans-serif;
        }
        QLineEdit {
            font-size: 18px;
            padding: 6px;
            border-radius: 8px;
            background-color: rgba(255, 255, 255, 0.15);
            color: #FFFFFF;
        }
        QPushButton {
            font-size: 16px;
            padding: 8px;
            border-radius: 8px;
            background: #2563EB;
            color: #FFFFFF;
            border: none;
        }
        QTextEdit {
            font-size: 14px;
            background-color: rgba(255,255,255,0.1);
            color: #E0E7FF;
            border-radius: 8px;
            padding: 8px;
        }
        QLabel#temp_display { font-size: 40px; font-weight: 600; color: #DBEAFE; }
        QLabel#icon_display { font-size: 60px; font-family: "Segoe UI Emoji"; }
        QLabel#info_display { font-size: 20px; padding: 6px; background-color: rgba(255,255,255,0.1); border-radius: 6px; }
        """)
        self.city_text.setObjectName("city_text")
        self.temp_display.setObjectName("temp_display")
        self.icon_display.setObjectName("icon_display")
        self.info_display.setObjectName("info_display")

    def toggle_history(self):
        if self.history_display.isVisible():
            self.history_display.hide()
            self.history_button.setText("Show History")
        else:
            self.show_history()
            self.history_display.show()
            self.history_button.setText("Hide History")

    def get_weather(self):
        api_key = api_key_real
        city = self.city_input.text().strip()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        try:
            r = requests.get(url)
            weather = r.json()
            if weather.get("cod") == 200:
                self.show_weather(weather)
            else:
                self.show_error(weather.get("message", "Unknown error"))
        except Exception as e:
            self.show_error(str(e))

    def show_error(self, message):
        self.temp_display.setText("Error")
        self.icon_display.setText("⚠️")
        if "city not found" in message.lower():
            msg = "City not found 🚫"
        elif "500" in message or "internal" in message.lower():
            msg = "Server error ⚡"
        else:
            msg = "Something went wrong ❌"
        self.info_display.setText(msg)

    def show_weather(self, data):
        kelvin = data["main"]["temp"]
        temps = np.array([kelvin])
        celsius = temps - 273.15
        fahrenheit = (temps * 9/5) - 459.67
        city = self.city_input.text().strip()
        description = data["weather"][0]["description"]

        self.temp_display.setText(f"{celsius[0]:.0f}° | {fahrenheit[0]:.0f}°F")
        self.icon_display.setText(self.pick_icon(data["weather"][0]["id"]))
        self.info_display.setText(description.capitalize())

        new_entry = {
            "City": city,
            "Celsius": round(celsius[0], 2),
            "Fahrenheit": round(fahrenheit[0], 2),
            "Description": description,
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.weather_log = pd.concat([self.weather_log, pd.DataFrame([new_entry])], ignore_index=True)
        self.weather_log.to_csv("weather_log.csv", index=False)

    def show_history(self):
        if not self.weather_log.empty:
            last_entries = self.weather_log.tail(10)
            self.history_display.setText(last_entries.to_string(index=False))
        else:
            self.history_display.setText("No history available")

    @staticmethod
    def pick_icon(code):
        if 200 <= code <= 232:
            return "⚡️"
        elif 300 <= code <= 321:
            return "💧"
        elif 500 <= code <= 531:
            return "☔"
        elif 600 <= code <= 622:
            return "🌨️"
        elif 701 <= code <= 741:
            return "💨"
        elif code == 762:
            return "🔥"
        elif code == 771:
            return "🌬️"
        elif code == 781:
            return "🌪️"
        elif code == 800:
            return "🌞"
        elif 801 <= code <= 804:
            return "⛅"
        else:
            return "🌈"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleWeather()
    window.show()
    sys.exit(app.exec_() or 0)
