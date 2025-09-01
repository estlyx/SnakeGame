Классическая игра 'Змейка'

Для локальной сборки/разработки создаем виртуальное окружение и устанавливаем зависимости

````
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
````

Сборка осуществляется через pyinstaller командой `pyinstaller --onefile main.py`


После выполнения команды исполняемый файл `main` лежит в папке dist
