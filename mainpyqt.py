
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox,
    QListWidget, QMessageBox
)
from library.models import DigitalLibrary, Book, BookNotAvailableError
import sys

class LibraryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Management System - PyQt")
        self.setGeometry(100, 100, 600, 500)

        self.library = DigitalLibrary()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Input fields
        self.title_input = QLineEdit()
        self.author_input = QLineEdit()
        self.isbn_input = QLineEdit()
        self.size_input = QLineEdit()
        self.size_input.setDisabled(True)

        # Labels and layout
        layout.addLayout(self.create_row("Title:", self.title_input))
        layout.addLayout(self.create_row("Author:", self.author_input))
        layout.addLayout(self.create_row("ISBN:", self.isbn_input))

        # Checkbox and size input
        checkbox_layout = QHBoxLayout()
        self.ebook_checkbox = QCheckBox("Is eBook?")
        self.ebook_checkbox.stateChanged.connect(self.toggle_ebook_field)
        checkbox_layout.addWidget(self.ebook_checkbox)
        checkbox_layout.addWidget(QLabel("Size (MB):"))
        checkbox_layout.addWidget(self.size_input)
        layout.addLayout(checkbox_layout)

        # Add Book button
        self.add_button = QPushButton("Add Book")
        self.add_button.clicked.connect(self.add_book)
        layout.addWidget(self.add_button)

        # Book List
        self.book_list = QListWidget()
        layout.addWidget(self.book_list)

        # Lend Button
        self.lend_button = QPushButton("Lend Selected Book")
        self.lend_button.clicked.connect(self.lend_book)
        layout.addWidget(self.lend_button)

        self.setLayout(layout)

    def create_row(self, label_text, widget):
        row = QHBoxLayout()
        row.addWidget(QLabel(label_text))
        row.addWidget(widget)
        return row

    def toggle_ebook_field(self):
        if self.ebook_checkbox.isChecked():
            self.size_input.setDisabled(False)
        else:
            self.size_input.setDisabled(True)
            self.size_input.clear()

    def add_book(self):
        title = self.title_input.text()
        author = self.author_input.text()
        isbn = self.isbn_input.text()
        size = self.size_input.text()

        if not title or not author or not isbn:
            QMessageBox.warning(self, "Input Error", "Please enter title, author and ISBN.")
            return

        if self.ebook_checkbox.isChecked():
            try:
                size_mb = float(size)
                self.library.add_ebook(title, author, isbn, size_mb)
            except ValueError:
                QMessageBox.warning(self, "Input Error", "eBook size must be a number.")
                return
        else:
            self.library.add_book(Book(title, author, isbn))

        QMessageBox.information(self, "Success", "Book added successfully!")
        self.update_book_list()
        self.clear_inputs()

    def clear_inputs(self):
        self.title_input.clear()
        self.author_input.clear()
        self.isbn_input.clear()
        self.size_input.clear()
        self.ebook_checkbox.setChecked(False)

    def update_book_list(self):
        self.book_list.clear()
        for book in self.library:
            self.book_list.addItem(str(book))

    def lend_book(self):
        selected = self.book_list.currentItem()
        if selected:
            text = selected.text()
            isbn = text.split("ISBN: ")[-1].split(")")[0]
            try:
                self.library.lend_book(isbn)
                QMessageBox.information(self, "Success", f"Book lent successfully!")
                self.update_book_list()
            except BookNotAvailableError as e:
                QMessageBox.warning(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Error", "Please select a book to lend.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec_())
