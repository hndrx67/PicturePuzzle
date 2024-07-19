
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QSpinBox, QGraphicsItem, QGraphicsRectItem, QCheckBox, QHBoxLayout, QGraphicsRectItem, QGraphicsSimpleTextItem, QSplashScreen  
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QFont
from PyQt5.QtCore import Qt, QRectF, QPointF, QSize, QTimer, QCoreApplication, QUrl, QPropertyAnimation, QEasingCurve
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import random
import os





'''
absolute file path 
'''
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

class OpeningWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Title Window")
        self.setGeometry(0, 0, 300, 300)
        self.center_on_screen()

        self.setWindowFlag(Qt.FramelessWindowHint)
        #self.setAttribute(Qt.WA_TranslucentBackground)

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 300, 300)
        pixmap = QPixmap (os.path.join(script_dir,"PyPicturePuzzle Startup screen v1.jpg"))  
        pixmap = pixmap.scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(pixmap)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.start_fade_out)
        self.timer.start(4000) 

        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(os.path.join(script_dir, "arara.mp3"))))  
        self.mediaPlayer.play()
        self.mediaPlayer.setVolume(40)
        
    def center_on_screen(self):
        screen_geometry = QCoreApplication.instance().desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def start_fade_out(self):
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.finished.connect(self.close)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setDuration(2000)  
        self.animation.setEasingCurve(QEasingCurve.OutQuad)
        self.animation.start()











class LabeledPixmapItem(QGraphicsPixmapItem):
    def __init__(self, pixmap, label, show_border=True):
        super().__init__(pixmap)
        self.label = label
        self.snapped = False
        self.show_border = show_border

    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)
        if self.show_border:
            pen = QPen(Qt.black)
            pen.setWidth(1)
            painter.setPen(pen)
            painter.drawRect(self.boundingRect())

