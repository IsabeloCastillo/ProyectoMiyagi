import tkinter as tk
from tkinter import messagebox



class Producto:
    '''Clase Producto
    Incluye nombre,familia,precio,iva,proveedor,cantidad y caducidad del producto
    Args:
        nombre: Es string que compone el nombre del producto
        familia: String que define la familia a la que pertenece el producto
        precio: Es un float, define el precio del producto
        iva: Es un integer, define el impuesto iva del producto
        proveedor: Es un string que define el nombre del proveedor del producto
        cantidad: Es un integer que define la cantidad de productos
        caducidad: Es integer de 4 digitos que define el año que caduca el producto
        si el producto no es perecedero, tambien sirve para caducidad de la garantia.'''
    def __init__(self, nombre, familia, precio, iva, proveedor, cantidad=None, caducidad=None):
        # Constructor de la clase Producto
        self.nombre = nombre
        self.familia = familia
        self.precio = precio
        self.iva = iva
        self.proveedor = proveedor
        self.cantidad = cantidad
        self.caducidad = caducidad

       # Funcion para mostrar mensajes informativos
    def mostrar_mensaje(self, mensaje):
        ventana = tk.Tk()
        ventana.withdraw()  # Ocultar ventana principal
        messagebox.showinfo("ℹ️ Información ℹ️", mensaje)
        ventana.destroy()

    def es_formato_caducidad_valido(self, caducidad):
        try:
            # Verificamos si la caducidad contiene exactamente 4 dígitos
            if len(caducidad) == 4 and caducidad.isdigit():
                return True
            else:
                # Si no cumple con el formato, mostramos un mensaje de error con messagebox
                messagebox.showerror("Error", "La caducidad debe tener 4 dígitos para el año (Ejemplo: 2023)")
                return False
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al validar la caducidad: {str(e)}")
            return False


    # Metodos guetter y setters
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevoNombre):
        try:
            if not nuevoNombre:
                raise ValueError("El campo nombre no puede estar vacío")
            self.__nombre = nuevoNombre
        except ValueError as e:
            self.mostrar_mensaje(e)

    @property
    def familia(self):
        return self.__familia

    @familia.setter
    def familia(self, nuevaFamilia):
        try:
            if not nuevaFamilia:
                raise ValueError("El campo familia no puede estar vacío")
            self.__familia = nuevaFamilia
        except ValueError as e:
            self.mostrar_mensaje(e)

    @property
    def precio(self):
        return self.__precio

    @precio.setter
    def precio(self, nuevoPrecio):
        try:
            self.__precio = float(nuevoPrecio)
        except ValueError:
            self.mostrar_mensaje("Amig@ el precio debe ser un valor numérico")

    @property
    def iva(self):
        return self.__iva

    @iva.setter
    def iva(self, nuevoIva):
        try:
            self.__iva = int(nuevoIva)
        except ValueError:
            self.mostrar_mensaje("Amig@ el iva debe ser un valor numerico")

    @property
    def proveedor(self):
        return self.__proveedor

    @proveedor.setter
    def proveedor(self, nuevoProveedor):
        try:
            if not nuevoProveedor:
                raise ValueError("El campo proveedor no puede estar vacío")
            self.__proveedor = nuevoProveedor
        except ValueError as e:
            self.mostrar_mensaje(e)

    @property
    def cantidad(self):
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, nuevaCantidad):
        try:
            self.__cantidad = int(nuevaCantidad)
        except ValueError:
            self.mostrar_mensaje("Amig@ la cantidad debe ser un valor numerico")

    @property
    def caducidad(self):
        return self.__caducidad

    @caducidad.setter
    def caducidad(self, nuevaCaducidad):
        try:
            if not self.es_formato_caducidad_valido(nuevaCaducidad):
                raise ValueError("La caducidad debe tener 4 dígitos para el año (Ejemplo: 2023)")
            self.__caducidad = nuevaCaducidad
        except ValueError as e:
            self.mostrar_mensaje(e)

    def __str__(self):
        return f"Nombre: {self.nombre}\nFamilia: {self.familia}\nPrecio: {self.precio}\nIVA: {self.iva}\nProveedor: {self.proveedor}\nCantidad: {self.cantidad}\nCaducidad: {self.caducidad}"



