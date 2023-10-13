import sqlite3
from tkinter import messagebox


def conectar():
    # Esta función se encarga de establecer una conexión a la base de datos SQLite 'database.db'.

    conexion = sqlite3.connect('database.db')
    return conexion



def obtener_productos():
    # Establecer una conexión a la base de datos
    conexion = conectar()

    # Crear un cursor para interactuar con la base de datos
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL para seleccionar todos los productos
    cursor.execute("SELECT * FROM Producto")

    # Obtener todos los resultados de la consulta
    productos = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    conexion.close()

    # Devolver la lista de productos
    return productos



def obtener_clientes():
    # Establecer una conexión a la base de datos
    conexion = conectar()

    # Crear un cursor para interactuar con la base de datos
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL para seleccionar todos los clientes
    cursor.execute("SELECT * FROM Cliente")

    # Obtener todos los resultados de la consulta
    clientes = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    conexion.close()

    # Devolver la lista de clientes
    return clientes


def obtener_proveedores():
    # Establecer una conexión a la base de datos
    conexion = conectar()

    # Crear un cursor para interactuar con la base de datos
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL para seleccionar todos los clientes
    cursor.execute("SELECT * FROM Proveedor")

    # Obtener todos los resultados de la consulta
    proveedores = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    conexion.close()

    # Devolver la lista de proveedores
    return proveedores



def obtener_nombre_del_proveedor():
    try:
        # Establecer una conexión a la base de datos
        conexion = conectar()  # Asumo que esta es una función que has definido en otro lugar

        # Crear un cursor para interactuar con la base de datos
        cursor = conexion.cursor()

        # Ejecutar una consulta SQL para seleccionar solo los nombres de los proveedores
        cursor.execute("SELECT nombre FROM Proveedor")

        # Obtener todos los resultados de la consulta
        proveedores = cursor.fetchall()

        # Cerrar la conexión a la base de datos
        conexion.close()

        # Devolver solo los nombres de los proveedores como una lista plana
        return [item[0] for item in proveedores]

    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return []



def obtener_albaran():
    # Establecer una conexión a la base de datos
    conexion = conectar()

    # Crear un cursor para interactuar con la base de datos
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL para seleccionar todos los albaranes
    cursor.execute("SELECT * FROM Albaran")

    # Obtener todos los resultados de la consulta
    albaranes = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    conexion.close()

    # Devolver la lista de albaranes
    return albaranes


def obtener_factura():
    # Establecer una conexión a la base de datos
    conexion = conectar()

    # Crear un cursor para interactuar con la base de datos
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL para seleccionar todos los albaranes
    cursor.execute("SELECT * FROM Factura")

    # Obtener todos los resultados de la consulta
    facturas = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    conexion.close()

    # Devolver la lista de albaranes
    return facturas



