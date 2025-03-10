import sys
from PyQt5 import QtWidgets
from game import Game
from spectator_window import SpectatorWindow
from presenter_window import PresenterWindow
from background_customizer import BackgroundCustomizer


def main():
    app = QtWidgets.QApplication(sys.argv)
    # Initialize the game with songs.txt and players.txt.
    game = Game("songs.txt", "players.txt")

    spectator_win = SpectatorWindow(game)

    # Optionally apply a background customizer to the spectator window.
    # For example, set a background color or provide a path to an image.
    customizer = BackgroundCustomizer(background_image_path=None, background_color=None)
    spectator_win.set_background(customizer)

    presenter_win = PresenterWindow(game, spectator_win)

    spectator_win.show()
    presenter_win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()