class Cliente:
    ''' Clase Cliente
    Incluye nombre, cif, direccion, localidad, provincia, teléfono y email del cliente.
    Args:
        nombre: Es un string que define el nombre del cliente
        cif: String que define el cif del cliente
        direccion: String que define la direccion del cliente
        localidad: Es un string que define la localidad del cliente
        provincia: Es un string que define la provincia del cliente
        telefono : Es un string que define el telefono del cliente
        email: String que define el correo electronico del cliente'''

    def __init__(self, nombre, cif, direccion, localidad, provincia, telefono, email):
        # Constructor de la clase Cliente
        self.nombre = nombre
        self.cif = cif
        self.direccion = direccion
        self.localidad = localidad
        self.provincia = provincia
        self.telefono = telefono
        self.email = email

    def mostrar_mensaje(self, mensaje):
        ventana = tk.Tk()
        ventana.withdraw()  # Ocultar ventana principal
        messagebox.showinfo("Información", mensaje)
        ventana.destroy()

    # Funcion para
    def es_direccion_email_valida(self, email):
        try:
            # Verificamos si el email contiene "@" y al menos un "."
            if "@" in email and "." in email:
                return True
            else:
                messagebox.showerror("Error", "La dirección de correo electrónico no es válida")
                return False
        except Exception as e:
            messagebox.showerror("Error",
                                 f"Se produjo un error al validar la dirección de correo electrónico: {str(e)}")
            return False


    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevoNombre):
        try:
            if not nuevoNombre:
                raise ValueError("El campo nombre no puede estar vacío")
            self.__nombre = nuevoNombre
        except ValueError as e:
            self.mostrar_mensaje(e)

    @property
    def cif(self):
        return self.__cif

    @cif.setter
    def cif(self, nuevoCif):
        try:
            if not nuevoCif:
                raise ValueError("El campo cif no puede estar vacío")
            self.__cif = nuevoCif
        except ValueError as e:
            self.mostrar_mensaje(e)

    @property
    def direccion(self):
        return self.__direccion

    @direccion.setter
    def direccion(self, nuevaDireccion):
        try:
            if not nuevaDireccion:
                raise ValueError("El campo direccion no puede estar vacío")
            self.__direccion = nuevaDireccion
        except ValueError as e:
            self.mostrar_mensaje(e)

    @property
    def localidad(self):
        return self.__localidad

    @localidad.setter
    def localidad(self, nuevaLocalidad):
        try:
            if not nuevaLocalidad:
                raise ValueError("El campo localidad no puede estar vacío")
            self.__localidad = nuevaLocalidad
        except ValueError as e:
            self.mostrar_mensaje(e)

    @property
    def provincia(self):
        return self.__provincia

    @provincia.setter
    def provincia(self, nuevaProvincia):
        try:
            if not nuevaProvincia:
                raise ValueError("El campo provincia no puede estar vacío")
            self.__provincia = nuevaProvincia
        except ValueError as e:
            self.mostrar_mensaje(e)

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, telefono):
        if not telefono.isdigit():
            self.mostrar_mensaje("¡Oye! El número de teléfono debe contener solo números.")
            return
        self.__telefono = telefono

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, nuevoEmail):
        try:
            # Verificamos si el nuevoEmail es una dirección de correo electrónico válida
            if not self.es_direccion_email_valida(nuevoEmail):
                raise ValueError("El correo electrónico no es válido")
            self.__email = nuevoEmail
        except ValueError as e:
            self.mostrar_mensaje(e)


