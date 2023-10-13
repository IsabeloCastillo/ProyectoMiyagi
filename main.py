# Módulos estándar
from datetime import datetime
from collections import OrderedDict

# Módulos externos de GUI y diálogos
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, Menu

# Módulos para temas en tkinter
from ttkthemes import ThemedTk

# Módulos para PDFs y estilos
from reportlab.lib import colors, units, styles, pagesizes
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer

# Módulos para bases de datos
import sqlite3
from database import conectar, obtener_nombre_del_proveedor, calcular_total_con_iva
import database  # ¿Realmente necesitas este import también?

# Módulos para abrir páginas web
import webbrowser

# Módulos propios
from funciones import *
from clases import Producto, Cliente, Proveedor, Albaran
from database import crear_factura_desde_albaran  # Esto parece redundante si ya tienes 'import database'

# Otros
import subprocess




# Definimos la función update_time que toma una etiqueta (label) como argumento
def update_time(label):
    # Obtenemos la hora y fecha actual
    now = datetime.now()

    # Formateamos la hora y fecha en un string
    formatted_date = now.strftime("%d-%m-%Y- %H:%M:%S")

    # Creamos el mensaje que queremos mostrar
    welcome_message = f"Sugerencias para hoy {formatted_date}."

    # Actualizamos el texto de la etiqueta (label) con nuestro mensaje
    label.config(text=welcome_message)

    # Llamamos a la misma función después de 1 segundo (1000 milisegundos)
    label.after(1000, update_time, label)



temas = {
    'blue': {'fg': 'red', 'bg': 'lavender'},
    'black': {'fg': 'red', 'bg': 'lavender'},
    'kroc' :{'fg': 'red', 'bg': 'lavender'},
    'clearlooks' :{'fg': 'red', 'bg': 'lavender'},
    'itft1' :{'fg': 'red', 'bg': 'lavender'},
    'winxpblue' :{'fg': 'red', 'bg': 'lavender'}
}


def cambiar_tema_completo(root,  footer_label, info_label, caducidad_label, tree, tema):
    # Cambiar el tema del root
    root.set_theme(tema)

    # Obtener los colores del tema seleccionado del diccionario 'temas'
    try:
        nuevo_color = temas[tema]['fg']
        nuevo_fondo = temas[tema]['bg']
    except KeyError:
        messagebox.showinfo(f"El tema {tema} no se encuentra en el diccionario.")

        print(f"El tema {tema} no se encuentra en el diccionario.")
        return

    # Actualizar colores del header, footer, info y caducidad
    footer_label.config(fg='slate blue', bg=nuevo_fondo)
    info_label.config(fg=nuevo_color, bg=nuevo_fondo)
    caducidad_label.config(fg=nuevo_color, bg=nuevo_fondo)

    # Actualizar el treeview
    #tree.tag_configure('tu_tag', background=nuevo_fondo, foreground=nuevo_color)




def init_gui():
    root = ThemedTk(theme="vista")
    root.title("Mi Ventana")
    style = ttk.Style()
    style.configure('.', font=('Courier', 13, "bold"), foreground='navy')

    # Configuración del Treeview
    style.configure("Treeview",
                    font=("Courier", 10, "bold"),
                    background="Sky Blue1",
                    fieldbackground="Steelblue1",
                    foreground="navy")

    style.configure("Treeview.Heading",
                    font=("Courier", 10, "bold"),
                    background="lawn green",
                    foreground="gray40")


    ancho = 1000
    alto = 600
    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()
    x = (ancho_pantalla / 2) - (ancho / 2)
    y = (alto_pantalla / 2) - (alto / 2)
    root.geometry(f"{ancho}x{alto}+{int(x)}+{int(y)}")

    # Header y Footer
    header_frame = tk.Frame(root, bg="lavender", padx=10, pady=10)
    header_frame.pack(side=tk.TOP, fill=tk.X)


    welcome_label = tk.Label(header_frame, bg="lavender", fg="slate blue", font=("Courier", 14, "bold"))
    welcome_label.pack()

    # Crear un label para mostrar el producto con menos stock
    info_label = tk.Label(header_frame, bg="lavender", fg="red", font=("Courier", 14, "bold"))
    info_label.pack()

    # Obtener el producto con menos stock y actualizar el label
    producto, cantidad = producto_con_menos_stock()
    info_label['text'] = f"Producto con menos stock: {producto}, Cantidad: {cantidad}"

    # Crear un label para mostrar los productos que caducan este año
    caducidad_label = tk.Label(header_frame, bg="lavender", fg="red", font=("Courier", 14, "bold"))
    caducidad_label.pack()

    # Obtener los productos que caducan este año y actualizar el label
    productos_caducan = productos_que_caducan_este_ano()
    productos_caducan_str = ", ".join([prod[0] for prod in productos_caducan])
    caducidad_label['text'] = f"Productos que caducan pronto: {productos_caducan_str}"

    update_time(welcome_label)  # Llama a la función para iniciar la actualización del tiempo

    # Obtener la fecha y hora actuales
    now = datetime.now()
    formatted_date = now.strftime("%d-%m-%Y- %H:%M:%S")

    footer_frame = tk.Frame(root, bg="lavender", padx=10, pady=5)
    footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
    footer_label = tk.Label(footer_frame, text="Miyagi Gest. v1.0 © 2023 Isabelo Company ™® ", bg="lavender", fg="slate blue",
                            font=("Courier", 20, "bold"))
    footer_label.pack()

    # Frames izquierdo y derecho con padding
    left_frame = ttk.Frame(root, padding="10 10 10 10")
    left_frame.pack(side=tk.LEFT, fill=tk.Y)

    right_frame = ttk.Frame(root, padding="10 10 10 10")
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


    table_frame = ttk.Frame(root, padding="10")  # padding es el espacio alrededor del contenido en el frame
    table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    tree = []



    productos_button = ttk.Button(left_frame, text="PRODUCTOS      ", style='TButton',
                                  command=lambda table_frame=table_frame: show_form('Producto', table_frame,
                                                                                    right_frame,cambiar_tema_completo,root,  footer_label, info_label, caducidad_label, tree),
                                  width=20)
    productos_button.pack(pady=20)

    clientes_button = ttk.Button(left_frame, text="CLIENTES   ", style='TButton',
                                 command=lambda table_frame=table_frame: show_form('Cliente', table_frame, right_frame,cambiar_tema_completo,root,  footer_label, info_label, caducidad_label, tree),
                                 width=20)
    clientes_button.pack(pady=20)

    proveedores_button = ttk.Button(left_frame, text="PROVEEDORES", style='TButton',
                                    command=lambda table_frame=table_frame: show_form('Proveedor', table_frame,
                                                                                      right_frame,cambiar_tema_completo,root,  footer_label, info_label, caducidad_label, tree),
                                    width=20)
    proveedores_button.pack(pady=20)

    btn_albaran = ttk.Button(left_frame, text="ALBARANES ", style='TButton',
                             command=lambda table_frame=table_frame: show_form('Albaran', table_frame, right_frame,cambiar_tema_completo,root,  footer_label, info_label, caducidad_label, tree),
                             width=20)
    btn_albaran.pack(pady=(20, 20))

    btn_factura = ttk.Button(left_frame, text="FACTURAS  ", style='TButton',
                             command=lambda table_frame=table_frame: show_form("Facturas", table_frame, right_frame,cambiar_tema_completo,root,  footer_label, info_label, caducidad_label, tree),
                             width=20)
    btn_factura.pack(pady=20)

    btn_funciones = ttk.Button(left_frame, text="FUNCIONES ", style='TButton',
                               command=lambda table_frame=table_frame: show_form('Funciones', table_frame, right_frame,cambiar_tema_completo,root,  footer_label, info_label, caducidad_label, tree),
                               width=20)
    btn_funciones.pack(pady=(20, 20))

    btn_temas = ttk.Button(left_frame, text="TEMAS ", style='TButton',
                               command=lambda table_frame=table_frame: show_form('Temas',table_frame, right_frame,cambiar_tema_completo,root,  footer_label, info_label, caducidad_label, tree),
                               width=20)
    btn_temas.pack(pady=(20, 20))


    root.mainloop()






