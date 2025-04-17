import sqlite3

def init_db():
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    
    # Создание таблицы для заметок с тремя столбцами: id, text и category.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            category TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    return conn

def add_note_to_db(note, category, conn):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO notes (text, category) VALUES (?, ?)', (note, category))
    conn.commit()

def read_notes_from_db(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes')
    notes = cursor.fetchall()
    return notes

def update_note_in_db(note_id, new_content, new_category, conn):
    cursor = conn.cursor()
    cursor.execute('UPDATE notes SET text = ?, category = ? WHERE id = ?', (new_content, new_category, note_id))
    conn.commit()

def delete_note_from_db(note_id, conn):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
    conn.commit()

def OpenWrite(inc):
    # Записываем заметку в текстовый файл
    with open("input.txt", 'a+') as file:
        file.write(inc + '\n')

def ReadFile():
    # Читаем и выводим содержимое текстового файла
    with open("input.txt", 'r') as file:
        content = file.read()
        print("-----------Вывод-----------\n")
        print("-> ", content)

if __name__ == "__main__":
    print("-----------Заметки-----------\n")
    
    # Инициализируем базу данных
    conn = init_db()

    while True:
        print("1. Изменить заметку")
        print("2. Добавить заметку")
        print("3. Удалить заметку")
        print("4. Показать все заметки")
        print("5. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            note_id = int(input("Введите ID заметки для изменения: "))
            new_content = input("Введите новый текст заметки: ")
            new_category = input("Введите новую категорию заметки: ")
            update_note_in_db(note_id, new_content, new_category, conn)

        elif choice == '2':
            AdStr = input("Введите текст для добавления: ")
            category = input("Введите категорию заметки: ")
            add_note_to_db(AdStr, category, conn)
            OpenWrite(AdStr)

        elif choice == '3':
            note_id = int(input("Введите ID заметки для удаления: "))
            delete_note_from_db(note_id, conn)

        elif choice == '4':
            notes = read_notes_from_db(conn)
            print("-----------Заметки из базы данных-----------\n")
            for note in notes:
                print(f"ID: {note[0]}, Заметка: {note[1]}, Категория: {note[2]}")

        elif choice == '5':
            print("Выход из программы.")
            break

    # Закрываем соединение с базой данных
    conn.close()