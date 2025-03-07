import mariadb

def conectar():
    try:
        conexion = mariadb.connect(
            host="localhost",
            user="root",
            password="mysql",
            database="dbtaller",
            port=3307
        )
        return conexion
    except mariadb.Error as e:
        print(f"Error de conexión: {e}")
        return None

def insertar_linea_inv(idlinea, nombreproy):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        sql = "INSERT INTO lineainv (idlinea, nombreproy) VALUES (?, ?)"
        try:
            cursor.execute(sql, (idlinea, nombreproy))
            conn.commit()
            print("Línea de investigación insertada correctamente.")
        except mariadb.Error as e:
            print(f"Error al insertar: {e}")
        finally:
            cursor.close()
            conn.close()

def obtener_lineas_inv():
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        sql = "SELECT * FROM lineainv"
        try:
            cursor.execute(sql)
            lineas = cursor.fetchall()
            print("\nLista de Líneas de Investigación:")
            for linea in lineas:
                print(f"ID: {linea[0]}, Proyecto: {linea[1]}")
        except mariadb.Error as e:
            print(f"Error al obtener datos: {e}")
        finally:
            cursor.close()
            conn.close()

def actualizar_linea_inv(idlinea, nuevo_nombre):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        sql = "UPDATE lineainv SET nombreproy = ? WHERE idlinea = ?"
        try:
            cursor.execute(sql, (nuevo_nombre, idlinea))
            conn.commit()
            print("Línea de investigación actualizada correctamente.")
        except mariadb.Error as e:
            print(f"Error al actualizar: {e}")
        finally:
            cursor.close()
            conn.close()

def eliminar_linea_inv(idlinea):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        sql = "DELETE FROM lineainv WHERE idlinea = ?"
        try:
            cursor.execute(sql, (idlinea,))
            conn.commit()
            print("Línea de investigación eliminada correctamente.")
        except mariadb.Error as e:
            print(f"Error al eliminar: {e}")
        finally:
            cursor.close()
            conn.close()

def insertar_tipo_proyecto(tipo):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        sql = "INSERT INTO tipoproyecto (tipo) VALUES (?)"
        try:
            cursor.execute(sql, (tipo,))
            conn.commit()
            print("Tipo de proyecto insertado correctamente.")
        except mariadb.Error as e:
            print(f"Error al insertar en tipoproyecto: {e}")
        finally:
            cursor.close()
            conn.close()

def obtener_tipos_proyecto():
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        sql = "SELECT * FROM tipoproyecto"
        try:
            cursor.execute(sql)
            proyectos = cursor.fetchall()
            print("\nLista de Tipos de Proyecto:")
            for proyecto in proyectos:
                print(f"Tipo: {proyecto[0]}")
        except mariadb.Error as e:
            print(f"Error al obtener datos: {e}")
        finally:
            cursor.close()
            conn.close()

def eliminar_tipo_proyecto(tipo):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        sql = "DELETE FROM tipoproyecto WHERE tipo = ?"
        try:
            cursor.execute(sql, (tipo,))
            conn.commit()
            print("Tipo de proyecto eliminado correctamente.")
        except mariadb.Error as e:
            print(f"Error al eliminar de tipoproyecto: {e}")
        finally:
            cursor.close()
            conn.close()

# Menú para probar las funciones
if __name__ == "__main__":
    while True:
        print("\n=== CRUD Líneas de Investigación y Tipos de Proyecto ===")
        print("1. Insertar Línea de Investigación")
        print("2. Mostrar Líneas de Investigación")
        print("3. Actualizar Línea de Investigación")
        print("4. Eliminar Línea de Investigación")
        print("5. Insertar Tipo de Proyecto")
        print("6. Mostrar Tipos de Proyecto")
        print("7. Eliminar Tipo de Proyecto")
        print("8. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            idlinea = input("Ingrese el ID de la línea de investigación: ")
            nombreproy = input("Ingrese el nombre del proyecto: ")
            insertar_linea_inv(idlinea, nombreproy)

        elif opcion == "2":
            obtener_lineas_inv()

        elif opcion == "3":
            idlinea = input("Ingrese el ID de la línea de investigación a actualizar: ")
            nuevo_nombre = input("Ingrese el nuevo nombre del proyecto: ")
            actualizar_linea_inv(idlinea, nuevo_nombre)

        elif opcion == "4":
            idlinea = input("Ingrese el ID de la línea de investigación a eliminar: ")
            eliminar_linea_inv(idlinea)

        elif opcion == "5":
            tipo = input("Ingrese el código del tipo de proyecto: ")
            insertar_tipo_proyecto(tipo)

        elif opcion == "6":
            obtener_tipos_proyecto()

        elif opcion == "7":
            tipo = input("Ingrese el código del tipo de proyecto a eliminar: ")
            eliminar_tipo_proyecto(tipo)

        elif opcion == "8":
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Intente de nuevo.")
