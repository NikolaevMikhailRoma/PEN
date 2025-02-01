I need to create python project with pyqt for interactive voting task.
Repo has two files seongs.txt and players.txt files with 'new line' separator.

The first window contains a table with song names in the order specified in the text file, the song number is added in brackets before the song name. There are three columns: total score, song name and current score.

The second window is created for the presenter.

Points 1, 3, 6, 9 are selected sequentially.

The game process is as follows: a cycle starts. A player is selected in order. Next score on the list, the host chooses the name of the song and assigns it the current score, during this the first window is updated and in the column with the current score is added the current number of points, until all the points will not be distributed, it should be reflected in the table with the current score, after this cycle points go to the total number of points, the table in the first window is sorted and begins the turn for another player. At the end everything just stops until the presenter closes the window.

There should be three classes. The game class itself and two window classes, one for the spectator and one for the presenter. The presenter will drag their own window to another location.
