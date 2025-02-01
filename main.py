import sys
from PyQt5.QtWidgets import QApplication
from game import Game
from spectator_window import SpectatorWindow
from presenter_window import PresenterWindow


def main():
    app = QApplication(sys.argv)
    # Инициализация игры с файлами songs.txt и players.txt
    game = Game("songs.txt", "players.txt")

    spectator_win = SpectatorWindow(game)
    presenter_win = PresenterWindow(game, spectator_win)

    spectator_win.show()
    presenter_win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
