import sys
import os
import requests
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLineEdit, QLabel, QWidget, QMessageBox

class JSONPlaceholderClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def fetch_data(self, resource):
        url = f"{self.base_url}/{resource}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("JSONPlaceholder Downloader")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.resource_edit = QLineEdit()
        self.layout.addWidget(QLabel("Resource:"))
        self.layout.addWidget(self.resource_edit)

        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.download_data)
        self.layout.addWidget(self.download_button)

    def download_data(self):
        resource = self.resource_edit.text()
        if not resource:
            QMessageBox.warning(self, "Error", "Please enter a resource.")
            return

        client = JSONPlaceholderClient("https://jsonplaceholder.typicode.com")
        data = client.fetch_data(resource)
        if not data:
            QMessageBox.warning(self, "Error", "Failed to fetch data.")
            return

        output_folder = "json_data"
        os.makedirs(output_folder, exist_ok=True)
        filename = f"{resource}.json"
        filepath = os.path.join(output_folder, filename)
        with open(filepath, "w") as f:
            json.dump(data, f)

        QMessageBox.information(self, "Success", f"Data successfully saved to {filepath}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

