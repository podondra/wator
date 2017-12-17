import numpy
from PyQt5 import QtWidgets, uic, QtGui, QtCore, QtSvg
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


class WaTorWidget(QtWidgets.QWidget):
    def __init__(self, wator):
        super().__init__()
        self.wator = wator
        size = logical_to_pixels(*wator.creatures.shape)
        self.setMinimumSize(*size)
        self.setMaximumSize(*size)
        self.resize(*size)

    def paintEvent(self, event):
        rect = event.rect()

        row_min, col_min = pixels_to_logical(rect.left(), rect.top())
        row_min = max(row_min, 0)
        col_min = max(col_min, 0)
        row_max, col_max = pixels_to_logical(rect.right(), rect.bottom())
        row_max = min(row_max + 1, self.wator.creatures.shape[0])
        col_max = min(col_max + 1, self.wator.creatures.shape[1])

        painter = QtGui.QPainter(self)

        for row in range(row_min, row_max):
            for column in range(col_min, col_max):
                x, y = logical_to_pixels(row, column)
                rect = QtCore.QRectF(x, y, CELL_SIZE, CELL_SIZE)

                white = QtGui.QColor(255, 255, 255)
                painter.fillRect(rect, QtGui.QBrush(white))

                SVG_WATER.render(painter, rect)

                if self.wator.creatures[row, column] > 0:
                    SVG_FISH.render(painter, rect)
                elif self.wator.creatures[row, column] < 0:
                    SVG_SHARK.render(painter, rect)

    def mousePressEvent(self, event):
        row, column = pixels_to_logical(event.x(), event.y())

        if event.button() == QtCore.Qt.LeftButton and \
                0 <= row < self.wator.creatures.shape[0] and \
                0 <= column < self.wator.creatures.shape[1]:
            if self.selected == 1:
                self.wator.creatures[row, column] = numpy.random.randint(
                        1, self.wator.age_fish
                        )
            elif self.selected == -1:
                self.wator.creatures[row, column] = numpy.random.randint(
                        self.wator.age_shark, -1
                        )
                self.wator.energies[row, column] = self.wator.energy_initial
            else:
                self.wator.creatures[row, column] = 0
        elif event.button() == QtCore.Qt.RightButton:
            self.wator.creatures[row, column] = 0

        self.update(*logical_to_pixels(row, column), CELL_SIZE, CELL_SIZE)


def new_dialog(window, grid):
    dialog = QtWidgets.QDialog(window)

    with open('ui/newmaze.ui') as f:
        uic.loadUi(f, dialog)

    result = dialog.exec()

    if result == QtWidgets.QDialog.Rejected:
        return

    rows = dialog.findChild(QtWidgets.QSpinBox, 'heightBox').value()
    cols = dialog.findChild(QtWidgets.QSpinBox, 'widthBox').value()

    wator = WaTor(shape=(rows, cols), nfish=0, nsharks=0)
    grid.wator = wator

    size = logical_to_pixels(rows, cols)
    grid.setMinimumSize(*size)
    grid.setMaximumSize(*size)
    grid.resize(*size)

    grid.update()


def next_chronon(grid):
    grid.wator.tick()
    grid.update()


def about_dialog(window):
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


def open_wator(window, grid):
    filename = QtWidgets.QFileDialog.getOpenFileName(window, 'Open File')[0]
    try:
        creatures = numpy.loadtxt(filename, dtype=numpy.int8)
    except ValueError as e:
        text = 'Please select file <code>numpy.savetxt</code> format.'
        QtWidgets.QMessageBox.critical(window, 'Invalid File', text)
        return
    except FileNotFoundError:
        return

    grid.wator = WaTor(creatures=creatures)
    grid.update()


def save_wator(window, grid):
    filename = QtWidgets.QFileDialog.getSaveFileName(window, 'Save File')[0]
    if filename != '':
        numpy.savetxt(filename, grid.wator.creatures)


def params_dialog(window, grid):
    dialog = QtWidgets.QDialog(window)

    with open('ui/params.ui') as f:
        uic.loadUi(f, dialog)

    values = [grid.wator.age_fish, -grid.wator.age_shark,
              grid.wator.energy_initial, grid.wator.energy_eat]
    boxes = ['ageFishBox', 'ageSharkBox', 'energyInitialBox', 'energyEatBox']
    for value, box in zip(values, boxes):
        window.findChild(QtWidgets.QSpinBox, box).setValue(value)

    result = dialog.exec()

    if result == QtWidgets.QDialog.Rejected:
        return

    grid.wator.age_fish = dialog.findChild(QtWidgets.QSpinBox,
                                           'ageFishBox').value()
    grid.wator.age_shark = -dialog.findChild(QtWidgets.QSpinBox,
                                             'ageSharkBox').value()
    grid.wator.energy_initial = dialog.findChild(QtWidgets.QSpinBox,
                                                 'energyInitialBox').value()
    grid.wator.energy_eat = dialog.findChild(QtWidgets.QSpinBox,
                                             'energyEatBox').value()


def main():
    app = QtWidgets.QApplication([])

    window = QtWidgets.QMainWindow()
    window.setWindowIcon(QtGui.QIcon('img/shark.svg'))

    with open('ui/mainwindow.ui') as f:
        uic.loadUi(f, window)

    scroll_area = window.findChild(QtWidgets.QScrollArea, 'scrollArea')

    wator = WaTor(shape=(10, 10), nfish=16, nsharks=4)
    grid = WaTorWidget(wator)
    scroll_area.setWidget(grid)

    palette = window.findChild(QtWidgets.QListWidget, 'palette')

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

    action_new = window.findChild(QtWidgets.QAction, 'actionNew')
    action_new.triggered.connect(lambda: new_dialog(window, grid))

    action_about = window.findChild(QtWidgets.QAction, 'actionAbout')
    action_about.triggered.connect(lambda: about_dialog(window))

    action_next_chronon = window.findChild(QtWidgets.QAction,
                                           'actionNextChronon')
    action_next_chronon.triggered.connect(lambda: next_chronon(grid))

    action_open = window.findChild(QtWidgets.QAction, 'actionOpen')
    action_open.triggered.connect(lambda: open_wator(window, grid))

    action_save = window.findChild(QtWidgets.QAction, 'actionSave')
    action_save.triggered.connect(lambda: save_wator(window, grid))

    action_parameters = window.findChild(QtWidgets.QAction, 'actionParams')
    action_parameters.triggered.connect(lambda: params_dialog(window, grid))

    window.show()

    return app.exec()
