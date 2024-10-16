import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QMessageBox, QDateEdit, QTimeEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate, QTime
import json  # JSON ile çalışmak için gerekli kütüphane
import os   # Dosya kontrolü için

class TodoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_tasks()  # Uygulama açıldığında görevleri yükle
    
    def initUI(self):
        self.setWindowTitle("Yapılacaklar Listesi")

        # Pencere simgesi ekliyoruz
        self.setWindowIcon(QIcon("todoappicon.png"))

        # Pencere boyutunu 600x800 olarak ayarlıyoruz
        self.setGeometry(300, 300, 600, 800)

        # Ana layout
        layout = QVBoxLayout()

        # Giriş alanı
        self.inputField = QLineEdit(self)
        self.inputField.setPlaceholderText("Görev ekle...")
        layout.addWidget(self.inputField)

        # Tarih seçici
        self.dateEdit = QDateEdit(self)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setDate(QDate.currentDate())
        layout.addWidget(self.dateEdit)

        # Saat seçici
        self.timeEdit = QTimeEdit(self)
        self.timeEdit.setTime(QTime.currentTime())
        layout.addWidget(self.timeEdit)

        # Ekleme butonu
        self.addButton = QPushButton("Ekle", self)
        self.addButton.clicked.connect(self.add_task)
        layout.addWidget(self.addButton)

        # Yapılacaklar listesi
        self.todoList = QListWidget(self)
        layout.addWidget(self.todoList)

        # Silme butonu
        self.deleteButton = QPushButton("Seçili Görevi Sil", self)
        self.deleteButton.clicked.connect(self.delete_task)
        layout.addWidget(self.deleteButton)

        self.setLayout(layout)

    def add_task(self):
        task = self.inputField.text()
        selected_date = self.dateEdit.date().toString("dd/MM/yyyy")  # Tarihi al
        selected_time = self.timeEdit.time().toString("HH:mm")  # Saati al

        if task != "":
            task_with_datetime = f"{task} (Tarih: {selected_date}, Saat: {selected_time})"
            self.todoList.addItem(task_with_datetime)
            self.inputField.setText("")  # Giriş alanını temizle
            self.save_tasks()  # Yeni görev eklenince kaydet
        else:
            QMessageBox.warning(self, "Hata", "Lütfen bir görev girin!")
    
    def delete_task(self):
        selected_task = self.todoList.currentRow()
        if selected_task >= 0:
            self.todoList.takeItem(selected_task)
            self.save_tasks()  # Görev silinince kaydet
        else:
            QMessageBox.warning(self, "Hata", "Silinecek bir görev seçmediniz!")

    def save_tasks(self):
        """Görevleri JSON dosyasına kaydeder."""
        tasks = []
        for i in range(self.todoList.count()):
            tasks.append(self.todoList.item(i).text())

        with open("tasks.json", "w") as file:
            json.dump(tasks, file)

    def load_tasks(self):
        """JSON dosyasından görevleri yükler."""
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as file:
                tasks = json.load(file)
                for task in tasks:
                    self.todoList.addItem(task)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TodoApp()
    window.show()
    sys.exit(app.exec_())
