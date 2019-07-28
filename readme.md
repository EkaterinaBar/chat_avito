Тестовое задание на позицию стажера-бекендера

HTTP сервер написан на языке программирования Python с использованием БД sqlite
В приложении используется библиотека http-parser для Python (скачивается автоматически при использовании docker)

Для запуска сервера необходимо выполнить команду docker-compose up из корня моего git репозитория


ВАЖНОЕ ПРИМЕЧАНИЕ:
При тестировании сервера на Windows обнаружилось, что в командах необходимо заменить одинарные кавычки на двойные.

Примеры запросов при запуске на Windows:

Добавить нового пользователя:

curl --header "Content-Type: application/json"  --request POST  --data "{\"username\": \"user_4\"}" http://localhost:9000/users/add

Создать новый чат между пользователями:

curl --header "Content-Type: application/json" --request POST --data "{\"name\": \"chat_3\", \"users\": [\"1\", \"3\"]}" http://localhost:9000/chats/add

Отправить сообщение в чат от лица пользователя:

curl --header "Content-Type: application/json" --request POST --data "{\"chat\": \"2\", \"author\": \"1\", \"text\": \"hello\"}" http://localhost:9000/messages/add

Получить список чатов конкретного пользователя:

curl --header "Content-Type: application/json" --request POST --data "{\"user\": \"1\"}" http://localhost:9000/chats/get

Получить список сообщений в конкретном чате:

curl --header "Content-Type: application/json" --request POST --data "{\"chat\": \"1\"}" http://localhost:9000/messages/get