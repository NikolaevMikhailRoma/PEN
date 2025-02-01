import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton


class Game:
    def __init__(self, songs_file, players_file):
        self.songs = self.load_songs(songs_file)
        self.players = self.load_players(players_file)
        self.scores = {song: 0 for song in self.songs}
        self.current_scores = {song: 0 for song in self.songs}
        self.player_index = 0
        self.points = [1, 3, 6, 9]
        self.current_point_index = 0

    def load_songs(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]

    def load_players(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]

    def assign_points(self, song):
        if self.current_point_index < len(self.points):
            points = self.points[self.current_point_index]
            self.current_scores[song] = points
            self.current_point_index += 1
            return True
        return False

    def finalize_round(self):
        for song, points in self.current_scores.items():
            self.scores[song] += points
        self.current_scores = {song: 0 for song in self.songs}
        self.current_point_index = 0
        self.player_index = (self.player_index + 1) % len(self.players)


class SpectatorWindow(QWidget):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Voting Table")
        self.layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Total Score", "Song Name", "Current Score"])
        self.layout.addWidget(self.table)

        self.update_table()
        self.setLayout(self.layout)

    def update_table(self):
        self.table.setRowCount(len(self.game.songs))
        sorted_songs = sorted(self.game.songs, key=lambda s: self.game.scores[s], reverse=True)
        for row, song in enumerate(sorted_songs):
            self.table.setItem(row, 0, QTableWidgetItem(str(self.game.scores[song])))
            self.table.setItem(row, 1, QTableWidgetItem(song))
            self.table.setItem(row, 2, QTableWidgetItem(str(self.game.current_scores[song])))
        self.table.resizeColumnsToContents()


class PresenterWindow(QWidget):
    def __init__(self, game, spectator_window):
        super().__init__()
        self.game = game
        self.spectator_window = spectator_window
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Presenter Panel")
        self.layout = QVBoxLayout()

        self.label = QLabel(f"Now voting: {self.game.players[self.game.player_index]}")
        self.layout.addWidget(self.label)

        for song in self.game.songs:
            btn = QPushButton(song)
            btn.clicked.connect(lambda _, s=song: self.assign_points(s))
            self.layout.addWidget(btn)

        self.finalize_btn = QPushButton("Finalize Round")
        self.finalize_btn.clicked.connect(self.finalize_round)
        self.layout.addWidget(self.finalize_btn)

        self.setLayout(self.layout)

    def assign_points(self, song):
        if self.game.assign_points(song):
            self.spectator_window.update_table()

    def finalize_round(self):
        self.game.finalize_round()
        self.spectator_window.update_table()
        self.label.setText(f"Now voting: {self.game.players[self.game.player_index]}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Game("songs.txt", "players.txt")
    spectator_window = SpectatorWindow(game)
    presenter_window = PresenterWindow(game, spectator_window)
    spectator_window.show()
    presenter_window.show()
    sys.exit(app.exec_())
