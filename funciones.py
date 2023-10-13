import sqlite3
from database import conectar
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from datetime import datetime


def actualizar_producto():
    messagebox.showinfo("Información", "Próximamente...")


# Función para actualizar los datos de un producto en la base de datos
def actualizar_producto_proximamente(producto_id, nombre, familia, precio, iva, proveedor, cantidad, caducidad):

    conexion = conectar() # Establecer una conexión a la base de datos
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL para actualizar los valores del producto
    cursor.execute('''UPDATE Producto SET 
                      Nombre = ?, 
                      Familia = ?, 
                      Precio = ?, 
                      IVA = ?, 
                      Proveedor = ?, 
                      Cantidad = ?, 
                      Caducidad = ? 
                      WHERE ID = ?''',
                   (producto_id,nombre, familia, precio, iva, proveedor, cantidad, caducidad))

    conexion.commit() # Confirmar los cambios en la base de datos
    conexion.close()# Cerrar la conexión a la base de datos



def abrir_cuadro_dialogo_eliminar():
    # Utiliza la variable global 'root' para acceder a la ventana principal
    global root

    # Crea una ventana secundaria (cuadro de diálogo)
    dialog = tk.Toplevel(root)
    dialog.title("Eliminar Producto")

    # Crea una etiqueta y un cuadro de entrada para ingresar el ID del producto
    tk.Label(dialog, text="Ingresa el ID del producto a eliminar:").pack()
    id_producto = tk.Entry(dialog)
    id_producto.pack()

    # Función para eliminar el producto
    def confirmar_eliminar():
        try:
            id_producto_int = int(id_producto.get())
            eliminar_producto(id_producto_int)
            dialog.destroy()  # Cierra el cuadro de diálogo después de eliminar
        except ValueError:
            # Manejo de error si no se ingresa un número válido
            tk.messagebox.showerror("Error", "Ingresa un número válido para el ID del producto.")

    # Crea un botón "Aceptar" para confirmar la eliminación
    tk.Button(dialog, text="Aceptar", command=confirmar_eliminar).pack()