class ImagePuzzle(QWidget):
    def __init__(self):
        super().__init__()

        self.image_path = None
        self.puzzle_size = 4
        self.original_size = None
        self.scrambled = False
        self.show_border = True
        self.pan_mode = False  

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Puzzler v23.69 BETA TEST')
        self.setGeometry(0, 0, 1000, 600)
        self.center_on_screen2()

        layout = QVBoxLayout(self)

        browse_button = QPushButton('Browse Pictures', self)
        browse_button.setFixedSize(100, 30)
        browse_button.clicked.connect(self.browseImage)

        self.puzzle_size_label = QLabel('Puzzle Size:', self)

        self.puzzle_size_spinbox = QSpinBox(self)
        self.puzzle_size_spinbox.setFixedSize(50, 25)
        self.puzzle_size_spinbox.setMinimum(2)
        self.puzzle_size_spinbox.setMaximum(10)
        self.puzzle_size_spinbox.setValue(self.puzzle_size)
        self.puzzle_size_spinbox.valueChanged.connect(self.updatePuzzleSize)

        self.border_toggle = QCheckBox('Border', self)
        self.border_toggle.setChecked(True)
        self.border_toggle.stateChanged.connect(self.toggleBorder)

        self.pan_button = QPushButton('Pan', self) 
        self.pan_button.setFixedSize(80, 30)
        self.pan_button.setCheckable(True)
        self.pan_button.clicked.connect(self.togglePanMode)

        self.scramble_button = QPushButton('Scramble', self)
        self.scramble_button.setFixedSize(80, 30)
        self.scramble_button.clicked.connect(self.scrambleImage)

        self.clear_button = QPushButton('Clear', self)
        self.clear_button.setFixedSize(80, 30)
        self.clear_button.clicked.connect(self.clearImage)
        self.clear_button.setEnabled(False)

        self.refresh_button = QPushButton('Refresh', self)
        self.refresh_button.setFixedSize(80, 30)
        self.refresh_button.clicked.connect(self.refreshWindow)
        self.refresh_button.setEnabled(False)

        self.zoom_in_button = QPushButton('Zoom In', self)
        self.zoom_in_button.setFixedSize(80, 30)
        self.zoom_in_button.clicked.connect(lambda: self.zoom(1.2))

        self.zoom_out_button = QPushButton('Zoom Out', self)
        self.zoom_out_button.setFixedSize(80, 30)
        self.zoom_out_button.clicked.connect(lambda: self.zoom(0.8))

        self.randomize_button = QPushButton('Randomize', self)
        self.randomize_button.setFixedSize(80, 30)
        self.randomize_button.clicked.connect(self.randomizePieces)

        button_layout = QHBoxLayout()
        button_layout.addWidget(browse_button)
        button_layout.addWidget(self.puzzle_size_label)
        button_layout.addWidget(self.puzzle_size_spinbox)
        button_layout.addWidget(self.border_toggle)
        button_layout.addWidget(self.pan_button)
        button_layout.addWidget(self.scramble_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.zoom_in_button)
        button_layout.addWidget(self.zoom_out_button)
        button_layout.addWidget(self.randomize_button) 
        button_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        layout.addLayout(button_layout)

        image_container = QWidget(self)
        image_container_layout = QVBoxLayout(image_container)

        self.view = QGraphicsView(self)
        image_container_layout.addWidget(self.view)

        layout.addWidget(image_container)

        self.setLayout(layout)
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)
        self.selected_piece = None
        
    def center_on_screen2(self):
        screen_geometry = QCoreApplication.instance().desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def togglePanMode(self):
        self.pan_mode = not self.pan_mode
        self.view.setDragMode(QGraphicsView.ScrollHandDrag if self.pan_mode else QGraphicsView.NoDrag)

    def browseImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        filePath, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (.png *.jpg *.bmp);;All Files ()", options=options)

        if filePath:
            self.image_path = filePath
            self.loadImage()
            self.scrambled = False
            self.scramble_button.setEnabled(True)
            self.clear_button.setEnabled(False)
            self.refresh_button.setEnabled(False)

    def loadImage(self):
        if not self.image_path:
            return

        self.scene.clear()

        pixmap = QPixmap(self.image_path)
        original_image = QImage(self.image_path)

        screen_size = self.view.size()
        scaled_pixmap = pixmap.scaled(screen_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        item = QGraphicsPixmapItem(scaled_pixmap)

        self.original_size = original_image.size()
        self.scene.setSceneRect(0, 0, scaled_pixmap.width(), scaled_pixmap.height())

        self.scene.addItem(item)

    def updatePuzzleSize(self):
        self.puzzle_size = self.puzzle_size_spinbox.value()

    def scrambleImage(self):
        if not self.image_path or self.scrambled:
            return

        original_pixmap = self.scene.items()[0].pixmap()
        piece_width = original_pixmap.width() // self.puzzle_size
        piece_height = original_pixmap.height() // self.puzzle_size

        self.scene.clear()

        puzzle_pieces = []
        labels = list(range(1, self.puzzle_size ** 2 + 1))

        for row in range(self.puzzle_size):
            for col in range(self.puzzle_size):
                label = labels.pop(0)
                rect = QRectF(col * piece_width, row * piece_height, piece_width, piece_height)
                piece_pixmap = original_pixmap.copy(rect.toRect())
                piece_item = LabeledPixmapItem(piece_pixmap, label, self.show_border)
                puzzle_pieces.append(piece_item)

        while not self.isSolvable(puzzle_pieces):
            random.shuffle(puzzle_pieces)

        for i, piece_item in enumerate(puzzle_pieces):
            col_pos = i % self.puzzle_size
            row_pos = i // self.puzzle_size
            x_pos = col_pos * piece_width
            y_pos = row_pos * piece_height
            piece_item.setPos(QPointF(x_pos, y_pos))

        self.connectPieces(puzzle_pieces)

        for piece_item in puzzle_pieces:
            self.scene.addItem(piece_item)

        for item in self.scene.items():
            item.setFlag(QGraphicsPixmapItem.ItemIsMovable)

        self.scrambled = True
        self.scramble_button.setEnabled(False)
        self.clear_button.setEnabled(True)
        self.refresh_button.setEnabled(True)

    def randomizePieces(self):
        if not self.scrambled:
            return

        puzzle_pieces = [item for item in self.scene.items() if isinstance(item, LabeledPixmapItem)]

        while not self.isSolvable(puzzle_pieces):
            random.shuffle(puzzle_pieces)

        for i, piece_item in enumerate(puzzle_pieces):
            col_pos = i % self.puzzle_size
            row_pos = i // self.puzzle_size
            x_pos = col_pos * piece_item.pixmap().width()
            y_pos = row_pos * piece_item.pixmap().height()
            piece_item.setPos(QPointF(x_pos, y_pos))
            piece_item.snapped = False  
            piece_item.setFlag(QGraphicsPixmapItem.ItemIsMovable)  

        self.connectPieces(puzzle_pieces)

    def clearImage(self):
        self.scene.clear()
        self.image_path = None
        self.scrambled = False
        self.scramble_button.setEnabled(True)
        self.clear_button.setEnabled(False)
        self.refresh_button.setEnabled(False)

    def connectPieces(self, puzzle_pieces):
        for piece1, piece2 in zip(puzzle_pieces, puzzle_pieces[1:]):
            self.connectPuzzlePieces(piece1, piece2)
            piece1.setFlag(QGraphicsPixmapItem.ItemIsMovable, True)  

    def connectPuzzlePieces(self, piece1, piece2):
        piece1.setFlag(QGraphicsPixmapItem.ItemIsMovable, False)
        piece2.setFlag(QGraphicsPixmapItem.ItemIsMovable, False)
        self.checkSnapConditions(piece1, piece2)

    def checkSnapConditions(self, piece1, piece2):
        if not piece1.snapped and not piece2.snapped and self.areEdgesAligned(piece1, piece2):
            self.snapPieces(piece1, piece2)
            piece1.setFlag(QGraphicsPixmapItem.ItemIsMovable, True)  
            piece2.setFlag(QGraphicsPixmapItem.ItemIsMovable, True)  

    def areEdgesAligned(self, piece1, piece2):
        tolerance = 5

        rect1 = piece1.sceneBoundingRect()
        rect2 = piece2.sceneBoundingRect()

        if abs(rect1.right() - rect2.left()) < tolerance:
            return True

        if abs(rect1.left() - rect2.right()) < tolerance:
            return True

        if abs(rect1.bottom() - rect2.top()) < tolerance:
            return True

        if abs(rect1.top() - rect2.bottom()) < tolerance:
            return True

        return False

    def snapPieces(self, piece1, piece2):
        rect1 = piece1.sceneBoundingRect()
        rect2 = piece2.sceneBoundingRect()

        if abs(rect1.right() - rect2.left()) < abs(rect1.left() - rect2.right()):
            offset = QPointF(rect2.left() - rect1.right(), 0)
        else:
            offset = QPointF(rect2.right() - rect1.left(), 0)

        piece1.setPos(piece1.pos() + offset)

        if abs(rect1.bottom() - rect2.top()) < abs(rect1.top() - rect2.bottom()):
            offset = QPointF(0, rect2.top() - rect1.bottom())
        else:
            offset = QPointF(0, rect2.bottom() - rect1.top())

        piece1.setPos(piece1.pos() + offset)

        piece1.snapped = True
        piece2.snapped = True

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def mousePressEvent(self, event):
        if self.scrambled and not self.pan_mode:
            item = self.view.itemAt(event.pos())

            if item and isinstance(item, LabeledPixmapItem):
                self.selected_piece = item

    def mouseReleaseEvent(self, event):
        if self.selected_piece and self.scrambled and not self.pan_mode:
            item = self.view.itemAt(event.pos())

            if item and isinstance(item, LabeledPixmapItem) and item != self.selected_piece:
                self.selected_piece.setPos(item.pos())
                item.setPos(self.selected_piece.pos())
                self.selected_piece.snapped, item.snapped = item.snapped, self.selected_piece.snapped
                self.selected_piece = None

    def toggleBorder(self, state):
        self.show_border = state
        self.refreshWindow()

    def isSolvable(self, puzzle_pieces):
        inversions = 0
        for i in range(len(puzzle_pieces)):
            for j in range(i + 1, len(puzzle_pieces)):
                if puzzle_pieces[i].label > puzzle_pieces[j].label and puzzle_pieces[i].label != self.puzzle_size ** 2 and puzzle_pieces[j].label != self.puzzle_size ** 2:
                    inversions += 1

        if self.puzzle_size % 2 == 1:
            return inversions % 2 == 0
        else:
            empty_row = len(puzzle_pieces) // self.puzzle_size
            empty_row_from_bottom = self.puzzle_size - empty_row
            return (inversions % 2 == 0 and empty_row_from_bottom % 2 == 1) or (inversions % 2 == 1 and empty_row_from_bottom % 2 == 0)

    def zoom(self, factor):
        self.view.setTransform(self.view.transform().scale(factor, factor))

    def refreshWindow(self):
        self.scene.clear()
        self.image_path = None
        self.scrambled = False
        self.scramble_button.setEnabled(True)
        self.clear_button.setEnabled(False)
        self.refresh_button.setEnabled(False)
        self.loadImage()
        
        
        
def show_puzzle(opening_window, timer):
    opening_window.hide()
    puzzle = ImagePuzzle()
    puzzle.show()
    timer.disconnect()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    opening_window = OpeningWindow()
    opening_window.show()

    #
    timer = QTimer()
    timer.timeout.connect(lambda: show_puzzle(opening_window, timer))
    timer.start(5000) 

    sys.exit(app.exec_())
    
   
        
        
'''
def show_puzzle(opening_window):
    opening_window.hide()
    puzzle = ImagePuzzle()
    puzzle.show()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    opening_window = OpeningWindow()
    opening_window.show()

    # Create a QTimer to delay showing the second window
    timer = QTimer()
    timer.timeout.connect(lambda: show_puzzle(opening_window))
    timer.start(2000)  # 2000 milliseconds = 2 seconds

    sys.exit(app.exec_())

def show_puzzle(opening_window):
    opening_window.hide()
    puzzle = ImagePuzzle()
    puzzle.show()
'''



'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    opening_window = OpeningWindow()
    opening_window.show()
    puzzle = ImagePuzzle()
    puzzle.show()
    sys.exit(app.exec_())
'''