# Función para registrar un nuevo usuario en la base de datos
def registrar_usuario_en_db(usuario, password):
    # Verificar si la contraseña cumple con los requisitos de seguridad
    if es_password_segura(password):

        # Conectar con la base de datos SQLite
        conexion = sqlite3.connect('usuarios.db')
        cursor = conexion.cursor()

        # Encriptar la contraseña con SHA-256
        hash_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            # Intentar insertar el nuevo usuario en la base de datos
            cursor.execute("INSERT INTO usuarios (usuario, password) VALUES (?, ?)", (usuario, hash_password))

        except sqlite3.IntegrityError:
            # Si el usuario ya existe, mostrar un mensaje de error y salir
            messagebox.showerror("Registro fallido", "El nombre de usuario ya existe", font=("Arial", 14))
            return False

        # Confirmar los cambios y cerrar la conexión con la base de datos
        conexion.commit()
        conexion.close()

        # Mostrar un mensaje de éxito
        messagebox.showinfo("Registro exitoso", "Usuario creado exitosamente", font=("Arial", 14))
        return True
    else:
        # Si la contraseña no es segura, mostrar un mensaje de error
        messagebox.showerror("Contraseña insegura",
                             "La password debe tener al menos 8 caracteres e incluir letras, números y símbolos especiales.",
                             font=("Arial", 14))
        return False


# Definir una función para mostrar un mensaje en una ventana emergente
def mostrar_mensaje(mensaje):
    ventana = tk.Tk()  # Crear una ventana de Tkinter
    ventana.withdraw()  # Ocultar la ventana principal para que no se muestre

    # Mostrar el mensaje en una ventana emergente de tipo "Información"
    messagebox.showinfo("Información", mensaje)

    ventana.destroy()  # Cerrar y eliminar la ventana de Tkinter

# Muestra todos los productos en una tabla
def show_all_products_table(right_frame):
    productos = database.obtener_productos()  # Aseguramos de que esta función obtenga los datos de tus productos

    # Asegurarnos de que algo en el right_frame se elimine
    for widget in right_frame.winfo_children():
        widget.destroy()

    # Crear un frame para la tabla dentro de tu right_frame
    table_frame = ttk.Frame(right_frame)
    table_frame.pack(fill=tk.BOTH, expand=1)


    # Convertir los productos a un diccionario que ttk.Treeview pueda entender
    columns = ['ID', 'NOMBRE', 'FAMILIA', 'PRECIO', 'IVA', 'PROVEEDOR', 'CANTIDAD', 'CADUCIDAD']

    # Crear el Treeview con el estilo definido
    tree = ttk.Treeview(table_frame, columns=columns, show='headings', style="Treeview")

    # Asociar el menú contextual con el evento de clic derecho en el Treeview
    tree.bind("<Button-3>", lambda event, tree=tree: show_context_menu(event, tree, 'producto'))  # Funcion para el boton  derecho del raton

    # Definimos las cabeceras
    for col in columns:
        tree.heading(col, text=col, anchor='center')  # Añadir anchor para centrar las cabeceras

    # Definir el ancho de las columnas y centrar el contenido
    tree.column('ID', width=50, anchor='center')
    tree.column('NOMBRE', width=390, anchor='w')
    tree.column('FAMILIA', width=150, anchor='w')
    tree.column('PRECIO', width=100, anchor='e')
    tree.column('IVA', width=70, anchor='e')
    tree.column('PROVEEDOR', width=300, anchor='w')
    tree.column('CANTIDAD', width=90, anchor='e')
    tree.column('CADUCIDAD', width=120, anchor='center')

    # Llenamos la tabla con los productos y aplicamos estilos alternos
    for i, producto in enumerate(productos):
        if i % 2 == 0:
            tree.insert("", "end", values=producto, tags=('EvenRow.Treeview',))
        else:
            tree.insert("", "end", values=producto, tags=('OddRow.Treeview',))

    # Empaquetamos la tabla y agregamos una barra de desplazamiento
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview, style="Thick.Vertical.TScrollbar")

    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill=tk.BOTH, expand=True)
    scrollbar.pack(side="right", fill="y")

    return tree


# Muestra todos los clientes en una tabla
def show_all_clients_table(right_frame):
    clientes = database.obtener_clientes()

    # Aseguramos que cualquier widget previo en right_frame se elimine
    for widget in right_frame.winfo_children():
        widget.destroy()

    # Creamos un frame para la tabla dentro del right_frame
    table_frame = ttk.Frame(right_frame)
    table_frame.pack(fill=tk.BOTH, expand=1)


    # Definimos las columnas para ttk.Treeview
    columns = ['ID', 'NOMBRE', 'CIF', 'DIRECCION', 'LOCALIDAD', 'PROVINCIA', 'TELEFONO', 'EMAIL']
    tree = ttk.Treeview(table_frame, columns=columns, show='headings', style="Treeview")
    tree.bind("<Button-3>", lambda event, tree=tree: show_context_menu(event, tree, 'cliente'))

    # Definimos las cabeceras y sus anchos
    for col in columns:
        tree.heading(col, text=col, anchor=tk.CENTER)  # Añadir anchor aquí para centrar las cabeceras
    tree.column('ID', width=50, anchor=tk.CENTER)
    tree.column('NOMBRE', width=330, anchor=tk.CENTER)
    tree.column('CIF', width=100, anchor=tk.CENTER)
    tree.column('DIRECCION', width=250, anchor=tk.CENTER)
    tree.column('LOCALIDAD', width=100, anchor=tk.CENTER)
    tree.column('PROVINCIA', width=100, anchor=tk.CENTER)
    tree.column('TELEFONO', width=100, anchor=tk.CENTER)
    tree.column('EMAIL', width=250, anchor=tk.CENTER)

    # Llenamos la tabla con los clientes
    for cliente in clientes:
        tree.insert("", "end", values=cliente)

    # Empaquetamos la tabla y agregamos una barra de desplazamiento
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill=tk.BOTH, expand=True)
    scrollbar.pack(side="right", fill="y")

    return tree

# Muestra todos los proveedores en una tabla
def show_all_providers_table(right_frame):
    proveedores = database.obtener_proveedores()

    # Aseguramos de que cualquier widget previo en right_frame se elimine
    for widget in right_frame.winfo_children():
        widget.destroy()

    # Creamos un frame para la tabla dentro de tu right_frame
    table_frame = ttk.Frame(right_frame)
    table_frame.pack(fill=tk.BOTH, expand=1)


    # Definimos las columnas para ttk.Treeview
    columns = ['ID', 'NOMBRE', 'CIF', 'DIRECCION', 'LOCALIDAD', 'PROVINCIA', 'TELEFONO', 'EMAIL']
    tree = ttk.Treeview(table_frame, columns=columns, show='headings', style='MiEstilo.Treeview')
    tree.bind("<Button-3>", lambda event, tree=tree: show_context_menu(event, tree, 'proveedor'))


    # Definimos las cabeceras y sus anchos
    for col in columns:
        tree.heading(col, text=col, anchor=tk.CENTER)  # Añadir anchor aquí para centrar las cabeceras
    tree.column('ID', width=50, anchor=tk.CENTER)
    tree.column('NOMBRE', width=330, anchor=tk.CENTER)
    tree.column('CIF', width=100, anchor=tk.CENTER)
    tree.column('DIRECCION', width=250, anchor=tk.CENTER)
    tree.column('LOCALIDAD', width=100, anchor=tk.CENTER)
    tree.column('PROVINCIA', width=100, anchor=tk.CENTER)
    tree.column('TELEFONO', width=100, anchor=tk.CENTER)
    tree.column('EMAIL', width=250, anchor=tk.CENTER)

    # Llenamos la tabla con los clientes
    for proveedores in proveedores:
        tree.insert("", "end", values=proveedores)

    # Empaquetamos la tabla y agregamos una barra de desplazamiento
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill=tk.BOTH, expand=True)
    scrollbar.pack(side="right", fill="y")

    return tree

