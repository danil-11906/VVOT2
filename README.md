## Барков Данил, 11-906

index.py - код контейнера, кладет в новый бакет обработанное изображение

реализация Telegram бота: fucntion-tg.py
получение данных для обработки: fucntion-face.py

докерфайл для контейнера: Dockerfile
конфиг GATEWAY: api-gateway 

Создать бакет с именем itis-2022-2023-vvot39-photos в сервисе «Yandex Object Storage»

Создать облачную функцию с именем vvot39-face-detection в сервисе «Yandex Cloud Functions» и скопировать содержимое файла из репозитория с аналогичным названием. Добавить  accessKey и secretKey взятые из сервисного аккаунта с ролью admin.

Создать триггер с именем vvot39-photo-trigger с настройками как на картине с названием vvot39-photo-trigger в репозитории.

Создать очередь с именем vvot39-tasks в сервисе «Yandex Message Queue». 

Создать бакет с именем itis-2022-2023-vvot39-faces

Создать базу даннынных vvot39-db-photo-face в сервисе «Yandex Managed Service for YDB» и в ней создать таблицу с именем faces со структурой как на фото vvot39-db-photo-face в репозитории.

Создать Api шлюз с именем itis-2022-2023-vvot39-api в сервисе «API Gateway» и скопировать содержимое yml файла из репозитория.

TG_BOT = https://t.me/vvot2022_task2_bot
  ![photo_2022-12-25_11-54-06 (2)](https://user-images.githubusercontent.com/55778811/209463398-5f4b4871-aced-4211-b916-27d96d17a444.jpg)

