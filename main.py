# main.py

from ui.main_ui import MainUI
import sys
from PyQt5 import QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    driver_path = "drivers/chromedriver"  # Path to ChromeDriver
    proxy_file_path = "config/proxies.txt"
    main_ui = MainUI(driver_path, proxy_file_path)
    main_ui.show()
    sys.exit(app.exec_())