# Muestra todos los albaranes en una tabla
def show_all_albaranes_table(right_frame):
    albaranes = database.obtener_albaran()

    # Aseguramos de que cualquier widget previo en right_frame se elimine
    for widget in right_frame.winfo_children():
        widget.destroy()

    # Creamos un frame para la tabla dentro del right_frame
    table_frame = ttk.Frame(right_frame)
    table_frame.pack(fill=tk.BOTH, expand=1)



    # Definimos las columnas para ttk.Treeview
    columns = ['ID ALBARAN', 'FECHA', 'ID CLIENTE', 'TOTAL']
    tree = ttk.Treeview(table_frame, columns=columns, show='headings', style='Treeview')
    tree.bind("<Button-3>", lambda event, tree=tree: show_context_menu(event, tree, 'albaran'))

    # Definimos las cabeceras y sus anchos
    for col in columns:
        tree.heading(col, text=col, anchor=tk.CENTER)  # Añadir anchor aquí para centrar las cabeceras
    tree.column('ID ALBARAN', width=50, anchor=tk.CENTER)
    tree.column('FECHA', width=330, anchor=tk.CENTER)
    tree.column('ID CLIENTE', width=100, anchor=tk.CENTER)
    tree.column('TOTAL', width=250, anchor=tk.CENTER)

    # Llenamos la tabla con los clientes
    for albaran in albaranes:
        tree.insert("", "end", values=albaran)

    # Empaquetamos la tabla y agregamos una barra de desplazamiento
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill=tk.BOTH, expand=True)
    scrollbar.pack(side="right", fill="y")

    return tree

def show_all_facturas_table(right_frame):
    facturas = database.obtener_factura()

    # Aseguramos de que cualquier widget previo en right_frame se elimine
    for widget in right_frame.winfo_children():
        widget.destroy()

    # Crear un frame para la tabla dentro del right_frame
    table_frame = ttk.Frame(right_frame)
    table_frame.pack(fill=tk.BOTH, expand=1)


    # Definir las columnas para ttk.Treeview
    columns = ['ID FACTURA', 'FECHA', 'ID CLIENTE', 'ID PROVEEDOR', 'PRODUCTO', 'CANTIDAD', 'IVA', 'DESCUENTO', 'TOTAL']
    tree = ttk.Treeview(table_frame, columns=columns, show='headings', style='Treeview')
    tree.bind("<Button-3>", lambda event, tree=tree: show_context_menu(event, tree, 'factura'))

    # Definiendo las cabeceras y ajustando el ancho
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    # Llenando la tabla con los albaranes
    for factura in facturas:
        tree.insert("", "end", values=factura)

    # Empaquetando la tabla y agregando una barra de desplazamiento
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill=tk.BOTH, expand=True)
    scrollbar.pack(side="right", fill="y")

    clear_right_frame(right_frame)

    return tree

