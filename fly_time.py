import math
import random

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QWidget


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class BaseObject:
    size = 10
    x = 0
    y = 0
    rotate = 0


class AnimationObject(BaseObject):
    min = Point(0, 0)
    max = Point(0, 0)

    start = Point(0, 0)
    target = Point(0, 0)
    pathTime = 0
    awaitTime = 0
    reserved = False
    dx = 0
    dy = 0

    def move(self,
             target: Point | None = None,
             path_time: int | None = None,
             await_time: int | None = None,
             accuracy: int = 1) -> None:
        self.target = target if target is not None else self.get_random_target()
        self.rotate = self.calculate_angle(self.start, self.target)
        self.pathTime = path_time if path_time else random.randint(100, 1000)
        self.awaitTime = await_time if await_time else random.randint(500, 1000)
        self.dx = (self.target.x - self.start.x) / self.pathTime + 2 * (1 - accuracy)
        self.dy = (self.target.y - self.start.y) / self.pathTime + 2 * (1 - accuracy)
        self.reserved = True

    def update(self):
        if self.pathTime > 0 and self.reserved:
            self.x += self.dx
            self.y += self.dy
            self.pathTime -= 1

    def get_random_target(self):
        return Point(random.randint(self.min.x, self.max.x), random.randint(self.min.y, self.max.y))

    @staticmethod
    def calculate_angle(start: Point, target: Point) -> float:
        dx = target.x - start.x
        dy = target.y - start.y

        angle_rad = math.atan2(dy, dx)

        return angle_rad


class Fly(AnimationObject):
    def __init__(self, width: int, height: int):
        pixmap = QPixmap('fly.png')
        pixmap = pixmap.scaled(20,
                               20,
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        self.pixmap = pixmap
        self.min = Point(0, 0)
        self.max = Point(width, height)


class FloatingShapesWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Настройка прозрачного полноэкранного окна
        self.setWindowFlags(Qt.WindowStaysOnTopHint |
                            Qt.FramelessWindowHint |
                            Qt.Tool
                            )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground)

        # Инициализация перед показом
        self.flies = []
        self.init_flies()

        # Таймер для анимации
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_shapes)
        self.timer.start(20)  # ~33 FPS

        self.showFullScreen()

    def init_flies(self):
        for _ in range(10):
            fly = Fly(self.width(), self.height())
            fly.move()
            self.flies.append(fly)

    def animate_shapes(self):
        """Обновление позиций фигур"""
        if not self.isVisible():
            return

        for fly in self.flies:
            fly.update()

        self.update()

    def paintEvent(self, event):
        """Отрисовка фигур"""
        if not self.isVisible():
            return

        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)

            for fly in self.flies:
                x, y, rotate = fly.x, fly.y, fly.rotate
                pixmap = fly.pixmap

                painter.save()
                painter.translate(x, y)
                painter.rotate(rotate)

                painter.drawPixmap(
                    -pixmap.width() // 2,
                    -pixmap.height() // 2,
                    pixmap
                )

                painter.restore()

        finally:
            painter.end()

    # Переопределяем методы для пропуска событий
    def mousePressEvent(self, event):
        event.ignore()

    def mouseReleaseEvent(self, event):
        event.ignore()

    def mouseDoubleClickEvent(self, event):
        event.ignore()

    def mouseMoveEvent(self, event):
        event.ignore()

    def keyPressEvent(self, event):
        event.ignore()

    def keyReleaseEvent(self, event):
        event.ignore()