def guardar_producto(producto):
    # Establecer una conexión a la base de datos
    conexion = conectar()
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL para insertar un nuevo producto
    cursor.execute('''
        INSERT INTO Producto (Nombre, Familia, Precio, IVA, Proveedor, Cantidad, Caducidad)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (producto.nombre, producto.familia, producto.precio, producto.iva, producto.proveedor, producto.cantidad,
          producto.caducidad))

    # Guardar los cambios en la base de datos
    conexion.commit()

    # Cerrar la conexión a la base de datos
    conexion.close()



def guardar_cliente(cliente):
    # Establecer una conexión a la base de datos
    conexion = conectar()
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL para insertar un nuevo cliente
    cursor.execute("""
        INSERT INTO Cliente (nombre, cif, direccion, localidad, provincia, telefono, email)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (cliente.nombre, cliente.cif, cliente.direccion, cliente.localidad, cliente.provincia, cliente.telefono,
          cliente.email))

    # Guardar los cambios en la base de datos
    conexion.commit()

    # Cerrar la conexión a la base de datos
    conexion.close()




def guardar_proveedor(proveedor):
    # Establecer una conexión a la base de datos
    conexion = conectar()
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL para insertar un nuevo proveedor
    cursor.execute("""
        INSERT INTO proveedor (nombre, cif, direccion, localidad, provincia, telefono, email)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
    proveedor.nombre, proveedor.cif, proveedor.direccion, proveedor.localidad, proveedor.provincia, proveedor.telefono,
    proveedor.email))

    # Guardar los cambios en la base de datos
    conexion.commit()

    # Cerrar la conexión a la base de datos
    conexion.close()


def crear_tablas():
    # Establecer una conexión a la base de datos
    conexion = conectar()
    cursor = conexion.cursor()

    # Crear la tabla 'Producto' si no existe
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Producto ( 
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT NOT NULL,
        Familia TEXT,
        Precio REAL NOT NULL,
        IVA REAL,
        Proveedor TEXT,
        Cantidad INTEGER,
        Caducidad TEXT
    )
    ''')

    # Crear la tabla 'Cliente' si no existe
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Cliente (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT NOT NULL,
        CIF TEXT NOT NULL,
        Direccion TEXT,
        Localidad TEXT,
        Provincia TEXT,
        Telefono TEXT,
        Email TEXT
    )
    ''')

    # Crear la tabla 'Proveedor' si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Proveedor (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre TEXT NOT NULL,
            CIF TEXT NOT NULL,
            Direccion TEXT,
            Localidad TEXT,
            Provincia TEXT,
            Telefono TEXT,
            Email TEXT
        )
        ''')

    # Crear la tabla 'Albaran' si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Albaran (
            AlbaranID INTEGER PRIMARY KEY AUTOINCREMENT,
            Fecha DATE,
            ClienteID INT,
            Total REAL,        
            FOREIGN KEY (ClienteID) REFERENCES Cliente(ID)
        );
        ''')

    # Crear la tabla 'Factura' si no existe
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Factura (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        ClienteID INTEGER,
        Nombre TEXT NOT NULL,
        CIF TEXT NOT NULL,
        Fecha DATE,
        Iva REAL,
        Descuento REAL,
        Total REAL,
        FOREIGN KEY (ClienteID) REFERENCES Cliente(ID)
    )
    ''')

    # # Crear la tabla 'DetalleAlbaran' si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS DetalleAlbaran (
            DetalleID INTEGER PRIMARY KEY AUTOINCREMENT,
            AlbaranID INTEGER,
            ClienteID INTEGER,
            ProductoID INTEGER,
            Producto TEXT,
            Precio REAL,
            Cantidad INTEGER,
            Fecha TEXT,
            Total REAL,
            FOREIGN KEY (AlbaranID) REFERENCES Albaran(ID),
            FOREIGN KEY (ClienteID) REFERENCES Cliente(ID),
            FOREIGN KEY (ProductoID) REFERENCES Producto(ID)
        )
        ''')

    # # Crear la tabla 'DetalleAlbaran' si no existe
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS DetalleFactura (
                DetalleID INTEGER PRIMARY KEY AUTOINCREMENT,
                AlbaranID INTEGER,
                ClienteID INTEGER,
                ProductoID INTEGER,
                Producto TEXT,
                Precio REAL,
                Cantidad INTEGER,
                Fecha TEXT,
                Total REAL,
                FOREIGN KEY (AlbaranID) REFERENCES Albaran(ID),
                FOREIGN KEY (ClienteID) REFERENCES Cliente(ID),
                FOREIGN KEY (ProductoID) REFERENCES Producto(ID)
            )
            ''')

    # Guarda los cambios y cierra la conexión a la base de datos
    conexion.commit()
    conexion.close()


if __name__ == '__main__':
    # Esta condición verifica si este script se está ejecutando como el programa principal.
    # Si es así, llama a la función crear_tablas para crear las tablas en la base de datos.
    crear_tablas()


def add_albaran(id_cliente, id_producto, id_proveedor, cantidad, fecha):
    try:
        conn = open_db()
        c = conn.cursor()

        c.execute("INSERT INTO DetalleAlbaran (ID_Cliente, ID_Producto, ID_Proveedor, Cantidad, Fecha) VALUES (?, ?, ?, ?, ?)",
                  (id_cliente, id_producto, id_proveedor, cantidad, fecha))

        conn.commit()
        close_db(conn)
        messagebox.showinfo("Éxito", "Albarán añadido con éxito.")
    except Exception as e:
        close_db(conn)
        messagebox.showerror("Error", f"Hubo un error: {e}")



def insertar_detalle_albaran(id_albaran, id_producto, cantidad):
    # Establecer una conexión a la base de datos
    conexion = conectar()
    cursor = conexion.cursor()

    # Insertar un nuevo detalle de albarán con el ID del albarán, el ID del producto y la cantidad proporcionados
    cursor.execute("INSERT INTO DetalleAlbaran (ID_Albaran, ID_Producto, Cantidad) VALUES (?, ?, ?)",
                   (id_albaran, id_producto, cantidad))

    # Guardar los cambios en la base de datos
    conexion.commit()

    # Cerrar la conexión a la base de datos
    conexion.close()