# Función para mostrar diferentes formularios
def show_form(form_type, table_frame, right_frame, cambiar_tema_completo, root, footer_label, info_label,
              caducidad_label, tree):
    if not table_frame:
        table_frame = ttk.Frame(right_frame)
        table_frame.pack(fill=tk.BOTH, expand=1)

    for widget in right_frame.winfo_children():
        widget.destroy()

    entries = {}

    if form_type == "Producto":
        fields = ["NUEVO PRODUCTO", "FAMILIA", "PRECIO", "IVA", "CANTIDAD", "CADUCIDAD"]

        for field in fields:
            font_label = ('Courier', 12)
            label = ttk.Label(right_frame, font=font_label, text=f"{field}:")
            entry = ttk.Entry(right_frame, width=50)
            label.pack(pady=5)
            entry.pack(pady=5)
            entries[field] = entry

        try:
            provider_label = ttk.Label(right_frame, text="PROVEEDOR:")
            provider_label.pack(pady=5)
            provider_list = obtener_nombre_del_proveedor()  # Suponemos que esta función ya está definida
            provider_combobox = ttk.Combobox(right_frame, values=provider_list)
            provider_combobox.pack(pady=5)
            entries["PROVEEDOR"] = provider_combobox

        except Exception as e:
            error_msg = f"Hubo un error al crear el Combobox para los proveedores: {e}"
            mostrar_mensaje(error_msg)

        btn_create_product = ttk.Button(right_frame, text="CREAR PRODUCTO NUEVO", style='TButton',
                                        command=lambda: create_product(entries, right_frame))
        btn_create_product.pack(pady=20)

        btn_show_products = ttk.Button(right_frame, text="MOSTRAR LISTA DE PRODUCTOS", style='TButton',
                                       command=lambda: show_all_products_table(right_frame))
        btn_show_products.pack(pady=20)

    # Proceso similar para "Cliente"
    elif form_type == "Cliente":
        fields = ["NUEVO CLIENTE", "CIF", "DIRECCION", "LOCALIDAD", "PROVINCIA", "TELEFONO", "EMAIL"]

        for field in fields:
            font_label = ('Courier', 12)
            label = ttk.Label(right_frame, font=font_label, text=f"{field}:")
            entry = ttk.Entry(right_frame, width=50)
            label.pack(pady=5)
            entry.pack(pady=5)
            entries[field] = entry

        # Botones de acciones para clientes
        btn_create_client = ttk.Button(right_frame, text="CREAR CLIENTE NUEVO", style='TButton', command=lambda: create_client(entries, btn_create_client))
        btn_create_client.pack(pady=20)
        btn_show_clients = ttk.Button(right_frame, text="   MOSTRAR LISTA DE CLIENTES  ", style='TButton', command=lambda:show_all_clients_table(right_frame))
        btn_show_clients.pack(pady=20)

    # Repitiendo la estructura para "Proveedor"
    elif form_type == "Proveedor":
        # Campos específicos del proveedor
        fields = ["NUEVO PROVEEDOR", "CIF", "DIRECCION", "LOCALIDAD", "PROVINCIA", "TELEFONO", "EMAIL"]
        for field in fields:
            font_label = ('Courier', 12)
            label = ttk.Label(right_frame, font=font_label, text=f"{field}:")
            entry = ttk.Entry(right_frame, width=50)
            label.pack(pady=5)
            entry.pack(pady=5)
            entries[field] = entry

        # Botones de acciones para proveedores
        btn_create_providers = ttk.Button(right_frame, text="CREAR PROVEEDOR NUEVO", style='TButton', command=lambda: create_proveedor(entries, btn_create_providers))
        btn_create_providers.pack(pady=20)
        btn_show_providers = ttk.Button(right_frame, text="MOSTRAR LISTA DE PROVEEDORES", style='TButton', command=lambda: show_all_providers_table(right_frame))
        btn_show_providers.pack(pady=20)

    elif form_type == "Albaran":


        # Creamos dos sub-frames dentro del frame de la derecha
        form_frame = ttk.Frame(right_frame)
        treeview_frame = ttk.Frame(right_frame)
        form_frame.pack(side="left", fill="y")
        treeview_frame.pack(side="right", fill="both", expand=True)

        # Campos específicos para formulario del frame izquierdo
        fields = ["ClienteID","Nombre Cliente" ,"ProductoID",  "Cantidad"]

        entries = {}  # Diccionario para almacenar las entradas

        # Crear los campos de entrada en el formulario
        for field in fields:
            font_label = ('Arial', 12)
            label = ttk.Label(form_frame, font=font_label, text=f"{field}:")
            entry = ttk.Entry(form_frame, width=20)
            label.pack(pady=5)
            entry.pack(pady=5)
            entries[field] = entry

        # Crear el botón para añadir el albarán
        btn_nuevo_albaran = ttk.Button(form_frame, text="NUEVO ALBARAN",command=lambda: nuevo_albaran(tree))
        btn_nuevo_albaran.pack(pady=20)

        btn_imprimir = ttk.Button(form_frame, text="IMPRIMIR ALBARAN", command=imprimir_albaran)
        btn_imprimir.pack(pady=20)

        btn_mostrar_albaranes = ttk.Button(form_frame, text="MOSTRAR ALBARANES",
                                           command=lambda: show_all_albaranes_table(right_frame))
        btn_mostrar_albaranes.pack(pady=20)

        btn_imprimir = ttk.Button(form_frame, text="FINALIZAR ALBARAN", command=lambda: finalizar_albaran(tree))
        btn_imprimir.pack(pady=20)

        # Crear el Treeview para mostrar los items del albarán
        tree = ttk.Treeview(treeview_frame)
        tree.column("#0", width=0, stretch=tk.NO)

        tree.bind("<Button-3>", lambda event, tree=tree: show_context_menu(event, tree, tipo_elemento))
        tree["columns"] = (
        "ClienteID", "Nombre Cliente", "ProductoID", "Nombre Producto", "Precio", "Cantidad", "Fecha", "Total")

        # Configurar las cabeceras y el ancho de las columnas
        tree.heading("ClienteID", text="ClienteID")
        tree.heading("Nombre Cliente", text="Nombre Cliente")
        tree.heading("ProductoID", text="ProductoID")
        tree.heading("Nombre Producto", text="Nombre Producto")
        tree.heading("Precio", text="Precio")
        tree.heading("Cantidad", text="Cantidad")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Total", text="Total")

        # Configurar el ancho y alineación de cada columna
        tree.column("ClienteID", width=100, anchor=tk.CENTER)
        tree.column("Nombre Cliente", width=200)
        tree.column("ProductoID", width=100, anchor=tk.CENTER)
        tree.column("Nombre Producto", width=200)
        tree.column("Precio", width=100, anchor=tk.E)
        tree.column("Cantidad", width=100, anchor=tk.CENTER)
        tree.column("Fecha", width=100)
        tree.column("Total", width=100, anchor=tk.E)  # anchor="w" alinea el texto a la izquierda

        tree.pack(fill="both", expand=True)


    elif form_type == "Facturas":
        # Botones de acciones para facturas
        btn_factura_de_albaran = ttk.Button(right_frame, text="  FACTURA DE ALBARAN  ", style='TButton',
                                            command=lambda: imprimir_factura())
        btn_factura_de_albaran.pack(pady=10)
        btn_create_factura = ttk.Button(right_frame, text="   CREAR  FACTURA   ", style='TButton', command=lambda :coming_soon())
        btn_create_factura.pack(pady=10)
        btn_show_factura = ttk.Button(right_frame, text=" MOSTRAR   FACTURAS ", style='TButton',command=lambda:coming_soon())
        btn_show_factura.pack(pady=10)

        return

    elif form_type == "Funciones":
        # Botones de acciones para funciones
        btn_stock_total = ttk.Button(right_frame, text="   STOCK   TOTAL    ", style='TButton',
                                     command=lambda: obtener_stock_total())
        btn_stock_total.pack(pady=10)

        btn_create_total_ventas = ttk.Button(right_frame, text="   TOTAL DE VENTAS  ", style='TButton',
                                             command=lambda: total_de_ventas())
        btn_create_total_ventas.pack(pady=10)
        '''btn_menos_stock = ttk.Button(right_frame, text="     MENOS STOCK    ", style='TButton',
                                     command=lambda: producto_con_menos_stock())
        btn_menos_stock.pack(pady=10)'''

        btn_mas_vendido = ttk.Button(right_frame, text="PRODUCTO MAS VENDIDO", style='TButton',
                                     command=lambda: producto_mas_vendido())
        btn_mas_vendido.pack(pady=10)


        btn_eliminar_albaran = ttk.Button(right_frame, text="  ELIMINAR ALABARAN ", style='TButton',
                                              command=lambda: coming_soon())
        btn_eliminar_albaran.pack(pady=10)

        btn_actualizar_producto = ttk.Button(right_frame, text="ACTUALIZAR  PRODUCTO", style='TButton',
                                           command=lambda: actualizar_producto())
        btn_actualizar_producto.pack(pady=10)

        btn_eliminar_producto = ttk.Button(right_frame, text="  ELIMINAR PRODUCTO ", style='TButton',
                                               command=lambda: coming_soon())
        btn_eliminar_producto.pack(pady=10)

        btn_agregar_usuario = ttk.Button(right_frame, text="AÑADIR NUEVO USUARIO", style='TButton',
                                         command=lambda: coming_soon())
        btn_agregar_usuario.pack(pady=10)

    elif form_type == "Temas":
        # Botones de acciones para funciones

        btn_dark = ttk.Button(right_frame, text="   OSCURO   ", style='TButton',
                              command=lambda: cambiar_tema_completo(root, footer_label, info_label,
                                                                    caducidad_label, tree, 'black'))
        btn_dark.pack(pady=10)

        btn_clearlooks = ttk.Button(right_frame, text="   CLARO    ", style='TButton',
                                    command=lambda: cambiar_tema_completo(root, footer_label, info_label,
                                                                          caducidad_label, tree, 'clearlooks'))
        btn_clearlooks.pack(pady=10)


        btn_madera = ttk.Button(right_frame, text="   MADERA   ", style='TButton',
                                         command=lambda: cambiar_tema_completo(root,  footer_label, info_label, caducidad_label, tree, 'kroc'))
        btn_madera.pack(pady=10)


        btn_blue = ttk.Button(right_frame, text="SPECIAL BLUE", style='TButton',
                               command=lambda: cambiar_tema_completo(root,  footer_label, info_label,
                                                                     caducidad_label, tree, 'blue'))
        btn_blue.pack(pady=10)


        btn_itft1 = ttk.Button(right_frame, text="  SKY BLUE  ", style='TButton',
                               command=lambda: cambiar_tema_completo(root, footer_label, info_label,
                                                                     caducidad_label, tree, 'itft1'))
        btn_itft1.pack(pady=10)

        btn_vainilla = ttk.Button(right_frame, text="   VAINILLA   ", style='TButton',
                               command=lambda: cambiar_tema_completo(root, footer_label, info_label,
                                                                     caducidad_label, tree, 'winxpblue'))
        btn_vainilla.pack(pady=10)

        return


# Definir la función para pedir un ID al usuario
def pedir_id(titulo, pregunta):
    # Mostrar un cuadro de diálogo para pedir una cadena de texto al usuario
    # 'titulo' es el título de la ventana del cuadro de diálogo
    # 'pregunta' es el mensaje que se muestra en el cuadro de diálogo
    return simpledialog.askstring(titulo, pregunta)

