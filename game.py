
import os
class Game:
    def __init__(self, songs_file, players_file):
        self.songs = []         # Список песен
        self.players = []       # Список игроков
        self.total_scores = {}  # Общие очки для каждой песни
        self.current_scores = {}# Очки текущего цикла для каждой песни
        self.points_sequence = [1, 3, 6, 9]  # Последовательность очков
        self.current_point_index = 0         # Индекс текущего очка в цикле
        self.current_player_index = 0        # Индекс текущего игрока

        self.load_songs(songs_file)
        self.load_players(players_file)

        # Инициализация очков для каждой песни
        for song in self.songs:
            self.total_scores[song] = 0
            self.current_scores[song] = 0

    def load_songs(self, songs_file):
        if os.path.exists(songs_file):
            with open(songs_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            self.songs = [line.strip() for line in lines if line.strip()]
        else:
            self.songs = []

    def load_players(self, players_file):
        if os.path.exists(players_file):
            with open(players_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            self.players = [line.strip() for line in lines if line.strip()]
        else:
            self.players = []

    def get_current_player(self):
        if self.players:
            return self.players[self.current_player_index]
        return None

    def assign_point(self, song_name):
        """Присваивает следующую по очереди оценку выбранной песне."""
        if self.current_point_index < len(self.points_sequence):
            points = self.points_sequence[self.current_point_index]
            self.current_scores[song_name] += points
            self.current_point_index += 1
            return points
        else:
            return None

    def is_turn_complete(self):
        """Проверяет, распределены ли все очки для текущего хода."""
        return self.current_point_index >= len(self.points_sequence)

    def finalize_turn(self):
        """Переносит очки цикла в общие, сбрасывает текущие очки и переходит к следующему игроку."""
        for song in self.songs:
            self.total_scores[song] += self.current_scores[song]
            self.current_scores[song] = 0
        self.current_point_index = 0
        self.current_player_index += 1
        # Если все игроки прошли ход, можно либо завершать игру, либо начать цикл заново.
        if self.current_player_index >= len(self.players):
            self.current_player_index = 0  # Начинаем заново или можно добавить условие завершения игры.