def guardar_albaran_completo(fecha, id_cliente, productos_agregados):
    # 1. Guardar el albarán
    id_albaran = insertar_albaran(fecha, id_cliente)

    # 2. Guardar los detalles del albarán
    for producto in productos_agregados:
        id_producto = obtener_id_producto_por_nombre(conexion, producto["nombre"])
        if id_producto:  # Solo si encontramos el producto en la base de datos
            insertar_detalle_albaran(id_albaran, id_producto, producto["cantidad"])

    # 3. Mostrar un mensaje de confirmación
    print("Albarán y sus detalles guardados con éxito.")
    messagebox.showinfo("Información", "Albarán guardado con éxito.")



def obtener_datos_albaran(id_albaran):
    conexion = None
    try:
        conexion = conectar()  # Establece la conexión a la base de datos
        cursor = conexion.cursor()

        # Consulta SQL para obtener los datos del albarán
        cursor.execute("SELECT fecha, id_cliente FROM Albaran WHERE ID = ?", (id_albaran,))
        albaran = cursor.fetchone()  # Obtiene la fila del albarán

        if albaran:
            fecha_albaran, id_cliente = albaran
            # Retorna la fecha y el ID del cliente del albarán
            return fecha_albaran, id_cliente
        else:
            # Si no se encuentra el albarán, retorna None
            return None, None

    except sqlite3.Error as error:
        print("Error al obtener datos del albarán:", error)
        return None, None

    finally:
        if conexion:
            conexion.close()  # Cierra la conexión a la base de datos


# Función para obtener los datos del detalle del albarán
def obtener_datos_detalle_albaran(id_detalle):
    conexion = None
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        # Consulta SQL para obtener los datos del detalle del albarán
        cursor.execute("SELECT id_albaran, id_producto, cantidad FROM DetalleAlbaran WHERE ID = ?", (id_detalle,))
        detalle_albaran = cursor.fetchone()

        if detalle_albaran:
            id_albaran, id_producto, cantidad = detalle_albaran
            return id_albaran, id_producto, cantidad
        else:
            return None, None, None

    except sqlite3.Error as error:
        print("Error al obtener datos del detalle del albarán:", error)
        return None, None, None

    finally:
        if conexion:
            conexion.close()



################################  F A C T U R A S  #####################################


def insertar_venta_directa(producto, cantidad, precio):
    # Establecer una conexión a la base de datos
    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()

    # Consulta para insertar la venta en la tabla FacturaDirecta
    cursor.execute('''
    INSERT INTO Factura(Producto, Cantidad, Precio)
    VALUES (?, ?, ?)
    ''', (producto, cantidad, precio))

    # Confirmar la transacción
    conexion.commit()

    # Cerrar la conexión
    conexion.close()

    print("Venta insertada con éxito!")