# Definir la función para pedir una cantidad al usuario
def pedir_cantidad(title, prompt):
    # Mostrar un cuadro de diálogo que pide un entero al usuario
    # 'title' es el título de la ventana del cuadro de diálogo
    # 'prompt' es el mensaje que se muestra en el cuadro de diálogo
    return simpledialog.askinteger(title, prompt)


def buscar_cliente_por_id(id_cliente):
    # Conecta a la base de datos
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Busca el cliente con el ID proporcionado
    cursor.execute("SELECT * FROM Cliente WHERE ID = ?", (id_cliente,))
    cliente = cursor.fetchone()

    # Cierra la conexión
    conn.close()

    return cliente


def buscar_producto_por_id(id_producto):
    # Conecta a la base de datos
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Busca el cliente con el ID proporcionado
    cursor.execute("SELECT * FROM Producto WHERE ID = ?", (id_producto,))
    cliente = cursor.fetchone()

    # Cierra la conexión
    conn.close()

    return cliente


def nuevo_albaran(tree):
    # Solicitar el ID del cliente al usuario y buscar el cliente en la base de datos
    id_cliente = pedir_id("Nuevo albarán", "Introduce el ID del cliente:")
    cliente = buscar_cliente_por_id(id_cliente)

    # Comprobar si el cliente existe
    if cliente:
        # Desempaquetar los datos del cliente
        id_cliente, nombre = cliente[0], cliente[1]

        # Insertar una nueva fila en el Treeview
        fila = tree.insert("", "end", values=(id_cliente, nombre, "", "", "", "", "", ""))

        # Bucle para permitir la adición de múltiples productos en el albarán
        while True:
            # Solicitar el ID del producto al usuario y buscar el producto en la base de datos
            id_producto = pedir_id("Nuevo albarán", "Introduce el ID del producto:")
            producto = buscar_producto_por_id(id_producto)

            # Comprobar si el producto existe
            if producto:
                # Desempaquetar los datos del producto
                id_producto, nombre_producto, precio_producto = producto[0], producto[1], producto[3]

                # Convertir el precio a float
                precio_producto = float(precio_producto)

                # Actualizar la fila del Treeview con los datos del producto
                tree.item(fila, values=(id_cliente, nombre, id_producto, nombre_producto, precio_producto, "", "", ""))

                # Solicitar la cantidad del producto al usuario
                cantidad = pedir_cantidad("Nuevo albarán", "Introduce la cantidad del producto:")
                cantidad = int(cantidad)

                # Verificar el stock disponible
                stock_disponible = obtener_stock_por_id(id_producto)

                if cantidad > stock_disponible:
                    # Mostrar un mensaje de advertencia si no hay suficiente stock
                    messagebox.showwarning("Stock insuficiente", f"Solo hay {stock_disponible} unidades disponibles.")
                    continue  # Reiniciar el bucle

                # Calcular y mostrar el total
                fecha = datetime.now().strftime("%Y-%m-%d")
                total = cantidad * precio_producto
                tree.item(fila, values=(
                id_cliente, nombre, id_producto, nombre_producto, precio_producto, cantidad, fecha, total))

                # Preguntar al usuario si desea añadir otro producto
                seguir = messagebox.askyesno("Continuar", "¿Quieres agregar otro producto?")

                if seguir:
                    fila = tree.insert("", "end", values=(id_cliente, nombre, "", "", "", "", "", ""))
                else:
                    break
            else:
                # Mostrar un mensaje si el producto no existe
                messagebox.showinfo("Producto no encontrado", "El producto no existe.")
    else:
        # Mostrar un mensaje si el cliente no existe
        messagebox.showinfo("Cliente no encontrado", "El cliente no existe.")


# Función que muestra un mensaje acerca de características futuras.
def coming_soon():
    messagebox.showinfo("Información", "¡Próximamente!",)

# Función que crea y guarda un producto en la base de datos.
def create_product(entries,right_frame):
    #clear_right_frame(right_frame)
    # Intenta recopilar datos. Si falta alguna clave, muestra un mensaje de error.
    try:
        nombre = entries["NUEVO PRODUCTO"].get()
        familia = entries["FAMILIA"].get()
        precio = entries["PRECIO"].get()
        iva = entries["IVA"].get()
        proveedor = entries["PROVEEDOR"].get()
        cantidad = entries["CANTIDAD"].get()
        caducidad = entries["CADUCIDAD"].get()
    except KeyError as e:
        messagebox.showerror("Error", f"Falta la entrada para {e}.")
        return

    # Instanciación del producto con los datos recopilados.
    producto = Producto(nombre, familia, precio, iva, proveedor, cantidad, caducidad)

    # Guardado del producto en la base de datos.
    database.guardar_producto(producto)

    # Formateo y presentación de la información del producto al usuario.
    info = f"""
    Nombre: {nombre}
    Familia: {familia}
    Precio: {precio}
    IVA: {iva}
    Proveedor: {proveedor}
    Cantidad: {cantidad}
    Caducidad: {caducidad}
    """
    messagebox.showinfo("Producto creado con éxito", info)

    # Limpieza de widgets en el frame derecho y eliminación del botón.
    clear_right_frame(right_frame)
    #btn.destroy()


def create_client(entries, right_frame):
    # Intenta recopilar datos. Si falta alguna clave, muestra un mensaje de error.
    try:
        nombre = entries["NUEVO CLIENTE"].get()
        cif = entries["CIF"].get()
        direccion = entries["DIRECCION"].get()
        localidad = entries["LOCALIDAD"].get()
        provincia = entries["PROVINCIA"].get()
        telefono = entries["TELEFONO"].get()
        email = entries["EMAIL"].get()
    except KeyError as e:
        # Muestra un mensaje de error si falta alguna entrada.
        messagebox.showerror("Error", f"Falta la entrada para {e}.")
        return

    # Instanciación del proveedor con los datos recopilados.
    cliente = Cliente(nombre, cif, direccion, localidad, provincia, telefono, email)

    # Guardado del proveedor en la base de datos.
    database.guardar_cliente(cliente)

    # Formateo y presentación de la información del proveedor al usuario.
    info = f"""
    Nombre: {nombre}
    CIF: {cif}
    Direccion: {direccion}
    Localidad: {localidad}
    Provincia: {provincia}
    Telefono: {telefono}
    E-mail: {email}
    """
    messagebox.showinfo("Cliente creado con éxito", info)

    # Limpieza de widgets en el frame derecho y eliminación del botón.
    clear_right_frame(right_frame)
    #btn.destroy()

# Función que crea y guarda un proveedor en la base de datos.
def create_proveedor(entries, right_frame):
    # Intenta recopilar datos. Si falta alguna clave, muestra un mensaje de error.
    try:
        nombre = entries["NUEVO PROVEEDOR"].get()
        cif = entries["CIF"].get()
        direccion = entries["DIRECCION"].get()
        localidad = entries["LOCALIDAD"].get()
        provincia = entries["PROVINCIA"].get()
        telefono = entries["TELEFONO"].get()
        email = entries["EMAIL"].get()
    except KeyError as e:
        messagebox.showerror("Error", f"Falta la entrada para {e}.")
        return

    # Instanciación del proveedor con los datos recopilados.
    proveedor = Proveedor(nombre, cif, direccion, localidad, provincia, telefono, email)

    # Guardado del proveedor en la base de datos.
    database.guardar_proveedor(proveedor)

    # Formateo y presentación de la información del proveedor al usuario.
    info = f"""
    Nombre: {nombre}
    CIF: {cif}
    Direccion: {direccion}
    Localidad: {localidad}
    Provincia: {provincia}
    Telefono: {telefono}
    E-mail: {email}
    """
    messagebox.showinfo("Proveedor creado con éxito", info)

    # Limpieza de widgets en el frame derecho y eliminación del botón.
    clear_right_frame(right_frame)
    #btn.destroy()


