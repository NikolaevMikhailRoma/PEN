from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget


class SpectatorWindow(QMainWindow):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.setWindowTitle("Окно для зрителей")
        self.resize(600, 400)
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Общий счет", "Песня", "Текущий счет"])

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.update_table()

    def update_table(self):
        songs = self.game.songs
        self.table.setRowCount(len(songs))
        for index, song in enumerate(songs):
            # Отображение номера песни в скобках перед названием
            song_display = f"({index + 1}) {song}"
            total_score = self.game.total_scores.get(song, 0)
            current_score = self.game.current_scores.get(song, 0)
            self.table.setItem(index, 0, QTableWidgetItem(str(total_score)))
            self.table.setItem(index, 1, QTableWidgetItem(song_display))
            self.table.setItem(index, 2, QTableWidgetItem(str(current_score)))
