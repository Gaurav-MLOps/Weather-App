import sys
import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QDialog
)
from PyQt5.QtCore import Qt
from API import api_key_real

class HistoryWindow(QDialog):
    def __init__(self, weather_log, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Weather History")
        self.setFixedSize(450, 500)

        self.history_display = QTextEdit(self)
        self.history_display.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.history_display)
        self.setLayout(layout)

        if not weather_log.empty:
            history_text = ""
            last_entries = weather_log.tail(20).sort_values(by="Time", ascending=False)
            
            temps = last_entries['Celsius'].values
            avg_temp = np.round(np.mean(temps), 1)
            history_text += f"📊 Average Temp: {avg_temp}°C\n"

            most_searched = weather_log['City'].mode().values[0]
            history_text += f"📍 Most Searched City: {most_searched}\n"
            history_text += "------------------------------\n"

            for _, row in last_entries.iterrows():
                temp_icon = ""
                if row['Celsius'] >= 35:
                    temp_icon = "🔥"
                elif row['Celsius'] <= 5:
                    temp_icon = "❄️"

                entry_time = datetime.strptime(row['Time'], "%Y-%m-%d %H:%M:%S")
                now = datetime.now()
                if entry_time.date() == now.date():
                    time_str = f"Today at {entry_time.strftime('%I:%M %p')}"
                elif entry_time.date() == (now - timedelta(days=1)).date():
                    time_str = f"Yesterday at {entry_time.strftime('%I:%M %p')}"
                else:
                    time_str = entry_time.strftime("%d %b %Y at %I:%M %p")

                highlight = "⭐" if row['City'] == most_searched else ""

                history_text += f"{highlight}🌆 City: {row['City']}\n"
                history_text += f"🌡 Temperature: {row['Celsius']}°C | {row['Fahrenheit']}°F {temp_icon}\n"
                history_text += f"☁ Weather: {row['Description'].capitalize()}\n"
                history_text += f"🕒 Time: {time_str}\n"
                history_text += "------------------------------\n"

            self.history_display.setText(history_text)
        else:
            self.history_display.setText("No history available")

        self.history_display.setStyleSheet(
            "font-size:16px;\n"
            "line-height:1.5em;\n"
        )

class SimpleWeather(QWidget):
    def __init__(self):
        super().__init__()

        self.weather_log = pd.DataFrame(
            columns=["City", "Celsius", "Fahrenheit", "Description", "Time"]
        )

        self.city_text = QLabel("City:", self)
        self.city_input = QLineEdit(self)
        self.check_button = QPushButton("Check Weather", self)
        self.history_button = QPushButton("📜 Show History", self)
        self.temp_display = QLabel(self)
        self.icon_display = QLabel(self)
        self.info_display = QLabel(self)

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

        self.setLayout(main_layout)

        for widget in [
            self.city_text,
            self.city_input,
            self.temp_display,
            self.icon_display,
            self.info_display
        ]:
            widget.setAlignment(Qt.AlignCenter)

        self.info_display.setWordWrap(True)

        self.setStyleSheet(
    """
    QWidget {
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:1,
            stop:0 #667eea, stop:0.5 #764ba2, stop:1 #f093fb
        );
        color: #FFFFFF;
        border-radius: 20px;
        font-family: 'Segoe UI', 'Poppins', sans-serif;
    }

    QLabel#city_text {
        font-size: 24px;
        font-weight: 600;
        color: rgba(255,255,255,0.9);
        background: rgba(255,255,255,0.1);
        padding: 8px 16px;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
    }

    QLineEdit {
        font-size: 18px;
        padding: 12px 16px;
        border-radius: 15px;
        background: rgba(255,255,255,0.15);
        color: #FFFFFF;
        border: 2px solid rgba(255,255,255,0.3);
        selection-background-color: rgba(255,255,255,0.3);
    }

    QLineEdit:focus {
        border: 2px solid rgba(255,255,255,0.6);
        background: rgba(255,255,255,0.2);
    }

    QLineEdit::placeholder {
        color: rgba(255,255,255,0.6);
        font-style: italic;
    }

    QPushButton {
        font-size: 16px;
        font-weight: 600;
        padding: 12px 20px;
        border-radius: 15px;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #FF6B6B, stop:0.5 #FF8E53, stop:1 #FF6B6B);
        color: #FFFFFF;
        border: none;
        margin: 5px;
    }

    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #FF8E53, stop:0.5 #FF6B6B, stop:1 #FF8E53);
        transform: translateY(-1px);
    }

    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #E55A5A, stop:0.5 #E57A43, stop:1 #E55A5A);
        padding: 13px 20px 11px 20px;
    }

    QPushButton[text="📜 Show History"] {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #4ECDC4, stop:1 #44A08D);
    }

    QPushButton[text="📜 Show History"]:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #5EDDD4, stop:1 #54B09D);
    }

    QLabel#temp_display {
        font-size: 56px;
        font-weight: 700;
        color: #FFFFFF;
        background: rgba(255,255,255,0.1);
        padding: 20px;
        border-radius: 20px;
        border: 2px solid rgba(255,255,255,0.2);
        margin: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    QLabel#icon_display {
        font-size: 80px;
        font-family: "Segoe UI Emoji", "Apple Color Emoji";
        padding: 10px;
        background: rgba(255,255,255,0.1);
        border-radius: 50%;
        border: 3px solid rgba(255,255,255,0.3);
        margin: 10px;
        min-width: 120px;
        min-height: 120px;
    }

    QLabel#info_display {
        font-size: 20px;
        font-weight: 500;
        color: rgba(255,255,255,0.95);
        background: rgba(255,255,255,0.1);
        padding: 15px 25px;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.2);
        margin: 10px;
        backdrop-filter: blur(5px);
    }

    QVBoxLayout {
        spacing: 15px;
        margin: 20px;
    }

    QHBoxLayout {
        spacing: 10px;
        margin: 0px;
    }

    QScrollBar:vertical {
        background: rgba(255,255,255,0.1);
        width: 15px;
        margin: 0px;
        border-radius: 7px;
    }

    QScrollBar::handle:vertical {
        background: rgba(255,255,255,0.3);
        border-radius: 7px;
        min-height: 20px;
    }

    QScrollBar::handle:vertical:hover {
        background: rgba(255,255,255,0.5);
    }

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        border: none;
        background: none;
    }
    """
)

        self.city_text.setObjectName("city_text")
        self.temp_display.setObjectName("temp_display")
        self.icon_display.setObjectName("icon_display")
        self.info_display.setObjectName("info_display")

        self.check_button.clicked.connect(self.get_weather)
        self.history_button.clicked.connect(self.show_history)

        self.city_input.returnPressed.connect(self.get_weather)

        self.setFixedWidth(400)
        self.setMinimumHeight(480)

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
        history_window = HistoryWindow(self.weather_log, parent=self)
        main_pos = self.geometry()
        history_window.move(main_pos.x() + main_pos.width() + 10, main_pos.y())
        history_window.show()

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