def create_albaran(entries, right_frame):
    conexion = conectar()
    cursor = conexion.cursor()


    AlbaranID = entries["ALBARAN ID"].get()
    ClienteID = entries["CLIENTE ID"].get()
    ProductoID = entries["PRODUCTO ID"].get()
    ProveedorID = entries["PROVEEDOR ID"].get()
    Cantidad = entries["CANTIDAD"].get()
    Fecha = entries["FECHA"].get()

    nuevo_albaran = (AlbaranID, ClienteID, ProductoID, ProveedorID, Cantidad, Fecha)

    try:
        cursor.execute("INSERT INTO Albaran VALUES (?, ?, ?, ?, ?, ?)", nuevo_albaran)
        conexion.commit()
        messagebox.showinfo("Exito", "Albarán creado con éxito!")



    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")



def show_context_menu(event, tree, tipo_elemento):
    if tree is None:
        tree = event.widget

    print("Evento de clic derecho registrado.")  # Para depuración

    selected_item = tree.selection()

    if not selected_item:  # Verifica si hay un elemento seleccionado
        print("Ningún elemento seleccionado.")  # Para depuración
        return

    selected_item = selected_item[0]  # Tomamos el primer elemento en caso de múltiples selecciones

    context_menu = Menu(tree, tearoff=0)

    # Añadir opciones de menú según el tipo de elemento
    if tipo_elemento == 'cliente':
        context_menu.add_command(label="Editar", command=lambda: coming_soon())
        context_menu.add_command(label="Eliminar", command=lambda: eliminar_fila(selected_item, tree, 'cliente', mostrar_mensaje))
    elif tipo_elemento == 'producto':
        context_menu.add_command(label="Editar", command=lambda: coming_soon())
        context_menu.add_command(label="Eliminar", command=lambda: eliminar_fila(selected_item, tree, 'producto', mostrar_mensaje))
    elif tipo_elemento == 'proveedor':
        context_menu.add_command(label="Editar", command=lambda: coming_soon())
        context_menu.add_command(label="Eliminar", command=lambda: eliminar_fila(selected_item, tree, 'proveedor', mostrar_mensaje))
    elif tipo_elemento == 'albaran':
        id_albaran = tree.item(selected_item, 'values')[0]
        id_cliente = tree.item(selected_item, 'values')[2]
        fecha = tree.item(selected_item, 'values')[1]
        print("VALUES 0",id_albaran)
        print("VALUES 1", id_cliente)
        print("VALUES 2", fecha)


        print(f"Debug en interfaz.py: id_cliente = {id_cliente}, tipo = {type(id_cliente)}")

        total = calcular_total_con_iva(id_albaran)


        context_menu.add_command(label="Editar", command=lambda: coming_soon())
        context_menu.add_command(label="Eliminar", command=lambda: eliminar_fila(selected_item, tree, 'albaran'))
        context_menu.add_command(label="Facturar", command=lambda: crear_factura_desde_albaran(id_albaran, id_cliente, fecha, total))
        print("Item", selected_item, "seleccionado con ratón.")
    else:
        print(f"Tipo de elemento desconocido: {tipo_elemento}")
        return

    context_menu.post(event.x_root, event.y_root)
    print("Menú contextual mostrado.")


def confirmar_eliminar(selected_item, tree):
    answer = messagebox.askyesno("Confirmación", "¿Estás seguro de que quieres eliminar este cliente?")
    if answer:
        eliminar_fila(selected_item, tree)

# Función para editar una fila
def editar_fila(selected_item):
    # Codigo para la logica
    print(f"Editar fila {selected_item}")



# Función para conectar a la base de datos SQLite
def conectar():
    try:
        # Intentamos establecer la conexión y devolver el objeto de conexión
        return sqlite3.connect('database.db')
    except sqlite3.Error as e:
        # Si hay un error durante la conexión, mostramos un mensaje de error
        messagebox.showerror("Error de conexión", f"Ocurrió un error al conectar con la base de datos: {e}")
        # Devolvemos None para indicar que la conexión no fue exitosa
        return None


# Función para obtener el stock de un producto dado su ID
def obtener_stock_por_id(id_producto):
    try:
        # Usamos la función 'conectar' para obtener la conexión a la base de datos
        conexion = conectar()
        cursor = conexion.cursor()

        # Ejecutamos una consulta SQL para obtener la cantidad en stock del producto con el ID dado
        cursor.execute("SELECT Cantidad FROM Producto WHERE ID = ?", (id_producto,))

        # Obtenemos el resultado de la consulta
        resultado = cursor.fetchone()
    except sqlite3.Error as e:
        # Si algo va mal con la consulta o la conexión, mostramos un mensaje de error
        messagebox.showerror("Error en la base de datos", f"Ocurrió un error: {e}")
        return None  # Devolvemos None para indicar que algo fue mal
    finally:
        # Cerramos la conexión a la base de datos, pase lo que pase
        conexion.close()

    # Si obtuvimos un resultado, devolvemos la cantidad en stock
    if resultado:
        return resultado[0]
    else:
        # Si no hay resultado (por ejemplo, si el ID del producto no existe), devolvemos None
        return None