class Proveedor:
    ''' Clase proveedor
        Incluye nombre, cif, direccion, localidad, provincia, teléfono y email del proveedor.
        Args:
            nombre: Es un string que define el nombre del proveedor
            cif: String que define el cif del proveedor
            direccion: String que define la direccion del proveedor
            localidad: Es un string que define la localidad del proveedor
            provincia: Es un string que define la provincia del proveedor
            telefono : Es un string que define el telefono del proveedor
            email: String que define el correo electronico del proveedor'''

    def __init__(self, nombre, cif, direccion, localidad, provincia, telefono, email):
        # Inicialización de atributos
        self.nombre = nombre
        self.cif = cif
        self.direccion = direccion
        self.localidad = localidad
        self.provincia = provincia
        self.telefono = telefono
        self.email = email

    def mostrar_mensaje(self, mensaje):
        ventana = tk.Tk()
        ventana.withdraw()  # Ocultar ventana principal
        messagebox.showinfo("Información", mensaje)
        ventana.destroy()

    def es_direccion_email_valida(self, email):
        try:
            # Verificamos si el email contiene "@" y al menos un "."
            if "@" in email and "." in email:
                return True
            else:
                messagebox.showerror("Error", "La dirección de correo electrónico no es válida")
                return False
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al validar la dirección de correo electrónico: {str(e)}")
            return False


    # Metodos guetter y setters de Proveedor
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevoNombre):
        try:
            if not nuevoNombre:
                raise ValueError("El campo nombre no puede estar vacío")
            self.__nombre = nuevoNombre
        except ValueError as e:
            self.mostrar_mensaje(e)

    @property
    def cif(self):
        return self.__cif

    @cif.setter
    def cif(self, nuevoCif):
        try:
            if not nuevoCif:
                raise ValueError("El campo cif no puede estar vacío")
            self.__cif = nuevoCif
        except ValueError as e:
            self.mostrar_mensaje(e)

    @property
    def direccion(self):
        return self.__direccion

    @direccion.setter
    def direccion(self, nuevaDireccion):
        try:
            if not nuevaDireccion:
                raise ValueError("El campo direccion no puede estar vacío")
            self.__direccion = nuevaDireccion
        except ValueError as e:
            self.mostrar_mensaje(e)

    @property
    def localidad(self):
        return self.__localidad

    @localidad.setter
    def localidad(self, nuevaLocalidad):
        try:
            if not nuevaLocalidad:
                raise ValueError("El campo localidad no puede estar vacío")
            self.__localidad = nuevaLocalidad
        except ValueError as e:
            self.mostrar_mensaje(e)

    @property
    def provincia(self):
        return self.__provincia

    @provincia.setter
    def provincia(self, nuevaProvincia):
        try:
            if not nuevaProvincia:
                raise ValueError("El campo provincia no puede estar vacío")
            self.__provincia = nuevaProvincia
        except ValueError as e:
            self.mostrar_mensaje(e)

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, telefono):
        if not telefono.isdigit():
            self.mostrar_mensaje("¡Oye! El número de teléfono debe contener solo números.")
            return
        self.__telefono = telefono

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, nuevoEmail):
        try:
            # Verificamos si el nuevoEmail es una dirección de correo electrónico válida
            if not self.es_direccion_email_valida(nuevoEmail):
                raise ValueError("El correo electrónico no es válido")
            self.__email = nuevoEmail
        except ValueError as e:
            self.mostrar_mensaje(e)


class Albaran:
    '''Clase Albaran:
    Consta de  id, id_proveedor, id_cliente, fecha, producto, cantidad, iva, descuento y total albaran'''


    def __init__(self, id=None, id_proveedor=None, id_cliente=None, fecha=None,
                 producto=None, cantidad=None, iva=None, descuento=None, total_albaran=None):
        # Inicialización de atributos
        self.__id = id
        self.__id_proveedor = id_proveedor
        self.__id_cliente = id_cliente
        self.__fecha = fecha
        self.__producto = producto
        self.__cantidad = cantidad
        self.__iva = iva
        self.__descuento = descuento
        self.__total_albaran = total_albaran

    def mostrar_mensaje(self, mensaje):
        ventana = tk.Tk()
        ventana.withdraw()  # Ocultar ventana principal
        messagebox.showinfo("Información", mensaje)
        ventana.destroy()

    def es_direccion_email_valida(self, email):
        return "@" in email and "." in email

    # Propiedades para acceder y modificar atributos privados (se han definido para cada atributo)

    def __str__(self):
        return f"Albaran(ID: {self.__id}, Proveedor: {self.__id_proveedor}, Cliente: {self.__id_cliente}, Fecha: {self.__fecha}, Producto: {self.__producto}, Cantidad: {self.__cantidad}, IVA: {self.__iva}, Descuento: {self.__descuento}, Total Albaran: {self.__total_albaran})"

    def calcular_total(self):
        # Por si quieres agregar alguna lógica para calcular el total
        pass


