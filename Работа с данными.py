import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QTextEdit, QPushButton, 
                             QMessageBox, QGroupBox, QListWidget, QListWidgetItem,
                             QSplitter)
from PyQt5.QtCore import Qt

DATA_FILE = "user_data.json"

class DataAppWithList(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_data_list()
        
    def initUI(self):
        self.setWindowTitle("Работа с данными - выбор записи из списка")
        self.setGeometry(300, 300, 800, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        left_label = QLabel("Сохранённые записи:")
        self.records_list = QListWidget()
        self.records_list.itemClicked.connect(self.on_item_clicked)
        
        left_layout.addWidget(left_label)
        left_layout.addWidget(self.records_list)
        
        button_layout = QHBoxLayout()
        self.load_selected_btn = QPushButton("Загрузить выбранное")
        self.load_selected_btn.clicked.connect(self.load_selected_record)
        
        self.refresh_btn = QPushButton("Обновить список")
        self.refresh_btn.clicked.connect(self.load_data_list)
        
        button_layout.addWidget(self.load_selected_btn)
        button_layout.addWidget(self.refresh_btn)
        left_layout.addLayout(button_layout)
        
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        input_group = QGroupBox("Ввод новых данных")
        input_layout = QVBoxLayout()
        
        self.input_edit = QTextEdit()
        self.input_edit.setPlaceholderText("Введите новые данные здесь...")
        self.input_edit.setMaximumHeight(150)
        
        input_layout.addWidget(self.input_edit)
        input_group.setLayout(input_layout)
        
        save_layout = QHBoxLayout()
        self.save_btn = QPushButton("Сохранить как новую запись")
        self.save_btn.clicked.connect(self.save_new_record)
        
        save_layout.addWidget(self.save_btn)
    
        display_group = QGroupBox("Загруженные данные")
        display_layout = QVBoxLayout()
        
        self.display_text = QTextEdit()
        self.display_text.setReadOnly(True)
        self.display_text.setMaximumHeight(150)
        
        display_layout.addWidget(self.display_text)
        display_group.setLayout(display_layout)
        
        control_layout = QHBoxLayout()
        self.clear_btn = QPushButton("Очистить поля")
        self.clear_btn.clicked.connect(self.clear_fields)
        
        control_layout.addWidget(self.clear_btn)
        
        self.status_label = QLabel("Статус: Готов")
        
        right_layout.addWidget(input_group)
        right_layout.addLayout(save_layout)
        right_layout.addWidget(display_group)
        right_layout.addLayout(control_layout)
        right_layout.addWidget(self.status_label)
        
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 1)
        
        self.current_data = ""
        self.all_data_list = []
        
    def load_data_list(self):
        self.all_data_list = self.read_from_file()
        self.records_list.clear()
        
        for i, record in enumerate(self.all_data_list, 1):
            preview = record[:80] + "..." if len(record) > 80 else record
            self.records_list.addItem(f"{i}. {preview}")
        
        self.status_label.setText(f"Статус: Загружено {len(self.all_data_list)} записей")
    
    def read_from_file(self):
        if not os.path.exists(DATA_FILE):
            return []
        
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def save_to_file(self, data):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    def save_new_record(self):
        new_data = self.input_edit.toPlainText().strip()
        
        if not new_data:
            QMessageBox.warning(self, "Предупреждение", "Введите данные для сохранения")
            return
        
        self.all_data_list.append(new_data)
        self.save_to_file(self.all_data_list)
        self.current_data = new_data
        self.display_text.setText(self.current_data)
        self.load_data_list()
        self.input_edit.clear()
        
        self.status_label.setText(f"Статус: Данные сохранены")
        QMessageBox.information(self, "Успех", "Данные успешно сохранены")
    
    def on_item_clicked(self, item):
        index = self.records_list.row(item)
        if index < len(self.all_data_list):
            self.current_data = self.all_data_list[index]
            self.display_text.setText(self.current_data)
            self.status_label.setText(f"Статус: Выбрана запись #{index + 1}")
    
    def load_selected_record(self):
        if self.current_data:
            self.input_edit.setText(self.current_data)
            self.status_label.setText(f"Статус: Запись загружена в редактор")
            QMessageBox.information(self, "Загрузка", "Выбранная запись загружена в поле ввода")
        else:
            QMessageBox.warning(self, "Предупреждение", "Сначала выберите запись из списка")
    
    def clear_fields(self):
        self.input_clear_btn = QMessageBox.question(self, "Подтверждение", 
                                    "Очистить все поля?",
                                    QMessageBox.Yes | QMessageBox.No)
        
        if self.input_clear_btn == QMessageBox.Yes:
            self.input_edit.clear()
            self.display_text.clear()
            self.current_data = ""
            self.status_label.setText("Статус: Поля очищены")


def main():
    app = QApplication(sys.argv)
    window = DataAppWithList()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