# Función para finalizar el albarán, añadirlo a la base de datos y actualizar el stock.
def finalizar_albaran(tree):
    # Obtiene todos los items en el árbol (Treeview)
    items = tree.get_children()

    # Si no hay items, muestra una advertencia
    if not items:
        messagebox.showwarning("Advertencia", "El albarán está vacío")
        return

    # Inicia una conexión con la base de datos
    conexion = conectar()
    cursor = conexion.cursor()

    # Obtiene la fecha actual
    fecha = datetime.now().strftime('%d/%m/%Y')

    # Obtiene el ID del cliente del primer item en el árbol
    cliente_id = tree.item(items[0], 'values')[0]

    # Calcula el total del albarán sumando los totales de cada item
    total_albaran = sum(float(tree.item(item, 'values')[7]) for item in items)

    # Inserta el nuevo albarán en la tabla Albaran
    cursor.execute("INSERT INTO Albaran (Fecha, ClienteID, Total) VALUES (?, ?, ?)",
                   (fecha, cliente_id, total_albaran))
    conexion.commit()

    # Obtiene el último ID insertado en la tabla Albaran
    albaran_id = cursor.lastrowid


    # Itera por cada item/producto en el árbol
    for item in items:
        valores = tree.item(item, 'values')
        producto_id = int(valores[2])
        cantidad_vendida = int(valores[5])

        # Comprueba el stock actual del producto
        stock_actual = obtener_stock_por_id(producto_id)

        # Si no se pudo obtener el stock, muestra una advertencia
        if stock_actual is None:
            messagebox.showwarning("Advertencia", f"No se pudo obtener el stock del producto {producto_id}")
            return

        # Si no hay suficiente stock, muestra una advertencia
        if stock_actual < cantidad_vendida:
            messagebox.showwarning("Advertencia",
                                   f"No hay suficiente stock del producto {producto_id}. Stock disponible: {stock_actual}")
            return

        # Actualiza el stock del producto
        nuevo_stock = stock_actual - cantidad_vendida
        cursor.execute("UPDATE Producto SET Cantidad = ? WHERE ID = ?", (nuevo_stock, producto_id))

        # Inserta el detalle del albarán en la tabla DetalleAlbaran
        cursor.execute(
            "INSERT INTO DetalleAlbaran (AlbaranID, ClienteID, ProductoID, Producto, Precio, Cantidad, Fecha, Total) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (albaran_id, cliente_id, producto_id, valores[3], valores[4], cantidad_vendida, fecha, valores[7]))

    # Guarda los cambios en la base de datos
    conexion.commit()


    # Cierra la conexión a la base de datos
    conexion.close()

    # Limpia el árbol (Treeview), eliminando todos los items
    tree.delete(*tree.get_children())

    # Muestra un mensaje de éxito
    messagebox.showinfo("Éxito", "Albarán finalizado y guardado en la base de datos")
    actualizar_stock(producto_id,nuevo_stock)




# Función para actualizar el stock de un producto dado su ID
def actualizar_stock(producto_id, nuevo_stock):
    # Usamos la función 'conectar' para obtener la conexión a la base de datos
    conexion = conectar()
    cursor = conexion.cursor()
    print("Llegando al UPDATE")

    cursor.execute("UPDATE Producto SET Cantidad = ? WHERE ID = ?", (nuevo_stock, producto_id))

    print("UPDATE LEIDO .....???")

    # Confirmamos los cambios en la base de datos
    conexion.commit()

    # Devolvemos True para indicar que la actualización fue exitosa

    conexion.close()




# Función para consultar el detalle de un albarán específico por su ID.
def consulta_detalle_albaran(albaran_id):
    # Usamos la función conectar() para obtener la conexión
    conn = conectar()
    cursor = conn.cursor()

    # El resto del código sigue igual
    cursor.execute("SELECT * FROM DetalleAlbaran WHERE AlbaranID=?", (albaran_id,))
    registros = cursor.fetchall()
    conn.close()

    lista_diccionarios = []
    for registro in registros:
        lista_diccionarios.append({
            "DetalleID": registro[0],
            "AlbaranID": registro[1],
            "ClienteID": registro[2],
            "ProductoID": registro[3],
            "Producto": registro[4],
            "Precio": registro[5],
            "Cantidad": registro[6],
            "Fecha": registro[7],
            "Total": registro[8]
        })

    return lista_diccionarios


def mostrar_mensaje(mensaje):
    ventana = tk.Tk()  # Crea una nueva ventana Tkinter
    ventana.withdraw()  # Oculta la ventana principal de Tkinter

    # Muestra un cuadro de mensaje informativo con el mensaje proporcionado
    messagebox.showinfo("Información", mensaje)

    ventana.destroy()  # Destruye la ventana para liberar recursos


def imprimir_albaran():
    try:
        # Pide al usuario el ID del albarán que quiere imprimir
        albaran_id = simpledialog.askstring("Input", "¿Qué Albarán quieres imprimir? Introduce el AlbaranID:")

        lista_de_diccionarios = []

        # Verifica si la lista tiene elementos y muestra la fecha del albarán
        if len(lista_de_diccionarios) > 0:
            fecha_albaran = lista_de_diccionarios[0]['Total']
            mostrar_mensaje(f"La fecha del albarán es: {fecha_albaran}")
        else:
            pass  # No hacer nada si la lista está vacía

        # Verifica si el ID del albarán es válido
        if albaran_id is not None and albaran_id.strip() != "":

            # Obtiene los detalles del albarán
            detalles = consulta_detalle_albaran(albaran_id)

            # Verifica si se encontraron detalles
            if detalles:
                # Crea listas para los productos, precios, fechas, totales y cantidades
                lista_productos = [detalle['Producto'] for detalle in detalles]
                lista_precios = [detalle['Precio'] for detalle in detalles]
                fecha_albaran = [detalle['Total'] for detalle in detalles]
                lista_total = [detalle['Cantidad'] for detalle in detalles]
                lista_cantidad = detalles[0]['Fecha']  # Suponemos que todas las fechas son iguales

                # Genera un PDF con los detalles
                generar_pdf(albaran_id, lista_productos, lista_precios, lista_cantidad, lista_total, fecha_albaran)

                # Muestra mensaje de éxito
                mostrar_mensaje("El PDF se ha generado correctamente.")
            else:
                # Muestra mensaje si no se encontraron detalles
                mostrar_mensaje("No se encontraron detalles para el albarán.")
        else:
            # Muestra mensaje si se canceló la operación o la entrada es inválida
            mostrar_mensaje("Operación cancelada o entrada inválida.")

    except Exception as e:  # Captura cualquier excepción
        # Muestra un mensaje con detalles del error
        mostrar_mensaje(f"Ups, algo salió mal. Detalles del error: {e}")



# Generamos el pdf de albaran
def generar_pdf(albaran_id, lista_productos, lista_precios, fecha_albaran, lista_cantidad, lista_total):
    directory = ".pdf_albaranes"

    if not os.path.exists(directory):
        os.makedirs(directory)

    pdf_name = f"{directory}/Albaran_{albaran_id}.pdf"
    pdf = SimpleDocTemplate(pdf_name, pagesize=A4)
    # el resto de tu código


    # Estilos de Paragraph
    styles = getSampleStyleSheet()

    # Añadir la imagen al principio (membrete o logo)
    ruta_imagen = "./images/membrete.png"
    img = Image(ruta_imagen, width=600, height=200)

    # Texto a la izquierda con Albarán ID y Fecha
    texto_albaran_id = Paragraph(f"<b>Albarán ID:</b> {str(albaran_id)}", styles["BodyText"])
    texto_fecha_albaran = Paragraph(f"<b>Fecha del Albarán:</b> {str(fecha_albaran)}", styles["BodyText"])

    # Espacio entre los Paragraph y la tabla
    espacio = Spacer(1, 12)

    # Nuevo encabezado de tabla
    data = [["Producto", "Precio", "Cantidad", "Total"]]

    # Variable para almacenar el subtotal
    subtotal = 0

    for i in range(len(lista_productos)):
        producto_id = Paragraph(f"<para align=center>{str(lista_productos[i])}</para>", styles["BodyText"])
        precio = Paragraph(f"<para align=center>{str(lista_precios[i])}</para>", styles["BodyText"])
        cantidad = Paragraph(f"<para align=center>{str(lista_cantidad[i])}</para>", styles["BodyText"])
        total = Paragraph(f"<para align=center>{str(lista_total[i])}</para>", styles["BodyText"])

        # Acumulamos en el subtotal
        subtotal += int(lista_total[i])

        data.append([producto_id, precio, cantidad, total])

    # Añadir la fila del subtotal
    subtotal_label = Paragraph("<para align=center>Subtotal</para>", styles["BodyText"])
    subtotal_value = Paragraph(f"<para align=center>{str(subtotal)}</para>", styles["BodyText"])
    data.append(["", "", subtotal_label, subtotal_value])

    table = Table(data)


    # Calculamos el ancho máximo de cada columna y lo aplicamos a la tabla
    for i in range(len(data[0])):
        max_ancho = calcular_ancho_maximo_columna(data, i)
        table._argW[i] = max_ancho  # Ajustamos el ancho de la columna

    # Aplicar estilos a la tabla
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey), # Color fondo cabecera
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke), #Color texto cabecera
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Esta línea centra el contenido
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), # Tipo de Fuente
        ('FONTSIZE', (0, 0), (-1, 0), 14), # Tamaño de la fuente
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12), #configurar el padding inferior de la tabla a 12 unidades
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige), #Color fondo lista productos
        ('BACKGROUND', (0, -1), (-1, -1), colors.orange),  # Color de la fila del subtotal
        ('GRID', (0, 0), (-1, -1), 1, colors.black) #Diseño de la cuadricula
    ]))

    # Agregar todos los elementos al PDF
    elementos = [img, texto_albaran_id, texto_fecha_albaran, espacio, table]
    pdf.build(elementos)

    # Abrir el PDF automáticamente
    abrir_pdf_con_adobe(pdf_name)

