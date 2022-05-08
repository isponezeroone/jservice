1) Создаем проект командой с помощью docker-compose из файла docker-compose.yml, билдим docker-образ и запускаем docker-контейнер.
docker-compose up -d --build

2) Заходим в браузере http://localhost:8004/docs и в окне POST запроса в теле запроса "questions_num" задаем необходимое количество вопросов. Нажимаем Execute. В Response body получаем в результате строку "question" с значением предыдущего сохраненного вопроса.

3) Для проверки работы БД можно отправить GET запрос и в Response body будет список всех сохраненных вопросов в базе данных.

4) Для проверки работы volumes с помощью команды docker-compose down остановим сервис и удалим docker-контейнеры. Далее снова запустим docker-контейнер командой docker-compose up -d и выполним GET запрос по адресу http://localhost:8004/docs. В итоге получим данные из БД, что говорит о том, что данные БД были верно сохранены на локальном диске. Так же это можно проверить перезапустив контейнеры командой docker-compose restart.

Основной скрипт main.py находится в папке project/app.
