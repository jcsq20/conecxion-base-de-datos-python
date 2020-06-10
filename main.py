import pymysql as MySQLdb

HOST = "localhost"
USER = "root"
PASSWORD = "123456"
DATABASE = "minicurso_python"


USER_TABLE = """ CREATE TABLE users(
                id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL,
                password VARCHAR(50) NOT NULL)"""

DROP_TABLE = "DROP TABLE IF EXISTS users "
SHOW_TABLES = "SHOW TABLES"
INSERT_USER = "INSERT INTO users(username, password) VALUES('{username}','{password}')"
SELECT_USER = "SELECT * FROM users where id = {id}"
UPDATE_USER = "UPDATE users SET username='{username}',password='{password}' where id = {id}"
DELETE_USER = "DELETE FROM users where id = {id}"
if __name__ == "__main__":
    try:
        #MySQLdb.connect("host", "username", "password", "namedb")
        connection = MySQLdb.connect(HOST, USER, PASSWORD, DATABASE)
        cursor = connection.cursor()#para poder interactuar creamos este cursor

        cursor.execute(DROP_TABLE)
        cursor.execute(USER_TABLE)

        #mostrar tablas
        #cursor.execute(SHOW_TABLES)
        #tables = cursor.fetchall()
        #for table in tables:
            #print(table)

        #insertar valores
        #name = input("ingrese el username: ")
        #pasw = input("ingrese el contraseña: ")
        query = INSERT_USER.format(username="juan", password="123")
        print(query)
        #los try y commit siempre se usan cuando se modifiquen los datos
        try:#lo ponemos en try por si cometemos un error en la insercion los muetre
            cursor.execute(query)
            connection.commit()#intenta persistir los datos en la base de datos
        except:
            connection.rollback()# si vota error que lo deje en un estado anterior 

        #mostrar tablas
        query = SELECT_USER.format(id=1)
        #print(query)
        cursor.execute(query)
        users = cursor.fetchall()
        for user in users:
            print(user)

        #actualizar tablas
        query = UPDATE_USER.format(username="juan1",password="123445",id=1)
        print(query)
        try:#lo ponemos en try por si cometemos un error en la insercion los muetre
            cursor.execute(query)
            connection.commit()#intenta persistir los datos en la base de datos
        except:
            connection.rollback()# si vota error que lo deje en un estado anterior 

        #eliminar registros
        query = DELETE_USER.format(id=1)
        print(query)
        try:#lo ponemos en try por si cometemos un error en la insercion los muetre
            cursor.execute(query)
            connection.commit()#intenta persistir los datos en la base de datos
        except:
            connection.rollback()# si vota error que lo deje en un estado anterior 



        connection.close()#cierro la conecxion
    except MySQLdb.Error as error:
        print(error)