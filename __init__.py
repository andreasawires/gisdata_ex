import time
import datetime
import mysql.connector

def crea_report():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='batch',
            user='user',
            password='resu'
        )
        cursor = connection.cursor()
        print("\nconnesso!")

        # get all users
        cursor.execute("SELECT * FROM utenti")
        users = cursor.fetchall()
        print("\nutenti fetchati!")

        for user in users:
            # print("Id = ", user[0])
            # print("nome = ", user[1])
            # print("primo deposito  = ", user[2])
            # print("saldo  = ", user[3], "\n")

            cursor.execute(f"SELECT * FROM operazioni WHERE utente_id = {user[0]} ORDER BY giorno ASC")
            user_operations = cursor.fetchall()

            with open(f"{user[0]}.txt", "w") as file:
                file.writelines(f"{user[1]}\n\n")

                new_saldo = user[3]
                for operation in user_operations:
                    date_formatted = operation[2].strftime("%d-%m-%Y")
                    file.writelines(f"{date_formatted} ** € {operation[-1]:>8}\n")

                    new_saldo += operation[-1]

                if new_saldo != user[3]:
                    cursor.execute(f"UPDATE utenti SET saldo = {new_saldo} WHERE id = {user[0]}")
                    connection.commit()
                # print(new_saldo)

            print(f"\n{user[1]} fatto!\n")


    except Exception as e:
        print("Errore", e)
    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()

if __name__ == "__main__":
    while True:
        # script starts at 9:00 am
        now = datetime.datetime.now()
        if now.hour == 9 and now.minute == 0:
            crea_report()
            break
        time.sleep(60)