# Funcion para seleccionar el albaran que queremos imprimir en factura
def imprimir_factura():
    try:
        # Pide el AlbaranID al usuario
        albaran_id = simpledialog.askstring("Input", "¿Qué Albarán quieres facturar? Introduce el AlbaranID:")
        lista_de_diccionarios = []

        # Comprueba si hay detalles del albarán en la lista de diccionarios
        if len(lista_de_diccionarios) > 0:
            fecha_albaran = lista_de_diccionarios[0]['Total']
            mostrar_mensaje(f"La fecha del albarán es: {fecha_albaran}")
        else:
            pass

        # Si el albaran_id existe y no es una cadena vacía
        if albaran_id is not None and albaran_id.strip() != "":
            detalles = consulta_detalle_albaran(albaran_id)  # Obtiene los detalles del albarán

            # Si se encuentran detalles
            if detalles:
                # Recopila la información de los detalles en listas
                lista_productos = [detalle['Producto'] for detalle in detalles]
                lista_precios = [detalle['Precio'] for detalle in detalles]
                fecha_albaran = [detalle['Total'] for detalle in detalles]
                lista_total = [detalle['Cantidad'] for detalle in detalles]
                lista_cantidad = detalles[0]['Fecha']  # Asume que todas las fechas son iguales

                # Llama a la función para generar el PDF de la factura
                generar_pdf_factura(albaran_id, lista_productos, lista_precios, lista_cantidad, lista_total, fecha_albaran)
                mostrar_mensaje("La factura se ha generado correctamente.")
            else:
                mostrar_mensaje("No se encontraron detalles para el albarán.")
        else:
            mostrar_mensaje("Operación cancelada o entrada inválida.")
    except Exception as e:
        # Si algo sale mal, muestra el mensaje de error
        mostrar_mensaje(f"Ups, algo salió mal. Detalles del error: {e}")


def calcular_ancho_maximo_columna(data, columna):
    max_len = 0  # Variable para almacenar la longitud máxima del texto en la columna
    for fila in data:  # Iteramos a través de cada fila en la tabla (data)
        texto = fila[columna]  # Obtenemos el texto de la columna en la fila actual
        # Si el objeto tiene el método 'getPlainText', lo usamos para obtener el texto plano
        if hasattr(texto, 'getPlainText'):
            texto = texto.getPlainText()
        # Actualizamos max_len si el texto actual es más largo
        max_len = max(max_len, len(texto))
    # Convertimos la longitud del texto a unidades de ancho de columna (1 carácter = 10 unidades)
    return max_len * 10


# Funcion para imprimir en pdf la factura
def generar_pdf_factura(albaran_id, lista_productos, lista_precios, fecha_albaran, lista_cantidad, lista_total):
    directory = ".pdf_facturas"

    if not os.path.exists(directory):
        os.makedirs(directory)

    pdf_name = f"{directory}/Factura_{albaran_id}.pdf"
    pdf = SimpleDocTemplate(pdf_name, pagesize=A4)
    # Estilos de Paragraph
    styles = getSampleStyleSheet()

    # Añadir la imagen al principio (membrete o logo)
    ruta_imagen = "./images/membrete_factura.png"
    img = Image(ruta_imagen, width=600, height=200)

    # Texto a la izquierda con Albarán ID y Fecha
    texto_factura_id = Paragraph(f"<b>Factura ID:</b> {str(albaran_id)}", styles["BodyText"])
    texto_fecha_factura = Paragraph(f"<b>Fecha de Factura:</b> {str(fecha_albaran)}", styles["BodyText"])

    # Espacio entre los Paragraph y la tabla
    espacio = Spacer(1, 12)

    # Nuevo encabezado de tabla
    data = [["Producto", "Precio", "Cantidad", "Total"]]

    # Variable para almacenar el subtotal
    subtotal = 0

    for i in range(len(lista_productos)):
        producto_id = Paragraph(f"<para align=center>{str(lista_productos[i])}</para>", styles["BodyText"])
        precio = Paragraph(f"<para align=center>{str(lista_precios[i])}</para>", styles["BodyText"])
        cantidad = Paragraph(f"<para align=center>{str(lista_cantidad[i])}</para>", styles["BodyText"])
        total = Paragraph(f"<para align=center>{str(lista_total[i])}</para>", styles["BodyText"])

        # Acumulamos en el subtotal
        subtotal += int(lista_total[i])

        data.append([producto_id, precio, cantidad, total])

    # Cálculo del IVA
    importe_iva = round(subtotal * 21 / 100, 2)

    # Añadir la fila del IVA
    iva_label = Paragraph("<para align=center>IVA (21%)</para>", styles["BodyText"])
    iva_value = Paragraph(f"<para align=center>{str(importe_iva)}</para>", styles["BodyText"])
    data.append(["", "", iva_label, iva_value])

    # Añadir la fila del total con IVA
    total_con_iva = round(subtotal + importe_iva, 2)
    total_label = Paragraph("<para align=center>Total con IVA</para>", styles["BodyText"])
    total_value = Paragraph(f"<para align=center>{str(total_con_iva)}</para>", styles["BodyText"])
    data.append(["", "", total_label, total_value])


    table = Table(data)

    # Calculamos el ancho máximo de cada columna y lo aplicamos a la tabla
    for i in range(len(data[0])):
        max_ancho = calcular_ancho_maximo_columna(data, i)
        table._argW[i] = max_ancho  # Ajustamos el ancho de la columna

    # Aplicar estilos a la tabla
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Esta línea debería centrar todo el contenido
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.aliceblue),
        ('BACKGROUND', (0, -1), (-1, -1), colors.deepskyblue),  # Color de la fila del subtotal
        ('GRID', (0, 0), (-1, -1), 1, colors.goldenrod)
    ]))

    # Agregar todos los elementos al PDF
    elementos = [img, texto_factura_id, texto_fecha_factura, espacio, table]
    pdf.build(elementos)

    # Abrir el PDF automáticamente
    abrir_pdf_con_adobe(pdf_name)


# Funcion para que se abra automaticamente el pdf con adobe reader o en su defecto con adobe acrobat
def abrir_pdf_con_adobe(ruta_pdf):
    try:
        # Primera ruta al ejecutable de Adobe Reader
        adobe_executable_1 = "C:\\Program Files (x86)\\Adobe\\Acrobat Reader DC\\Reader\\AcroRd32.exe"

        # Intentar abrir el archivo PDF usando la primera ruta de Adobe Reader
        subprocess.Popen([adobe_executable_1, ruta_pdf])

    except Exception as e:
        print(f"Ocurrió un error con la primera ruta de Adobe, intentando con la segunda: {e}")

        try:
            # Segunda ruta al ejecutable de Adobe Reader
            adobe_executable_2 = "C:\\Program Files\\Adobe\\Acrobat DC\\Acrobat\\Acrobat.exe"

            # Intentar abrir el archivo PDF usando la segunda ruta de Adobe Reader
            subprocess.Popen([adobe_executable_2, ruta_pdf])

        except Exception as e2:
            print(f"Ocurrió un error con la segunda ruta de Adobe, no se pudo abrir el PDF: {e2}")



# Función que elimina todos los widgets del right_frame.
def clear_right_frame(right_frame):
    for widget in right_frame.winfo_children():
        widget.destroy()




if __name__ == "__main__":
    init_gui()

