from PyQt5 import QtWidgets, uic, QtGui, QtCore, QtSvg
import numpy
from .wator import WaTor


CELL_SIZE = 32
SVG_WATER = QtSvg.QSvgRenderer('img/water.svg')
SVG_FISH = QtSvg.QSvgRenderer('img/fish.svg')
SVG_SHARK = QtSvg.QSvgRenderer('img/shark.svg')
VALUE_ROLE = QtCore.Qt.UserRole


def pixels_to_logical(x, y):
    return y // CELL_SIZE, x // CELL_SIZE


def logical_to_pixels(row, column):
    return column * CELL_SIZE, row * CELL_SIZE


class GridWidget(QtWidgets.QWidget):
    def __init__(self, array):
        super().__init__()
        self.array = array
        size = logical_to_pixels(*array.shape)
        self.setMinimumSize(*size)
        self.setMaximumSize(*size)
        self.resize(*size)

    def paintEvent(self, event):
        rect = event.rect()

        row_min, col_min = pixels_to_logical(rect.left(), rect.top())
        row_min = max(row_min, 0)
        col_min = max(col_min, 0)
        row_max, col_max = pixels_to_logical(rect.right(), rect.bottom())
        row_max = min(row_max + 1, self.array.shape[0])
        col_max = min(col_max + 1, self.array.shape[1])

        painter = QtGui.QPainter(self)

        for row in range(row_min, row_max):
            for column in range(col_min, col_max):
                x, y = logical_to_pixels(row, column)
                rect = QtCore.QRectF(x, y, CELL_SIZE, CELL_SIZE)

                white = QtGui.QColor(255, 255, 255)
                painter.fillRect(rect, QtGui.QBrush(white))

                SVG_WATER.render(painter, rect)

                if self.array[row, column] > 0:
                    SVG_FISH.render(painter, rect)
                elif self.array[row, column] < 0:
                    SVG_SHARK.render(painter, rect)

    def mousePressEvent(self, event):
        row, column = pixels_to_logical(event.x(), event.y())

        if event.button() == QtCore.Qt.LeftButton and \
                0 <= row < self.array.shape[0] and \
                0 <= column < self.array.shape[1]:
            self.array[row, column] = self.selected
        elif event.button() == QtCore.Qt.RightButton:
            self.array[row, column] = 0

        self.update(*logical_to_pixels(row, column), CELL_SIZE, CELL_SIZE)


def new_dialog(window, grid):
    dialog = QtWidgets.QDialog(window)

    with open('ui/newmaze.ui') as f:
        uic.loadUi(f, dialog)

    result = dialog.exec()

    if result == QtWidgets.QDialog.Rejected:
        return

    cols = dialog.findChild(QtWidgets.QSpinBox, 'widthBox').value()
    rows = dialog.findChild(QtWidgets.QSpinBox, 'heightBox').value()

    grid.array = numpy.zeros((rows, cols), dtype=numpy.int8)

    size = logical_to_pixels(rows, cols)
    grid.setMinimumSize(*size)
    grid.setMaximumSize(*size)
    grid.resize(*size)

    grid.update()


def new_about(window):
    text = ('<h3>Wa-Tor</h3>'
            'Wa-Tor population dynamics simulation.<p>'
            '<p>Version: v0.3<br>'
            'Authors: Ondřej Podsztavek, Miro Hrončok<br>'
            'Repository: <a href="https://github.com/podondra/wator">'
            'https://github.com/podondra/wator</a><br>'
            'Licence: GNU General Public License v3.0<br>'
            'Graphics: <a href="https://opengameart.org/">'
            'OpenGameArt.org</a></p>')
    QtWidgets.QMessageBox.about(window, 'About Wa-Tor', text)


def main():
    app = QtWidgets.QApplication([])

    window = QtWidgets.QMainWindow()
    window.setWindowIcon(QtGui.QIcon('img/shark.svg'))

    with open('ui/mainwindow.ui') as f:
        uic.loadUi(f, window)

    wator = WaTor(shape=(10, 10), nfish=16, nsharks=4)

    scroll_area = window.findChild(QtWidgets.QScrollArea, 'scrollArea')

    grid = GridWidget(wator.creatures)
    scroll_area.setWidget(grid)

    palette = window.findChild(QtWidgets.QListWidget, 'pallete')

    def add_item(name, image, value):
        item = QtWidgets.QListWidgetItem(name)
        icon = QtGui.QIcon(image)
        item.setIcon(icon)
        palette.addItem(item)
        item.setData(VALUE_ROLE, value)

    add_item('water', 'img/water.svg', 0)
    add_item('fish', 'img/fish.svg', 1)
    add_item('shark', 'img/shark.svg', -1)

    def item_activated():
        for item in palette.selectedItems():
            grid.selected = item.data(VALUE_ROLE)

    palette.itemSelectionChanged.connect(item_activated)
    palette.setCurrentRow(1)

    action = window.findChild(QtWidgets.QAction, 'actionNew')
    action.triggered.connect(lambda: new_dialog(window, grid))

    about = window.findChild(QtWidgets.QAction, 'actionAbout')
    about.triggered.connect(lambda: new_about(window))

    window.show()

    return app.exec()