# Función para agregar un nuevo cliente a la base de datos
def agregar_cliente(nombre, cif, direccion, localidad, provincia, telefono, email):
    # Establecer una conexión a la base de datos
    conexion = conectar()
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL para insertar los datos del nuevo cliente en la tabla 'Cliente'
    cursor.execute(
        "INSERT INTO Cliente (Nombre, CIF, Direccion, Localidad, Provincia, Telefono, Email) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (nombre, cif, direccion, localidad, provincia, telefono, email))

    # Confirmar los cambios en la base de datos
    conexion.commit()

    # Cerrar la conexión a la base de datos
    conexion.close()


# Función para obtener los datos de un cliente de la base de datos
def obtener_cliente(conn, cliente_id):
    # Crear un cursor para ejecutar consultas SQL en la conexión proporcionada
    cursor = conn.cursor()

    # Ejecutar una consulta SQL para seleccionar el nombre, familia y dirección del cliente con el ID especificado
    cursor.execute("SELECT nombre, familia, direccion FROM cliente WHERE id=?", (cliente_id,))

    # Obtener la primera fila (si existe) que contiene los datos del cliente
    cliente = cursor.fetchone()

    # Cerrar el cursor
    cursor.close()

    # Retornar los datos del cliente (puede ser None si no se encontró el cliente)
    return cliente


# Función para actualizar los datos de un cliente en la base de datos
def actualizar_cliente(id, nombre, cif, direccion, localidad, provincia, telefono, email):
    # Establecer una conexión a la base de datos
    conexion = conectar()
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL para actualizar los valores del cliente
    cursor.execute('''UPDATE Cliente SET 
                      Nombre = ?, 
                      CIF = ?, 
                      Direccion = ?, 
                      Localidad = ?, 
                      Provincia = ?, 
                      Telefono = ?, 
                      Email = ? 
                      WHERE ID = ?''',
                   (nombre, cif, direccion, localidad, provincia, telefono, email, id))

    # Confirmar los cambios en la base de datos
    conexion.commit()

    # Cerrar la conexión a la base de datos
    conexion.close()


# Función para eliminar un producto de la base de datos

def eliminar_producto(producto_id):
    try:
        conexion = conectar()  # Suponiendo que tienes una función conectar() que abre una conexión a tu base de datos
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM Producto WHERE ID=?", (producto_id,))

        conexion.commit()
        conexion.close()

        return True  # Devuelve True si la eliminación fue exitosa
    except Exception as e:
        print(f"Ocurrió un error al eliminar el producto: {e}")
        return False  # Devuelve False si algo salió mal





def eliminar_cliente(cliente_id):
    try:
        conexion = conectar()  # Suponiendo que tienes una función conectar() que abre una conexión a tu base de datos
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM Cliente WHERE ID=?", (cliente_id,))

        conexion.commit()
        conexion.close()

        return True  # Devuelve True si la eliminación fue exitosa
    except Exception as e:
        print(f"Ocurrió un error al eliminar el cliente: {e}")
        return False  # Devuelve False si algo salió mal



def eliminar_proveedor(proveedor_id):
    print(f"Intentando eliminar el proveedor con ID: {proveedor_id} de la base de datos...")

    try:
        conexion = conectar()  # Conectar a la base de datos
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM Proveedor WHERE ID=?", (proveedor_id,))

        conexion.commit()
        conexion.close()

        return True  # Devuelve True si la eliminación fue exitosa
    except Exception as e:
        print(f"Ocurrió un error al eliminar el proveedor: {e}")
        print("Tipo de excepción:", type(e))
        return False  # Devuelve False si algo salió mal



def eliminar_albaran(albaran_id):
    try:
        conexion = conectar()  # Suponiendo que tienes una función conectar() que abre una conexión a tu base de datos
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM Albaran WHERE AlbaranID=?", (albaran_id,))

        conexion.commit()
        conexion.close()

        return True  # Devuelve True si la eliminación fue exitosa
    except Exception as e:
        print(f"Ocurrió un error al eliminar el albarán: {e}")
        return False  # Devuelve False si algo salió mal





def eliminar_fila(selected_item, tree, tipo_elemento, mostrar_mensaje):
    print(f"El selected_item es: {selected_item}")
    confirmacion = messagebox.askyesno("Confirmación", f"¿Estás seguro de que quieres eliminar este {tipo_elemento}?")
    if confirmacion:
        elemento = tree.item(selected_item, "values")
        elemento_id = elemento[0]  # Asume que el ID es el primer valor en la tupla
        print(f"El elemento_id es: {elemento_id}")
        print(f"Intentando eliminar el elemento con ID: {elemento_id} del Treeview...")  # Para depuración

        # Dependiendo del tipo de elemento, llamamos a diferentes funciones de la base de datos
        if tipo_elemento == 'cliente':
            resultado = eliminar_cliente(elemento_id)
        elif tipo_elemento == 'producto':
            resultado = eliminar_producto(elemento_id)
        elif tipo_elemento == 'proveedor':
            resultado = eliminar_proveedor(elemento_id)
        elif tipo_elemento == 'albaran':
            resultado = eliminar_albaran(elemento_id)
        else:
            print(f"Tipo de elemento desconocido: {tipo_elemento}")
            return

        if resultado:
            tree.delete(selected_item)
            tree.update_idletasks()  # Intenta actualizar explícitamente el Treeview
            print(f"{tipo_elemento.capitalize()} con ID {elemento_id} eliminado exitosamente.")
            mostrar_mensaje(f"{tipo_elemento.capitalize()} eliminado exitosamente.")
        else:
            print(f"Error al eliminar el {tipo_elemento} con ID {elemento_id}.")
            mostrar_mensaje(f"Error al eliminar el {tipo_elemento}.")
    else:
        mostrar_mensaje("Eliminación cancelada.")


# Función para obtener los datos de un producto de la base de datos
def obtener_producto(conn, producto_id):
    messagebox.showinfo("Información", "Próximamente...")

    # Crear un cursor para ejecutar consultas SQL en la conexión proporcionada
    cursor = conn.cursor()

    # Ejecutar una consulta SQL para seleccionar el nombre y el precio del producto con el ID especificado
    cursor.execute("SELECT nombre, precio FROM producto WHERE id=?", (producto_id,))

    # Obtener la primera fila (si existe) que contiene los datos del producto
    producto = cursor.fetchone()

    # Cerrar el cursor
    cursor.close()

    # Retornar los datos del producto (puede ser None si no se encontró el producto)
    return producto


# Función para generar un albarán con los productos seleccionados para un cliente
def generar_albaran(conn, cliente_id, productos):
    # Obtener los datos del cliente utilizando la función obtener_cliente
    cliente = obtener_cliente(conn, cliente_id)

    # Imprimir los datos del cliente
    print(f"Nombre: {cliente[0]}\nFamilia: {cliente[1]}\nDireccion: {cliente[2]}")

    # Inicializar el total en 0
    total = 0

    # Iterar a través de los productos y cantidades proporcionados
    for producto_id, cantidad in productos.items():
        # Obtener los datos del producto utilizando la función obtener_producto
        producto = obtener_producto(conn, producto_id)

        # Calcular el subtotal (precio del producto multiplicado por la cantidad)
        subtotal = producto[1] * cantidad

        # Imprimir los detalles del producto en el albarán
        print(f"{producto[0]} - Precio: {producto[1]} - Cantidad: {cantidad} - Subtotal: {subtotal}")

        # Sumar el subtotal al total
        total += subtotal

    # Imprimir el total del albarán
    print(f"Total: {total}")


# Función para actualizar los datos de un proveedor en la base de datos
def actualizar_proveedor(id, nombre, cif, direccion, localidad, provincia, telefono, email):
    # Establecer una conexión a la base de datos
    conexion = conectar()
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL para actualizar los datos del proveedor con el ID especificado
    cursor.execute('''UPDATE Proveedor SET 
                      Nombre = ?, 
                      CIF = ?, 
                      Direccion = ?, 
                      Localidad = ?, 
                      Provincia = ?, 
                      Telefono = ?, 
                      Email = ? 
                      WHERE ID = ?''',
                   (nombre, cif, direccion, localidad, provincia, telefono, email, id))

    # Confirmar los cambios en la base de datos
    conexion.commit()

    # Cerrar la conexión a la base de datos
    conexion.close()



# Función para agregar una nueva factura a la base de datos
def agregar_factura(cliente_id, nombre, cif, fecha, producto, cantidad, iva, descuento, total):
    # Establecer una conexión a la base de datos
    conexion = conectar()
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL para insertar los datos de la factura
    cursor.execute('''INSERT INTO Factura (ClienteID, Nombre, CIF, Fecha, Producto, Cantidad, Iva, Descuento, Total)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (cliente_id, nombre, cif, fecha, producto, cantidad, iva, descuento, total))

    # Confirmar los cambios en la base de datos
    conexion.commit()

    # Cerrar la conexión a la base de datos
    conexion.close()

# Función para obtener todas las facturas de la base de datos
def obtener_facturas():
    # Establecer una conexión a la base de datos
    conexion = conectar()
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL para seleccionar todas las facturas
    cursor.execute("SELECT * FROM Factura")

    # Obtener todas las filas (facturas) resultantes de la consulta
    facturas = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    conexion.close()

    # Retornar la lista de facturas
    return facturas

# Función para obtener una factura específica por su ID
def obtener_factura_por_id(id):
    # Establecer una conexión a la base de datos
    conexion = conectar()
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL para seleccionar la factura con el ID proporcionado
    cursor.execute("SELECT * FROM Factura WHERE ID = ?", (id,))

    # Obtener la primera fila (factura) resultante de la consulta (debería ser única por el ID)
    factura = cursor.fetchone()

    # Cerrar la conexión a la base de datos
    conexion.close()

    # Retornar la factura encontrada (o None si no se encuentra)
    return factura

# Función para actualizar una factura existente
def actualizar_factura(id, cliente_id, nombre, cif, fecha, producto, cantidad, iva, descuento, total):
    # Establecer una conexión a la base de datos
    conexion = conectar()
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL para actualizar la factura con el ID proporcionado
    cursor.execute('''UPDATE Factura SET 
                      ClienteID = ?, 
                      Nombre = ?, 
                      CIF = ?, 
                      Fecha = ?, 
                      Producto = ?, 
                      Cantidad = ?, 
                      Iva = ?, 
                      Descuento = ?, 
                      Total = ? 
                      WHERE ID = ?''',
                   (cliente_id, nombre, cif, fecha, producto, cantidad, iva, descuento, total, id))

    # Confirmar los cambios en la base de datos
    conexion.commit()

    # Cerrar la conexión a la base de datos
    conexion.close()



# Función para eliminar una factura por su ID
def eliminar_factura(id):
    # Establecer una conexión a la base de datos
    conexion = conectar()
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL para eliminar la factura con el ID proporcionado
    cursor.execute("DELETE FROM Factura WHERE ID = ?", (id,))

    # Confirmar los cambios en la base de datos
    conexion.commit()

    # Cerrar la conexión a la base de datos
    conexion.close()

# Función para agregar un nuevo albarán a la base de datos
def agregar_albaran(id_proveedor, id_cliente, fecha, producto, cantidad, iva, descuento, total_albaran):
    # Establecer una conexión a la base de datos
    conexion = conectar()
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL para insertar un nuevo albarán con los datos proporcionados
    cursor.execute('''INSERT INTO Albaran (id_proveedor, id_cliente, fecha, producto, cantidad, iva, descuento, total_albaran)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                   (id_proveedor, id_cliente, fecha, producto, cantidad, iva, descuento, total_albaran))

    # Confirmar los cambios en la base de datos
    conexion.commit()

    # Cerrar la conexión a la base de datos
    conexion.close()

# Función para obtener todos los albaranes de la base de datos
'''Esta función permite obtener todos los albaranes almacenados en la base de datos. 
Cada albarán se devuelve como una tupla con sus respectivos datos.'''
def obtener_albaranes():
    # Establecer una conexión a la base de datos
    conexion = conectar()
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL para seleccionar todos los albaranes
    cursor.execute("SELECT * FROM Albaran")

    # Obtener todos los albaranes como una lista de tuplas
    albaranes = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    conexion.close()

    # Devolver la lista de albaranes
    return albaranes

# Función para obtener un albarán específico por su ID
def obtener_albaran_por_id(id):
    # Establecer una conexión a la base de datos
    conexion = conectar()
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL para seleccionar un albarán por su ID
    cursor.execute("SELECT * FROM Albaran WHERE ID = ?", (id,))

    # Obtener el albarán como una tupla
    albaran = cursor.fetchone()

    # Cerrar la conexión a la base de datos
    conexion.close()

    # Devolver el albarán encontrado o None si no se encuentra
    return albaran

# Función para actualizar un albarán específico por su ID
def actualizar_albaran(id, cliente_id, descripcion, fecha, producto, cantidad, iva, descuento, total):
    # Establecer una conexión a la base de datos
    conexion = conectar()
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL para actualizar los datos del albarán por su ID
    cursor.execute('''UPDATE Albaran SET 
                      ClienteID = ?, 
                      Descripcion = ?, 
                      Fecha = ?, 
                      Producto = ?, 
                      Cantidad = ?, 
                      Iva = ?, 
                      Descuento = ?, 
                      Total = ? 
                      WHERE ID = ?''',
                   (cliente_id, descripcion, fecha, producto, cantidad, iva, descuento, total, id))

    # Confirmar los cambios en la base de datos
    conexion.commit()

    # Cerrar la conexión a la base de datos
    conexion.close()

def obtener_stock_total():
    # Establecer una conexión a la base de datos
    conexion = conectar()
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL para obtener la suma de la cantidad de todos los productos
    cursor.execute("SELECT SUM(Cantidad) FROM Producto")

    # Obtener el resultado de la consulta
    stock_total = cursor.fetchone()[0]

    # Cerrar la conexión a la base de datos
    conexion.close()

    # Verificar si hay stock total y mostrarlo en una ventana emergente
    if stock_total:
        messagebox.showinfo("Stock Total", f"El stock total de productos es de {stock_total} unidades.")
    else:
        messagebox.showwarning("Stock", "No hay productos en la base de datos o el stock es 0.")

    # Devolver el stock total por si lo necesitas en otro lugar del código
    return stock_total


# Función para buscar un producto por nombre en la base de datos
def buscar_producto(nombre):
    # Establecer una conexión a la base de datos
    conexion = conectar()
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL para buscar el producto por nombre
    cursor.execute("SELECT * FROM Producto WHERE Nombre = ?", (nombre,))

    # Obtener el primer producto que coincida con el nombre
    producto = cursor.fetchone()

    # Cerrar la conexión a la base de datos
    conexion.close()

    # Devolver el producto encontrado (o None si no se encuentra)
    return producto

    # Funcion para ver el producto mas vendido
def producto_mas_vendido():
    # Establecer una conexión a la base de datos
    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL para encontrar el producto más vendido
    cursor.execute('''
    SELECT p.Nombre, SUM(d.Cantidad) as TotalVendido
    FROM DetalleAlbaran d
    JOIN Producto p ON d.ProductoID = p.ID
    GROUP BY d.ProductoID
    ORDER BY TotalVendido DESC
    LIMIT 1
    ''')

    # Obtener el resultado de la consulta
    resultado = cursor.fetchone()

    # Cerrar la conexión a la base de datos
    conexion.close()

    # Verificar si se encontró un producto más vendido
    if resultado:
        producto_mas_vendido, total_vendido = resultado
        messagebox.showinfo("Producto Más Vendido", f"El producto más vendido es '{producto_mas_vendido}' con un total de {total_vendido} unidades vendidas.")
    else:
        messagebox.showwarning("Ventas", "No hay datos de ventas en la base de datos.")

    # Funcion para ver el producto con menos stock
def producto_con_menos_stock():
    try:
        conexion = sqlite3.connect('database.db')
        cursor = conexion.cursor()

        cursor.execute('''
        SELECT Nombre, Cantidad
        FROM Producto
        ORDER BY Cantidad ASC
        LIMIT 1
        ''')

        resultado = cursor.fetchone()

    except sqlite3.Error:
        return "Error en la DB", "N/A"
    finally:
        conexion.close()

    if resultado:
        return resultado  # Devolvemos producto y cantidad
    else:
        return "Ningún producto", "N/A"  # En caso de que no haya datos


    # Funciona para ver los productos que caducan este año
def productos_que_caducan_este_ano():
    try:
        conexion = sqlite3.connect('database.db')
        cursor = conexion.cursor()

        este_anio = datetime.now().year  # Obtiene el año actual

        cursor.execute(f'''
        SELECT Nombre, Caducidad
        FROM Producto
        WHERE Caducidad = {este_anio}
        ''')

        resultado = cursor.fetchall()

    except sqlite3.Error:
        return [("Error en la DB", "N/A")]
    finally:
        conexion.close()

    if resultado:
        return resultado  # Devolvemos una lista de productos con sus caducidades
    else:
        return [("Ningún producto", "N/A")]  # En caso de que no haya datos



    # Funcion para ver el total de ventas
def total_de_ventas():
    # Establecer una conexión a la base de datos
    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()

    consulta = '''
    SELECT Cantidad, Precio
    FROM DetalleAlbaran
    '''

    cursor.execute(consulta)

    # Inicializamos el total de ventas en 0
    total_ventas = 0

    # Calcular el total sumando el producto de la cantidad y el precio unitario de cada registor.
    for cantidad, precio in cursor.fetchall():
        total_ventas += cantidad * precio

    # Cerramos la conexion a la base de datos
    conexion.close()

    # Verificar si hubo ventas
    if total_ventas >0:
        messagebox.showinfo("Total de ventas",
                            f"El total de todas las ventas es: '{total_ventas}' € ")
    else:
        messagebox.showwarning("Ventas", "No hay datos de ventas en la base de datos.")

    return total_ventas


