import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

def init_db():
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    
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

class NotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Заметки")
        self.conn = init_db()
        
        self.create_widgets()

    def create_widgets(self):
        # Кнопка для добавления заметки
        self.add_button = tk.Button(self.root, text="Добавить заметку", command=self.add_note)
        self.add_button.pack(pady=10)

        # Кнопка для изменения заметки
        self.update_button = tk.Button(self.root, text="Изменить заметку", command=self.update_note)
        self.update_button.pack(pady=10)

        # Кнопка для удаления заметки
        self.delete_button = tk.Button(self.root, text="Удалить заметку", command=self.delete_note)
        self.delete_button.pack(pady=10)

        # Кнопка для отображения всех заметок
        self.show_button = tk.Button(self.root, text="Показать все заметки", command=self.show_notes)
        self.show_button.pack(pady=10)

        # Текстовое поле для отображения заметок
        self.text_area = scrolledtext.ScrolledText(self.root, width=50, height=20)
        self.text_area.pack(pady=10)

    def add_note(self):
        note = simpledialog.askstring("Добавить заметку", "Введите текст заметки:")
        category = simpledialog.askstring("Добавить категорию", "Введите категорию заметки:")
        if note and category:
            add_note_to_db(note, category, self.conn)
            messagebox.showinfo("Успех", "Заметка добавлена!")
        else:
            messagebox.showwarning("Внимание", "Текст заметки и категория не могут быть пустыми.")

    def update_note(self):
        note_id = simpledialog.askinteger("Изменить заметку", "Введите ID заметки для изменения:")
        new_content = simpledialog.askstring("Новый текст заметки", "Введите новый текст заметки:")
        new_category = simpledialog.askstring("Новая категория", "Введите новую категорию заметки:")
        if note_id and new_content and new_category:
            update_note_in_db(note_id, new_content, new_category, self.conn)
            messagebox.showinfo("Успех", "Заметка обновлена!")
        else:
            messagebox.showwarning("Внимание", "ID, текст заметки и категория не могут быть пустыми.")

    def delete_note(self):
        note_id = simpledialog.askinteger("Удалить заметку", "Введите ID заметки для удаления:")
        if note_id:
            delete_note_from_db(note_id, self.conn)
            messagebox.showinfo("Успех", "Заметка удалена!")
        else:
            messagebox.showwarning("Внимание", "ID не может быть пустым.")

    def show_notes(self):
        notes = read_notes_from_db(self.conn)
        self.text_area.delete(1.0, tk.END)  # Очистка текстового поля
        for note in notes:
            self.text_area.insert(tk.END, f"ID: {note[0]}, Заметка: {note[1]}, Категория: {note[2]}\n")

    def close(self):
        self.conn.close()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = NotesApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)  # Обработка закрытия окна
    root.mainloop()