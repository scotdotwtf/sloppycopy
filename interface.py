import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextOption, QPixmap, QIcon
import sloppycopy

class ConsoleOutput:
    def __init__(self, console_widget):
        self.console_widget = console_widget
    def write(self, message):
        self.console_widget.append(message.strip())
    def flush(self):
        pass

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SLOPPYCOPY")

        if sys.platform == "win32":
            self.setWindowIcon(QIcon("Interface/Icon.ico"))
        else:
            self.setWindowIcon(QIcon("Interface/Icon.png"))

        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap("Interface/Logo.png"))
        self.logo.setAlignment(Qt.AlignCenter)

        self.source_label = QLabel("Source", self)

        self.source_button = QPushButton("Browse", self)
        self.source_button.clicked.connect(lambda: self.browse_directory("source"))

        self.source_path = QLineEdit(self)
        self.source_path.setReadOnly(True)

        source_layout = QHBoxLayout()
        source_layout.addWidget(self.source_button)
        source_layout.addWidget(self.source_path)

        self.target_label = QLabel("Target", self)

        self.target_button = QPushButton("Browse", self)
        self.target_button.clicked.connect(lambda: self.browse_directory("target"))

        self.target_path = QLineEdit(self)
        self.target_path.setReadOnly(True)
        
        target_layout = QHBoxLayout()
        target_layout.addWidget(self.target_button)
        target_layout.addWidget(self.target_path)

        self.copy_button = QPushButton("Copy", self)
        self.copy_button.clicked.connect(self.copy_files)

        self.console_label = QLabel("Output", self)

        self.console = QTextEdit(self)
        self.console.setReadOnly(True)
        self.console.setMinimumHeight(200)
        self.console.setWordWrapMode(QTextOption.NoWrap)
        self.console.setStyleSheet("line-height: 1.2;")

        sys.stdout = ConsoleOutput(self.console)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.logo)
        main_layout.addWidget(self.source_label)
        main_layout.addLayout(source_layout)
        main_layout.addWidget(self.target_label)
        main_layout.addLayout(target_layout)
        main_layout.addWidget(self.copy_button)
        main_layout.addWidget(self.console_label)
        main_layout.addWidget(self.console)
        self.setLayout(main_layout)

    def browse_directory(self, directory_type):
        directory = QFileDialog.getExistingDirectory(self, f"Select {directory_type} directory")
        if directory:
            getattr(self, f"{directory_type}_path").setText(directory)

    def copy_files(self):
        source = self.source_path.text()
        target = self.target_path.text()

        if not source or not target:
            QMessageBox.warning(self, "Error", "Please select both source and target directories.")
            return
        else:
            try:
                sloppycopy.copy(source, target)
                print(f"Copying done, total changes: {sloppycopy.total_changes}")
                QMessageBox.information(self, "Copied", f"Copying done, total changes: {sloppycopy.total_changes}")
            except Exception as e:
                print(f"Error", f"Error occured. Please make github issue at https://github.com/scotdotwtf/sloppycopy/issues/new/choose and paste this: \n{e}")
                QMessageBox.critical(self, "Error", "Oh nose! looks like an error occuried. Please check the output.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())