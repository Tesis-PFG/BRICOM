import sys
from PyQt5.QtWidgets import QApplication 
from app import MainWindow

def main():
    """Main function for the application."""

    # Create the application
    app = QApplication(sys.argv)
    
    # Create and show the main window
    window = MainWindow()
    window.show()

    # Start the event loop
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()