import sys
import os
import importlib
from PyQt5 import QtWidgets

# Add the parent directory to sys.path so that Python can find 'api'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Dynamically import ProxyManager and BotLogic using importlib
try:
    proxy_manager_module = importlib.import_module('api.proxy_manager')
    bot_logic_module = importlib.import_module('api.bot_logic')

    # Access the classes from the imported modules
    ProxyManager = getattr(proxy_manager_module, 'ProxyManager', None)
    BotLogic = getattr(bot_logic_module, 'BotLogic', None)

    if ProxyManager is None or BotLogic is None:
        raise ImportError("Could not find ProxyManager or BotLogic classes. Please check their definitions.")
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

class MainUI(QtWidgets.QWidget):
    def __init__(self, driver_path, proxy_file_path):
        super().__init__()
        self.driver_path = driver_path
        self.proxy_manager = ProxyManager(proxy_file_path)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Viewership Bot')

        # Widgets for input
        self.url_label = QtWidgets.QLabel('Target URL:')
        self.url_input = QtWidgets.QLineEdit(self)
        self.tabs_label = QtWidgets.QLabel('Number of Tabs:')
        self.tabs_input = QtWidgets.QSpinBox(self)
        self.tabs_input.setRange(1, 50)
        self.start_button = QtWidgets.QPushButton('Start Bot', self)

        # Layout setup
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.tabs_label)
        layout.addWidget(self.tabs_input)
        layout.addWidget(self.start_button)
        self.setLayout(layout)

        # Button click event
        self.start_button.clicked.connect(self.start_bot)

    def start_bot(self):
        url = self.url_input.text()
        num_tabs = self.tabs_input.value()
        if url:
            bot_logic = BotLogic(self.proxy_manager, self.driver_path)
            for _ in range(num_tabs):
                bot_logic.start_browser_with_proxy(url)
        else:
            QtWidgets.QMessageBox.warning(self, 'Input Error', 'Please enter a valid URL.')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    driver_path = "chromedriver"  # Update this with the actual path to your driver
    proxy_file_path = "config/proxies.txt"
    ui = MainUI(driver_path, proxy_file_path)
    ui.show()
    sys.exit(app.exec_())
