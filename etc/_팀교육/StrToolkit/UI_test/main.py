import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from design import Ui_MainWindow

class WindLoadCalculator(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.calculate_button.clicked.connect(self.calculate_wind_load)

    def calculate_wind_load(self):
        try:
            height = float(self.height_input.text())
            wind_speed = float(self.wind_speed_input.text())
            exposure_category = self.exposure_category_input.currentText()
            
            # Simplified wind load calculation (example)
            wind_pressure = 0.00256 * (wind_speed ** 2)
            exposure_factor = {"A": 0.8, "B": 1.0, "C": 1.2, "D": 1.6}[exposure_category]
            wind_load = wind_pressure * height * exposure_factor

            self.result_display.setText(f"Calculated Wind Load: {wind_load:.2f} N/m²")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numerical values.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WindLoadCalculator()
    window.show()
    sys.exit(app.exec_())
