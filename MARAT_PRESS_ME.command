# Этот скрипт активирует виртуальное окружение и запускает main.py.
# Чтобы его запустить двойным кликом в Finder:
# 1. Сохраните этот файл с расширением .command, например, MARAT_PRESS_ME.command.
# 2. Сделайте файл исполняемым командой:
#      chmod +x MARAT_PRESS_ME.command
# 3. Дважды кликните по файлу в Finder – откроется Terminal и выполнится скрипт.

cd "$(dirname "$0")"
source .venv/bin/activate
python3 main.py
