I need to create python project with pyqt for interactive voting task.
Repo has two files seongs.txt and players.txt files with 'new line' separator.

The first window contains a table with song names in the order specified in the text file, the song number is added in brackets before the song name. There are three columns: total score, song name and current score.

The second window is created for the presenter.

Points 1, 3, 6, 9 are selected sequentially.

The game process is as follows: a cycle starts. A player is selected in order. Next score on the list, the host chooses the name of the song and assigns it the current score, during this the first window is updated and in the column with the current score is added the current number of points, until all the points will not be distributed, it should be reflected in the table with the current score, after this cycle points go to the total number of points, the table in the first window is sorted and begins the turn for another player. At the end everything just stops until the presenter closes the window.

There should be three classes. The game class itself and two window classes, one for the spectator and one for the presenter. The presenter will drag their own window to another location.


Отлично. Теперь займемся красотой, нужно сделать этот проект приятный для зрителя и займемся пока первым окном.
Что я хочу:
1. Слева от таблици есть подписи строк, убери их. 
2. Пусть к каждой песни в скобочках добавляется номер по которому она была представленна в списке, это нужно чтобы участники понимали её порядковый немер.
3. Пусть изначальное окно будет большего размера, я хочу чтобы при режиме full mode активное поле тоже увеличивалось а не было бы такого же мелкого шрифта
4. Сделай какое нибудь красивое окошко для каждой песни
5. Во время голосования пусть окошко каждой песни, которая была в текущем цикле и ей выставился балл будет окрашиваться другим цветом. Во время нового голосования пусть они примут в начале цвет по умолчанию.
6. Пусть будет плавный переход. Я имею ввиду что когда идет сортировка пусть песни плавно меняют свои места.
7. Сделай красивый фон с анимацией, наверное что-то такое есть в стандартах от qt но можешь что нибудь другое придумать.
8. Пусть снизу высвечивается текущий статус игры: Ждем участников, Сейчас голосует игрок N и он передает m баллов ... и т.д. подумай