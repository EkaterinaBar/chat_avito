�������� ������� �� ������� �������-���������

HTTP ������ ������� �� ����� ���������������� Python � �������������� �� sqlite
� ���������� ������������ ���������� http-parser ��� Python (����������� ������������� ��� ������������� docker)

��� ������� ������� ���������� ��������� ������� docker-compose up �� ����� ����� git �����������


������ ����������:
��� ������������ ������� �� Windows ������������, ��� � �������� ���������� �������� ��������� ������� �� �������.

������� �������� ��� ������� �� Windows:

�������� ������ ������������:
curl --header "Content-Type: application/json"  --request POST  --data "{\"username\": \"user_4\"}" http://localhost:9000/users/add

������� ����� ��� ����� ��������������:
curl --header "Content-Type: application/json" --request POST --data "{\"name\": \"chat_3\", \"users\": [\"1\", \"3\"]}" http://localhost:9000/chats/add

��������� ��������� � ��� �� ���� ������������:
curl --header "Content-Type: application/json" --request POST --data "{\"chat\": \"2\", \"author\": \"1\", \"text\": \"hello\"}" http://localhost:9000/messages/add

�������� ������ ����� ����������� ������������:
curl --header "Content-Type: application/json" --request POST --data "{\"user\": \"1\"}" http://localhost:9000/chats/get

�������� ������ ��������� � ���������� ����:
curl --header "Content-Type: application/json" --request POST --data "{\"chat\": \"1\"}" http://localhost:9000/messages/get