def crear_factura_desde_albaran(id_albaran, ClienteID, fecha, total):
    try:
        id_factura = insertar_factura(fecha, ClienteID)
        print(f"Creando factura desde albarán con AlbaranID: {id_albaran}, id_cliente: {ClienteID}, fecha: {fecha}, total: {total}")

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("SELECT ClienteID FROM Albaran WHERE AlbaranID=?", (id_albaran,))
        cliente_albaran = cursor.fetchone()[0]

        if str(cliente_albaran) != str(ClienteID):
            print("El albarán no pertenece a este cliente.")
            return

        # Inicializa el total de la factura a 0
        total_factura = 0.0

        cursor.execute("SELECT AlbaranID, ClienteId, ProductoID, Producto, Precio, Cantidad, Fecha, Total FROM DetalleAlbaran WHERE AlbaranID=?", (id_albaran,))
        detalles = cursor.fetchall()

        for detalle in detalles:
            AlbaranId, ClienteId, producto_id, producto, precio, cantidad, fecha, total = detalle

            # Pasa el precio y la cantidad a float
            precio = float(precio)
            cantidad = float(cantidad)

            # Calcula el total con IVA
            iva = 0.21
            total_con_iva = total * (1 + iva)

            # Acumula el total con IVA
            total_factura += total_con_iva

            cursor.execute("INSERT INTO DetalleFactura (AlbaranID, ClienteID, ProductoID, Producto, Precio, Cantidad, Fecha) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (AlbaranId, ClienteId, producto_id, producto, precio, cantidad, fecha))

        # Aquí actualizamos el total en la tabla Factura
        cursor.execute("UPDATE Factura SET Total=? WHERE ID=?", (total_factura, id_factura))

        # Guardar los cambios
        conexion.commit()
    except Exception as e:
        print(f"Se ha producido un error: {e}")
    finally:
        if conexion:
            conexion.close()

    print(f"Factura {id_factura} creada con éxito.")


def insertar_factura(fecha, ClienteID):
    try:
        print(f"Debug: id_cliente dentro de insertar_factura = {ClienteID}, tipo = {type(ClienteID)}")
        print(f"Iniciando inserción de factura con fecha: {fecha} y id_cliente: {ClienteID}")
        conexion = conectar()
        cursor = conexion.cursor()

        print("Voy a obtener el nombre y el CIF del cliente desde ClienteID")
        cursor.execute("SELECT Nombre, CIF FROM Cliente WHERE ID=?", (ClienteID,))
        resultado = cursor.fetchone()
        print(f"Resultado obtenido: {resultado}")

        if resultado is None:
            print("Error: Cliente con ID especificado no encontrado.")
            mostrar_mensaje("Error: Cliente con ID especificado no encontrado.")
            conexion.close()
            return None

        nombre_cliente, cif_cliente = resultado
        iva = "21"

        print(
            f"INSERTANDO EN Factura, fecha {fecha}, clienteid {ClienteID}, nombre {nombre_cliente}, cif {cif_cliente}")
        cursor.execute("INSERT INTO Factura (Fecha, ClienteID, Nombre, CIF, Iva) VALUES (?, ?, ?, ?, ?)",
                       (fecha, ClienteID, nombre_cliente, cif_cliente, iva))

        id_factura = cursor.lastrowid
        print(f"ID de factura recién insertada: {id_factura}")
        mostrar_mensaje(f"Factura creada con éxito. ID de factura: {id_factura}")

        conexion.commit()
        conexion.close()

        return id_factura
    except Exception as e:
        print(f"Se ha producido un error: {e}")
        mostrar_mensaje(f"Se ha producido un error: {e}")
        return None

import tkinter as tk
from tkinter import messagebox

def mostrar_mensaje(mensaje):
    ventana = tk.Tk()  # Crea una nueva ventana Tkinter
    ventana.withdraw()  # Oculta la ventana principal de Tkinter

    # Muestra un cuadro de mensaje informativo con el mensaje proporcionado
    messagebox.showinfo("Información", mensaje)

    ventana.destroy()  # Destruye la ventana para liberar recursos

def insertar_detalle_factura(id_factura, id_producto, cantidad):
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        # Obtener precio y IVA del producto
        cursor.execute("SELECT Precio, IVA FROM Producto WHERE ID = ?", (id_producto,))
        data = cursor.fetchone()

        if data is None:
            mostrar_mensaje("Producto no encontrado.")
            print("Producto no encontrado")
            conexion.close()
            return

        precio, iva = data

        # Calcular el subtotal y el total con IVA
        subtotal = precio * cantidad
        total_con_iva = subtotal * (1 + (iva / 100))

        # Insertar el detalle de la factura en la tabla DetalleFactura
        cursor.execute("INSERT INTO DetalleFactura (ID_Factura, ID_Producto, Cantidad, Total) VALUES (?, ?, ?, ?)",
                       (id_factura, id_producto, cantidad, total_con_iva))

        # Guardar los cambios en la base de datos
        conexion.commit()

        # Cerrar la conexión a la base de datos
        conexion.close()

        # Mostrar mensaje de éxito
        mostrar_mensaje(f"Detalle de factura creado con éxito. Total con IVA: {total_con_iva}")
    except Exception as e:
        # Mostrar mensaje de error
        mostrar_mensaje(f"Ha ocurrido un error: {e}")
        print(f"Ha ocurrido un error: {e}")


def calcular_total_con_iva(id_albaran):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT Total FROM Albaran WHERE AlbaranID=?", (id_albaran,))
    total_sin_iva = cursor.fetchone()[0]

    # Aplicar el 21% de IVA
    total_con_iva = total_sin_iva * 1.21

    # Cerrar la conexión
    conexion.close()

    return total_con_iva


