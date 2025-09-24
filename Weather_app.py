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

        main_layout = QVBoxLayout()
        city_layout = QHBoxLayout()
        city_layout.addWidget(self.city_text)
        city_layout.addWidget(self.city_input)
        city_layout.addWidget(self.history_button)

        main_layout.addLayout(city_layout)
        main_layout.addWidget(self.check_button)
        main_layout.addWidget(self.temp_display)
        main_layout.addWidget(self.icon_display)
        main_layout.addWidget(self.info_display)
        main_layout.addWidget(self.history_display)

        self.setLayout(main_layout)

        for widget in [self.city_text, self.city_input, self.temp_display, self.icon_display, self.info_display]:
            widget.setAlignment(Qt.AlignCenter)

        self.info_display.setWordWrap(True)

        self.setStyleSheet("""
        QWidget {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                stop:0 #6B7280, stop:0.5 #3B82F6, stop:1 #1E3A8A);
            color: #F3F4F6;
            border-radius: 15px;
            padding: 10px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
        }
        QLabel, QPushButton, QTextEdit {
            font-family: 'Poppins', 'Segoe UI', Calibri, sans-serif;
        }
        QLabel#city_text {
            font-size: 28px;
            font-weight: 700;
            font-style: italic;
            color: #E0E7FF;
            margin-bottom: 8px;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
            letter-spacing: 0.5px;
        }
        QLineEdit {
            font-size: 22px;
            padding: 8px 10px;
            border: 2px solid rgba(147, 197, 253, 0.5);
            border-radius: 10px;
            background-color: rgba(255, 255, 255, 0.15);
            color: #FFFFFF;
            margin: 8px 15px;
            transition: all 0.3s ease;
        }
        QLineEdit:focus {
            border-color: #93C5FD;
            background-color: rgba(255, 255, 255, 0.25);
            box-shadow: 0 0 10px rgba(147, 197, 253, 0.6);
            transform: scale(1.01);
        }
        QPushButton {
            font-size: 20px;
            font-weight: bold;
            padding: 10px;
            border-radius: 10px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                stop:0 #60A5FA, stop:1 #2563EB);
            color: #FFFFFF;
            border: none;
            margin: 8px 15px;
            transition: all 0.3s ease;
            box-shadow: 0 3px 12px rgba(37, 99, 235, 0.3);
        }
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                stop:0 #93C5FD, stop:1 #3B82F6);
            transform: translateY(-2px);
            box-shadow: 0 5px 18px rgba(59, 130, 246, 0.4);
        }
        QPushButton:pressed {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                stop:0 #2563EB, stop:1 #1E3A8A);
            transform: translateY(1px);
            box-shadow: 0 2px 8px rgba(37, 99, 235, 0.2);
        }
        QLabel#temp_display {
            font-size: 50px;
            font-weight: 600;
            font-family: 'Segoe UI', 'Helvetica', sans-serif;
            color: #DBEAFE;
            margin: 12px 0;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
        }
        QLabel#icon_display {
            font-size: 70px;
            font-family: "Segoe UI Emoji";
            margin: 8px 0;
            text-shadow: 1px 1px 6px rgba(0, 0, 0, 0.3);
            transform: scale(1);
            transition: transform 0.3s ease;
        }
        QLabel#icon_display:hover {
            transform: scale(1.05);
        }
        QLabel#info_display {
            font-size: 24px;
            color: #E0E7FF;
            margin: 8px 15px;
            padding: 8px;
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            box-shadow: 0 3px 12px rgba(0, 0, 0, 0.15);
            transition: all 0.3s ease;
        }
        QTextEdit {
            font-size: 16px;
            background-color: rgba(255,255,255,0.1);
            color: #E0E7FF;
            border-radius: 8px;
            padding: 10px;
            margin: 10px;
        }
        """)

        self.city_text.setObjectName("city_text")
        self.temp_display.setObjectName("temp_display")
        self.icon_display.setObjectName("icon_display")
        self.info_display.setObjectName("info_display")

        self.check_button.clicked.connect(self.get_weather)
        self.history_button.clicked.connect(self.show_history)

        self.setFixedWidth(400)
        self.setMinimumHeight(480)

        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

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
            self.history_display.show()
        else:
            self.history_display.setText("No history available")
            self.history_display.show()

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
