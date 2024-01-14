import psycopg2


# Функция, создающая структуру базы данных(таблицы).
def create_db(conn, cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Clients_info(
        client_id SERIAL PRIMARY KEY,
        thirst_name VARCHAR(30) NOT NULL,
        last_name VARCHAR(40) NOT NULL,
        email VARCHAR(254) UNIQUE
        );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Phone_numbers(
        number SERIAL PRIMARY KEY,
        client_id INTEGER REFERENCES Clients_info(client_id)
        );
    """)
    conn.commit()
    return


# Функция, позволяющая удалить созданные ранее таблицы.
def del_bd(conn, cur):
    cur.execute("""
        DROP TABLE Phone_numbers; 
        DROP TABLE Clients_info;
        """)
    conn.commit()
    return


# Функция, позволяющая добавить телефон для существующего клиента.
def add_phone(conn, cur, phone_number, id_new_client):
    cur.execute("""
    INSERT INTO Phone_numbers(number, client_id) VALUES (%s, %s) RETURNING number, client_id;
                """, (phone_number, id_new_client))
    result = cur.fetchone()
    res_phone = result[1]
    print(f"Вы добавили номер телефона {res_phone} в таблицу {result}")
    conn.commit()
    return res_phone


# Функция, позволяющая добавить нового клиента.
def new_client(conn, cur, name, last_name, email_client):
    cur.execute("""
    INSERT INTO Clients_info(thirst_name, last_name, email) VALUES (%s, %s, %s) RETURNING client_id, 
    thirst_name, last_name, email;
            """, (name, last_name, email_client))
    result = cur.fetchone()
    print(f"Вы внесли данные клиента{result} в таблицу. Ваш уникальный id - {result[0]}")
    id = result[0]
    conn.commit()
    return id


# Функция, позволяющая изменить данные о клиенте.
def update_bd(conn, cur, id):
    pass


if __name__ == '__main__':
    print("Здравствуйте! Вы зашли в программу для создания базы данных! Приятного рабочего дня!")
    db = input("Введите название для базы данных: ")
    add_user = input("Введите Ваш логин: ")
    pass_bd = input("Введите пароль: ")
    with psycopg2.connect(database=db, user=add_user, password=pass_bd) as conn:
        with conn.cursor() as cur:
            del_bd(conn, cur)
            print("Перед созданием новой базы данных, все предыдущие таблицы были успешно удалены!")
            # создадим новую таблицу
            create_db(conn, cur)
            print("Новые таблицы для загрузки данных о клиенте созданы!")
            # Справка
            HELP = int(input(f"1 - Добавить нового клиента; 2 - Изменить данные о клиенте; 3 - Удалить клиента;\n"
                             f" 4 - Найти клиента по его данным: имени, фамилии, email или телефону."))
            if HELP == 1:
                print("Давайте добавим нового клиента!")
                name = input("Введите имя клиента: ")
                last_name = input("Введите фамилию клиента: ")
                email_client = input("Введите почту клиента: ")
                # добавим нового клиента в таблицу
                add_client = input("Справка: для выхода из программы введите - stop,\n"
                                   " для начала добавления клиентов - add ")
                if add_client == "add":
                    while add_client != "stop":
                        new_client(conn, cur, name, last_name, email_client)
                        # добавим телефон для существующего клиента
                        try:
                            phone_number = int(input("Введите номер телефона, который хотите добавить: "))
                            id_new_client = int(input("Введите номер id: "))
                        except ValueError:
                            print("Внимание! Вы ввели некорректный номер!\n"
                                  " Номер телефона и id может содержать только числа.")
                        add_phone(conn, cur, phone_number, id_new_client)
            # попробуем изменить данные о клиенте
            if HELP == 2:
                pass
    conn.close()









#Функция, позволяющая удалить телефон для существующего клиента.
#Функция, позволяющая удалить существующего клиента.
#Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.



