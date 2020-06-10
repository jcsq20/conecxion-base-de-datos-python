import peewee
import datetime

HOST = "localhost"
USER = "root"
PASSWORD = "123456"
NAME_DATABASE = "minicurso_python"

database = peewee.MySQLDatabase(NAME_DATABASE,host=HOST, port=3306, user=USER, password=PASSWORD)
#crear tabla User
class User(peewee.Model):
    username = peewee.CharField(unique=True, max_length=50, index=True)
    password = peewee.CharField(max_length=50)
    email = peewee.CharField(max_length=50, null=True)
    active = peewee.BooleanField(default=True)
    created_date = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = database #conecta
        db_table = "users" #asigna el nombre a la tabla

    def __str__(self):
        return self.username

class Store(peewee.Model):
    #relacion 1 a 1
    #user = peewee.ForeignKeyField(User, primary_key = True)

    #relacion 1 a m(1 usuarios puede tener muchas tiendas)
    user = peewee.ForeignKeyField(User, related_name = "stores")
    name = peewee.CharField(max_length=50)
    address = peewee.TextField()
    active = peewee.BooleanField(default=True)
    created_date = peewee.DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = database #conecta
        db_table = "stores" #asigna el nombre a la tabla

    def __str__(self):
        return self.name
#relacion m a m 
class UserStore(peewee.Model):
    user = peewee.ForeignKeyField(User, related_name = "stores")
    store = peewee.ForeignKeyField(Store, related_name = "users")
    class Meta:
        database = database
        db_table = "user_store"
    def __str__(self):
        return "{} - {}".format(self.user, self.store)

def create_tables():
    if UserStore.table_exists():
        UserStore.drop_table()
    if Store.table_exists():
        Store.drop_table()
    if User.table_exists():
        User.drop_table()
    User.create_table()
    Store.create_table()
    UserStore.create_table()

def insert_register():
    #***insertar registros***
    #1
    user = User()
    user.username = "juan"
    user.password = "123"
    user.email = "juan@pruebas.com"
    user.save()#persistir nuestros datos en la base de datos

    #2
    user = User(username="prueba", password="password",email="pereza@unsi.com")
    user.save()

    #3
    user = {'username':'cf', 'password': '123'}
    user = User(**user)
    user.save()

    #4 #para relacion 1 a 1
    user = User.create(username="prueba2", password="password1",email="pere2za@unsi.com")
    store = Store.create(name="prueba", address="estoy perdido", user=user )

    #5
    query = User.insert(username="prueba3", password="passwor3",email="suarez3@unsi.com")
    query.execute()

def obtener_and_actualizar():
    #***obtener datos 
    #1
    user = User.get(User.id == 1)
    #print(user)
    #2
    users = User.select().where(User.id > 3)
    #for user in users:
        #print(user)
    #3
    user = User.select(User.id, User.username, User.password).where(User.id ==1).get()
    #print(user.id)


    #***Modificar datos
    #1
    user = User.get(User.id == 1)
    user.active = False
    user.save()

    #2
    query = User.update(active=False).where(User.id == 2)
    query.execute()

def delete_register():
    #***Eliminar registros
    #1
    user = User.get(User.id == 3)
    user.delete_instance()

    #2 
    query = User.delete().where(User.id == 4)
    query.execute()

    #3 forma recursiva en todas las relaciones
    user = User.get(User.id == 3)
    user.delete_instance(recursive=True)

if __name__ == "__main__":
    create_tables()
    insert_register()
    #***joins
    query =(
        Store.select().join(User).where(User.id >=1)
        #.where(User.id == 1)
        #.order_by(Store.active.desc())
    )
    print("arriba")
    for store in query:
        print("entre")
        print(store)
    print("*" * 15)
    #*** consulta
    #count contarlos
    count = User.select().where(User.id > 2).count()
    print(count)
    #limitador obtener tantos registros
    users = User.select().where(User.id > 1).limit(2)
    for user in users:
        print(user)
    #ordener ascendente .asc()o + o el - o desc() para descendente
    users = User.select().where(User.id > 1).order_by(-User.username)
    for user in users:
        print(user)

    #*** verificar si existe
    bandera = User.select().where(User.id ==10).exists()
    if bandera:
        print("El usuario existe")
    else:
        print("El usuario No existe")