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

        self.info_display.setWordWrap(True)

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #1E3A8A, stop:0.3 #3B82F6, stop:0.6 #60A5FA, stop:1 #93C5FD);
                color: #FFFFFF;
                border-radius: 20px;
                padding: 15px;
                box-shadow: 0 8px 40px rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(147, 197, 253, 0.3);
            }
            QLabel, QPushButton, QLineEdit {
                font-family: 'Poppins', 'Segoe UI', 'Helvetica Neue', sans-serif;
            }
            QLabel#city_text {
                font-size: 32px;
                font-weight: 800;
                font-style: italic;
                color: #DBEAFE;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4);
                letter-spacing: 1px;
                transition: all 0.4s ease;
            }
            QLabel#city_text:hover {
                transform: scale(1.05);
                color: #EFF6FF;
            }
            QLineEdit {
                font-size: 24px;
                padding: 12px 15px;
                border: 2px solid rgba(96, 165, 250, 0.6);
                border-radius: 15px;
                background-color: rgba(255, 255, 255, 0.2);
                color: #FFFFFF;
                margin: 10px 20px;
                transition: all 0.4s ease;
            }
            QLineEdit:focus {
                border-color: #BFDBFE;
                background-color: rgba(255, 255, 255, 0.3);
                box-shadow: 0 0 15px rgba(96, 165, 250, 0.8);
                transform: scale(1.02);
            }
            QPushButton {
                font-size: 22px;
                font-weight: bold;
                padding: 12px;
                border-radius: 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #2563EB, stop:0.5 #3B82F6, stop:1 #60A5FA);
                color: #FFFFFF;
                border: none;
                margin: 10px 20px;
                transition: all 0.4s ease;
                box-shadow: 0 4px 16px rgba(59, 130, 246, 0.4);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #3B82F6, stop:0.5 #60A5FA, stop:1 #93C5FD);
                transform: translateY(-3px) scale(1.02);
                box-shadow: 0 8px 24px rgba(96, 165, 250, 0.5);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #1E40AF, stop:0.5 #2563EB, stop:1 #3B82F6);
                transform: translateY(2px) scale(0.98);
                box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
            }
            QLabel#temp_display {
                font-size: 60px;
                font-weight: 700;
                font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
                color: #EFF6FF;
                margin: 15px 0;
                text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.4);
                transition: all 0.4s ease;
            }
            QLabel#temp_display:hover {
                transform: scale(1.03);
            }
            QLabel#icon_display {
                font-size: 80px;
                font-family: "Segoe UI Emoji";
                margin: 10px 0;
                text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.4);
                transition: transform 0.4s ease, color 0.4s ease;
            }
            QLabel#icon_display:hover {
                transform: scale(1.1) rotate(5deg);
                color: #DBEAFE;
            }
            QLabel#info_display {
                font-size: 26px;
                color: #E0E7FF;
                margin: 10px 20px;
                padding: 10px;
                background-color: rgba(255, 255, 255, 0.15);
                border-radius: 12px;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
                transition: all 0.4s ease;
            }
            QLabel#info_display:hover {
                background-color: rgba(255, 255, 255, 0.25);
                transform: scale(1.02);
            }
        """)

        self.city_text.setObjectName("city_text")
        self.temp_display.setObjectName("temp_display")
        self.icon_display.setObjectName("icon_display")
        self.info_display.setObjectName("info_display")

        self.check_button.clicked.connect(self.get_weather)

        self.setFixedWidth(320)
        self.setMinimumHeight(400)

        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

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

        weather_id = data["weather"][0]["id"]
        description = data["weather"][0]["description"]

        self.temp_display.setText(f"{celsius[0]:.0f}° | {fahrenheit[0]:.0f}°F")
        self.icon_display.setText(self.pick_icon(weather_id))
        self.info_display.setText(description.capitalize())

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