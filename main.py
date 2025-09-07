import sys

from PyQt5.QtWidgets import QApplication

from fly_time import FloatingShapesWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        widget = FloatingShapesWidget()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)