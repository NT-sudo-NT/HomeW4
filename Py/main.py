import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

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

def display_notes(conn):
    notes = read_notes_from_db(conn)
    display_area.delete(1.0, tk.END)  # Очистка области отображения
    for note in notes:
        display_area.insert(tk.END, f"ID: {note[0]}, Заметка: {note[1]}, Категория: {note[2]}\n")

def add_note():
    note = simpledialog.askstring("Добавить заметку", "Введите текст заметки:")
    category = simpledialog.askstring("Добавить заметку", "Введите категорию заметки:")
    if note and category:
        add_note_to_db(note, category, conn)
        messagebox.showinfo("Успех", "Заметка добавлена!")
    else:
        messagebox.showwarning("Ошибка", "Текст и категория не могут быть пустыми.")

def update_note():
    note_id = simpledialog.askinteger("Изменить заметку", "Введите ID заметки для изменения:")
    new_content = simpledialog.askstring("Изменить заметку", "Введите новый текст заметки:")
    new_category = simpledialog.askstring("Изменить заметку", "Введите новую категорию заметки:")
    if note_id and new_content and new_category:
        update_note_in_db(note_id, new_content, new_category, conn)
        messagebox.showinfo("Успех", "Заметка изменена!")
    else:
        messagebox.showwarning("Ошибка", "ID, текст и категория не могут быть пустыми.")

def delete_note():
    note_id = simpledialog.askinteger("Удалить заметку", "Введите ID заметки для удаления:")
    if note_id:
        delete_note_from_db(note_id, conn)
        messagebox.showinfo("Успех", "Заметка удалена!")
    else:
        messagebox.showwarning("Ошибка", "ID не может быть пустым.")

# Инициализация базы данных
conn = init_db()

# Создание основного окна
root = tk.Tk()
root.title("Заметки")

# Создание кнопок
btn_add = tk.Button(root, text="Добавить заметку", command=add_note)
btn_add.pack(pady=10)

btn_update = tk.Button(root, text="Изменить заметку", command=update_note)
btn_update.pack(pady=10)

btn_delete = tk.Button(root, text="Удалить заметку", command=delete_note)
btn_delete.pack(pady=10)

btn_display = tk.Button(root, text="Показать все заметки", command=lambda: display_notes(conn))
btn_display.pack(pady=10)

# Область для отображения заметок
display_area = scrolledtext.ScrolledText(root, width=40, height=10)
display_area.pack(pady=10)

# Запуск основного цикла приложения
root.mainloop()

# Закрываем соединение с базой данных
conn.close()