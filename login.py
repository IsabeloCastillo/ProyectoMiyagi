import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
import re  # Para usar expresiones regulares
from main import init_gui

# Funciones para gestionar la base de datos
def crear_tabla_usuarios():
    conexion = sqlite3.connect('usuarios.db')
    cursor = conexion.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                      (usuario TEXT PRIMARY KEY,
                       password TEXT)''')
    conexion.commit()

    # Añadir un usuario por defecto
    hash_password = hashlib.sha256("Tokio*123".encode()).hexdigest()
    cursor.execute("INSERT OR IGNORE INTO usuarios (usuario, password) VALUES (?, ?)",
                   ('isabelito', hash_password))

    conexion.commit()
    conexion.close()

def es_password_segura(password):
    if len(password) < 8:
        return False
    if not re.search("[a-zA-Z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    if not re.search("[@#$%^&+=]", password):
        return False
    return True



def verificar_login_en_db(usuario, password):
    conexion = sqlite3.connect('usuarios.db')
    cursor = conexion.cursor()
    hash_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND password = ?", (usuario, hash_password))
    data = cursor.fetchone()
    conexion.close()
    if data:
        messagebox.showinfo("Login exitoso", f"Bienvenido {usuario}")
        return True
    else:
        messagebox.showerror("Login fallido", "Usuario o password incorrectos")
        return False

# Interfaz gráfica de usuario
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Login")
        self.root.geometry("3840x2160")  # Tamaño de la ventana
        self.root.configure(bg="#2c3e50")  # Color de fondo de la ventana
        self.usuario_actual = None
        crear_tabla_usuarios()
        self.init_gui()

    def init_gui(self):
        tk.Label(self.root, text="Usuario:", bg="#2c3e50", fg="#ecf0f1", font=("Arial", 18)).grid(row=0, column=0,
                                                                                                  padx=20, pady=20)
        self.entry_usuario = tk.Entry(self.root, font=("Arial", 18))
        self.entry_usuario.grid(row=0, column=1, padx=20, pady=20)

        tk.Label(self.root, text="Contraseña:", bg="#2c3e50", fg="#ecf0f1", font=("Arial", 18)).grid(row=1,
                                                                                                     column=0,
                                                                                                     padx=20,
                                                                                                     pady=20)
        self.entry_password = tk.Entry(self.root, show="*", font=("Arial", 18))
        self.entry_password.grid(row=1, column=1, padx=20, pady=20)

        tk.Button(self.root, text="Login", command=self.verificar_login, bg="#2980b9", font=("Arial", 18)).grid(
            row=2, columnspan=2, pady=20)

        # Configura las columnas para centrar los campos de entrada
        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(0, weight=0)

    def verificar_login(self):
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()
        if verificar_login_en_db(usuario, password):
            self.usuario_actual = usuario
            self.root.destroy()
            init_gui()

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()