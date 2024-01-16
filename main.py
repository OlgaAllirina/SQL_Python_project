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
        number VARCHAR(11) PRIMARY KEY,
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


# Функции, позволяющая изменить данные о клиенте.
def update_name(conn, cur, id_name, up_name):
    cur.execute("""
    UPDATE Clients_info SET thirst_name = %s
    WHERE client_id = %s RETURNING client_id, thirst_name; """, (up_name, id_name))
    result = cur.fetchone()
    print(f"Вы изменили имя в таблице на {result}.")
    conn.commit()
    return result


def update_last_name(conn, cur, id_name, up_last_name):
    cur.execute("""
        UPDATE Clients_info SET last_name = %s
        WHERE client_id = %s RETURNING client_id, last_name; """, (up_last_name, id_name))
    result = cur.fetchone()
    print(f"Вы изменили имя в таблице на {result[1]}.")
    conn.commit()
    return result[1]


def update_email(conn, cur, id_name, up_email):
    cur.execute("""
            UPDATE Clients_info SET last_name = %s
            WHERE client_id = %s RETURNING client_id, email; """, (up_email, id_name))
    result = cur.fetchone()
    print(f"Вы изменили имя в таблице на {result[2]}.")
    conn.commit()
    return result[2]


def update_phone(conn, cur, id_name, up_phone):
    cur.execute("""
            UPDATE Phone_numbers SET number = %s
            WHERE client_id = %s RETURNING client_id, number; """, (up_phone, id_name))
    result = cur.fetchone()
    print(f"Вы изменили имя в таблице на {result[1]}.")
    conn.commit()
    return result[1]


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
            # добавим нового клиента в таблицу
            add_client = input("Справка: для выхода из программы введите - stop, для начала добавления клиентов - add ")
            if add_client == "add":
                while add_client != "stop":
                    name = input("Введите имя клиента: ")
                    last_name = input("Введите фамилию клиента: ")
                    email_client = input("Введите почту клиента: ")
                    new_client(conn, cur, name, last_name, email_client)
                    # добавим телефон для существующего клиента
                    try:
                        phone_number = int(input("Введите номер телефона, который хотите добавить: "))
                        id_new_client = int(input("Введите номер id: "))
                    except ValueError:
                        print("Внимание! Вы ввели некорректный номер!Номер телефона и id может содержать только числа.")
                    add_phone(conn, cur, phone_number, id_new_client)
                    add_client = input("Нажмите add для добавления следующего клиента, stop для выхода из программы:  ")
            # Справка
            HELP = int(input(f" 1  - Изменить данные о клиенте; 2 - Удалить клиента;\n"
                             f" 3 - Найти клиента по его данным: имени, фамилии, email или телефону."))
            # попробуем изменить данные о клиенте
            if HELP == 1:
                help_update = int(input("Для дальнейшей работы с программой, напишете цифру, \n"
                                        "соответствующую критерию, по которому хотите обновить данные: \n"
                                        "1 - изменить имя клиента, 2 - изменить фамилию клиента, \n"
                                        "3 - изменить почту клиента, 4 - изменить номер телефона. "))
                if help_update == 1:
                    id_name = int(input("Введите id клиента: "))
                    up_name = input("Введите новое имя: ")
                    update_name(conn, cur, id_name, up_name)
                elif help_update == 2:
                    id_name = int(input("Введите id клиента: "))
                    up_last_name = input("Введите новую фамилию клиента: ")
                    update_last_name(conn, cur, id_name, up_last_name)
                elif help_update == 3:
                    id_name = int(input("Введите id клиента: "))
                    up_email = input("Введите новый email клиента: ")
                    update_email(conn, cur, id_name, up_email)
                elif help_update == 4:
                    id_name = int(input("Введите id клиента: "))
                    up_phone = input("Введите новый телефон клиента: ")
                    update_phone(conn, cur, id_name, up_phone)

    conn.close()









#Функция, позволяющая удалить телефон для существующего клиента.
#Функция, позволяющая удалить существующего клиента.
#Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.



