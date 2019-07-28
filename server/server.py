import socket
import sqlite3
import time
import json
import sys
import re
from http_parser.pyparser import HttpParser
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'dbForChat.db')
class myRequest:
    def __init__(self, content_type, method, data,path):
        self._content_type = content_type
        self._method = method
        self._data = data
        self._path = path
    def toPrint(self):
        print("content_type: ",self._content_type)
        print("method: ",self._method)
        print("data: ",self._data)
        print("path: ",self._path)
class MyHTTPServer:
    def __init__(self, host, port, server_name):
        self._host = host
        self._port = port
        self._server_name = server_name

    def create_serv_sock(self):
        serv_sock = socket.socket(socket.AF_INET,      # задаем семейство протоколов 'Интернет' (INET)
                            socket.SOCK_STREAM)  # задаем тип передачи данных 'потоковый' (TCP)
        serv_sock.bind((self._host, self._port)) 
        serv_sock.listen() # можно установить размер очереди входящих подключений
        print("Server started")
        return serv_sock

    def connection(self,serv_sock):
        client_sock, client_addr = serv_sock.accept()
        print('Connected by', client_addr)
        return client_sock

    def read_data(self,client_sock,delimiter):
        request=bytearray()
        try:
            while True:
                data = client_sock.recv(1024)
                if not data: # Клиент преждевременно отключился.
                    return None
                request += data
                if request==b'exit\r\n':
                    return None
                if delimiter in request:
                    print("Client send: ", request)
                    return request
        except ConnectionResetError: # Соединение было неожиданно разорвано.
            return None

    def users_add(self,req): #Добавить нового пользователя
        conn = sqlite3.connect(db_path) # соединение с базой данных
        cursor = conn.cursor() # курсор - это специальный объект который делает запросы и получает их результаты 
        sql_statement = "SELECT count(*) FROM user"
        try: #try parsing to dict
            json_string = str(req._data).strip("'<>() ").replace('\'', '\"')
            parsed = json.loads(json_string)
        except:
            print(sys.exc_info())
            return '400: Bad Request (Wrong JSON)'
        username = parsed['username']
        try:
            cursor.execute(sql_statement)
            result = cursor.fetchall()
            num = result.pop() #получили строку
            num_id = re.findall('(\d+)', str(num)) #получили список чисел в строке
            num_id = int(num_id.pop())+1 #посчитали id
            print("id: ",num_id)
            print("username: ",username)
            cursor.execute("insert into user values (?,?,?)",(num_id,username,"'"+time.asctime()+"'"))
        except sqlite3.DatabaseError as err: 
            print(str(err))      
            return '400: Bad Request (DataBase: '+str(err)+')'
        else:
            conn.commit()
        conn.close()
        return num_id
    
    def messages_add(self,req): #Отправить сообщение в чат от лица пользователя
        conn = sqlite3.connect(db_path) # соединение с базой данных
        
        cursor = conn.cursor() # курсор - это специальный объект который делает запросы и получает их результаты 
        cursor.execute('PRAGMA foreign_keys = ON;') #чтобы включить поддержку внешних ключей
        conn.commit() 
        sql_statement = "SELECT count(*) FROM message"
        try: #try parsing to dict
            json_string = str(req._data).strip("'<>() ").replace('\'', '\"')
            parsed = json.loads(json_string)
        except:
            print(sys.exc_info())
            return '400: Bad Request (Wrong JSON)'
        id_chat = int(parsed['chat'])
        id_author = int(parsed['author'])
        text = parsed['text']
        try:
            cursor.execute(sql_statement)
            result = cursor.fetchall()
            num = result.pop() #получили строку
            id_mess = re.findall('(\d+)', str(num)) #получили список чисел в строке
            id_mess = int(id_mess.pop())+1 #посчитали id
            print("id_mess: ",id_mess)
            print("id_chat: ",id_chat)
            print("id_author: ",id_author)
            print("text: ",text)
            cursor.execute("insert into message values (?,?,?,?,?)",(id_mess,id_chat,id_author,text,"'"+time.asctime()+"'"))
        except sqlite3.DatabaseError as err: 
            print(str(err))      
            return '400: Bad Request (DataBase: '+str(err)+')'
        else:
            conn.commit()
        conn.close()
        return id_mess
   
    def chats_add(self,req): # Создать новый чат между пользователями
        conn = sqlite3.connect(db_path) # соединение с базой данных
        cursor = conn.cursor() # курсор - это специальный объект который делает запросы и получает их результаты  
        cursor.execute('PRAGMA foreign_keys = ON;') #чтобы включить поддержку внешних ключей
        conn.commit() 
        sql_statement = "SELECT count(*) FROM chat"
        try: #try parsing to dict
            json_string = str(req._data).strip("'<>() ").replace('\'', '\"')
            parsed = json.loads(json_string)
        except:
            print(sys.exc_info())
            return '400: Bad Request (Wrong JSON)'
        name = parsed['name']
        listOfUsers = parsed['users']
        try:
            cursor.execute(sql_statement)
            result = cursor.fetchall()
            num = result.pop() #получили строку
            id_chat = re.findall('(\d+)', str(num)) #получили список чисел в строке
            id_chat = int(id_chat.pop())+1 #посчитали id
            print("id: ",id_chat)
            print("name: ",name)
            cursor.execute("insert into chat values (?,?,?)",(id_chat,name,"'"+time.asctime()+"'"))
            cursor.execute("SELECT count(*) FROM user_chat")
            result = cursor.fetchall()
            num = result.pop() #получили строку
            id_chat_user = re.findall('(\d+)', str(num)) #получили список чисел в строке
            id_chat_user = int(id_chat_user.pop())+1 #посчитали id
            for id_user in listOfUsers:
                cursor.execute("insert into user_chat values (?,?,?)",(id_chat_user,int(id_user),id_chat))
                id_chat_user=id_chat_user+1
        except sqlite3.DatabaseError as err: 
            print(str(err))      
            return '400: Bad Request (DataBase: '+str(err)+')'
        else:
            conn.commit()
        conn.close()
        return id_chat
    def chats_get(self,req): #Получить список чатов конкретного пользователя
        conn = sqlite3.connect(db_path) # соединение с базой данных
        cursor = conn.cursor() # курсор - это специальный объект который делает запросы и получает их результаты  
        sql_statement = "SELECT DISTINCT chat.id, chat.name, chat.created_at FROM chat, user_chat, message WHERE chat.id=user_chat.chat_id AND user_chat.user_id=? AND message.chat=chat.id ORDER BY message.id DESC"
        try: #try parsing to dict
            json_string = str(req._data).strip("'<>() ").replace('\'', '\"')
            parsed = json.loads(json_string)
        except:
            print(sys.exc_info())
            return '400: Bad Request (Wrong JSON)'
        user = parsed['user']
        try:
            cursor.execute(sql_statement,user)
            result = cursor.fetchall()
            print(result)
        except sqlite3.DatabaseError as err: 
            print(str(err))      
            return '400: Bad Request (DataBase: '+str(err)+')'
        else:
            conn.commit()
        conn.close()
        return result
    
    def messages_get(self,req): # Получить список сообщений в конкретном чате
        conn = sqlite3.connect(db_path) # соединение с базой данных
        cursor = conn.cursor() 
        sql_statement = "SELECT message.id, message.chat, chat.name,message.author,user.username,message.text,message.created_at FROM message,chat,user WHERE message.chat=? AND message.chat=chat.id AND message.author = user.id ORDER BY message.id"
        try: # парсим json
            json_string = str(req._data).strip("'<>() ").replace('\'', '\"')
            parsed = json.loads(json_string)
        except:
            print(sys.exc_info())
            return '400: Bad Request (Wrong JSON)'
        chat = parsed['chat']
        try:
            cursor.execute(sql_statement,chat)
            result = cursor.fetchall()
            print(result)
        except sqlite3.DatabaseError as err: 
            print(str(err))      
            return '400: Bad Request (DataBase: '+str(err)+')'
        else:
            conn.commit()
        conn.close()
        return result

    def understand_request(self,data):
        p = HttpParser()
        recved = len(data)
        try:
            p.execute(data, recved)
            content_type = p.get_headers()["CONTENT-TYPE"]
            method = p.get_method()
            dataOfReq = str(p.recv_body(), "utf-8")
            path = p.get_path()
        except:
            print(sys.exc_info())
            return '400: Bad Request'+sys.exc_info()
        req = myRequest(content_type,method,dataOfReq,path)
        req.toPrint()
        if req._data == '': # если нет data
            return '204: No Content'
        if req._content_type != 'application/json':
            return '501: Not Implemented'
        if req._method != 'POST':
            return '501: Not Implemented'
        if req._path =='/users/add':
            return self.users_add(req)
        if req._path =='/chats/add':
              return self.chats_add(req)
        if req._path =='/messages/add':
              return self.messages_add(req)
        if req._path =='/chats/get':
              return self.chats_get(req)
        if req._path =='/messages/get':
              return self.messages_get(req)

        

    def write_response(self, client_sock,data):
        data = str(data)
        client_sock.sendall(bytearray(data, "utf-8"))
        print("Send to client:",data)

    def run(self):
        serv_sock = self.create_serv_sock()
        while True:
            client_sock=self.connection(serv_sock)
            while True:
                data = self.read_data(client_sock,b'\n')
                if data is None: # Клиент отключился
                    print("Client off")  
                    break
                else: 
                    answer = self.understand_request(data)
                    self.write_response(client_sock,answer)

            client_sock.close()

if __name__ == "__main__":
    myServer = MyHTTPServer("",9000,'first')
    try:
        myServer.run()
    except KeyboardInterrupt:
        pass

