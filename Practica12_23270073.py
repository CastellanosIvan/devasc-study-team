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

# Funciones para la tabla lineainv
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

# Funciones para la tabla tipoproyecto
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

def actualizar_tipo_proyecto(tipo_actual, nuevo_tipo):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        sql = "UPDATE tipoproyecto SET tipo = ? WHERE tipo = ?"
        try:
            cursor.execute(sql, (nuevo_tipo, tipo_actual))
            conn.commit()
            print("Tipo de proyecto actualizado correctamente.")
        except mariadb.Error as e:
            print(f"Error al actualizar: {e}")
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

# Funciones para la tabla profesor
def insertar_profesor(nombreProf):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        sql = "INSERT INTO profesor (nombreProf) VALUES (?)"
        try:
            cursor.execute(sql, (nombreProf,))
            conn.commit()
            print("Profesor insertado correctamente.")
        except mariadb.Error as e:
            print(f"Error al insertar profesor: {e}")
        finally:
            cursor.close()
            conn.close()

def obtener_profesores():
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        sql = "SELECT * FROM profesor"
        try:
            cursor.execute(sql)
            profesores = cursor.fetchall()
            print("\nLista de Profesores:")
            for profesor in profesores:
                print(f"ID: {profesor[0]}, Nombre: {profesor[1]}")
        except mariadb.Error as e:
            print(f"Error al obtener datos: {e}")
        finally:
            cursor.close()
            conn.close()

def actualizar_profesor(idprofesor, nuevo_nombre):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        sql = "UPDATE profesor SET nombreProf = ? WHERE idprofesor = ?"
        try:
            cursor.execute(sql, (nuevo_nombre, idprofesor))
            conn.commit()
            print("Profesor actualizado correctamente.")
        except mariadb.Error as e:
            print(f"Error al actualizar: {e}")
        finally:
            cursor.close()
            conn.close()

def eliminar_profesor(idprofesor):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        sql = "DELETE FROM profesor WHERE idprofesor = ?"
        try:
            cursor.execute(sql, (idprofesor,))
            conn.commit()
            print("Profesor eliminado correctamente.")
        except mariadb.Error as e:
            print(f"Error al eliminar profesor: {e}")
        finally:
            cursor.close()
            conn.close()

# Funciones para la tabla profesorproy
def insertar_profesor_proy(idprofesor, clave, calificacion, rol):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        sql = "INSERT INTO profesorproy (idprofesor, clave, calificacion, rol) VALUES (?, ?, ?, ?)"
        try:
            cursor.execute(sql, (idprofesor, clave, calificacion, rol))
            conn.commit()
            print("Relación Profesor-Proyecto insertada correctamente.")
        except mariadb.Error as e:
            print(f"Error al insertar: {e}")
        finally:
            cursor.close()
            conn.close()

def obtener_profesores_proy():
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        sql = "SELECT * FROM profesorproy"
        try:
            cursor.execute(sql)
            relaciones = cursor.fetchall()
            print("\nLista de Relaciones Profesor-Proyecto:")
            for relacion in relaciones:
                print(f"ID Profesor: {relacion[0]}, Clave Proyecto: {relacion[1]}, Calificación: {relacion[2]}, Rol: {relacion[3]}")
        except mariadb.Error as e:
            print(f"Error al obtener datos: {e}")
        finally:
            cursor.close()
            conn.close()

def actualizar_profesor_proy(idprofesor, clave, calificacion, rol):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        sql = "UPDATE profesorproy SET calificacion = ?, rol = ? WHERE idprofesor = ? AND clave = ?"
        try:
            cursor.execute(sql, (calificacion, rol, idprofesor, clave))
            conn.commit()
            print("Relación Profesor-Proyecto actualizada correctamente.")
        except mariadb.Error as e:
            print(f"Error al actualizar: {e}")
        finally:
            cursor.close()
            conn.close()

def eliminar_profesor_proy(idprofesor, clave):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        sql = "DELETE FROM profesorproy WHERE idprofesor = ? AND clave = ?"
        try:
            cursor.execute(sql, (idprofesor, clave))
            conn.commit()
            print("Relación Profesor-Proyecto eliminada correctamente.")
        except mariadb.Error as e:
            print(f"Error al eliminar: {e}")
        finally:
            cursor.close()
            conn.close()

# Menú principal
if __name__ == "__main__":
    while True:
        print("\n=== CRUD para Líneas de Investigación, Tipos de Proyecto, Profesores y Profesor-Proyecto ===")
        print("\n1. Insertar Línea de Investigación")
        print("2. Mostrar Líneas de Investigación")
        print("3. Actualizar Línea de Investigación")
        print("4. Eliminar Línea de Investigación")
        print("\n5. Insertar Tipo de Proyecto")
        print("6. Mostrar Tipos de Proyecto")
        print("7. Actualizar Tipo de Proyecto")
        print("8. Eliminar Tipo de Proyecto")
        print("\n9. Insertar Profesor")
        print("10. Mostrar Profesores")
        print("11. Actualizar Profesor")
        print("12. Eliminar Profesor")
        print("\n13. Insertar Relación Profesor-Proyecto")
        print("14. Mostrar Relaciones Profesor-Proyecto")
        print("15. Actualizar Relación Profesor-Proyecto")
        print("16. Eliminar Relación Profesor-Proyecto")
        print("17. Salir")
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
            tipo = input("Ingrese el tipo de proyecto: ")
            insertar_tipo_proyecto(tipo)
        elif opcion == "6":
            obtener_tipos_proyecto()
        elif opcion == "7":
            tipo_actual = input("Ingrese el tipo de proyecto a actualizar: ")
            nuevo_tipo = input("Ingrese el nuevo tipo de proyecto: ")
            actualizar_tipo_proyecto(tipo_actual, nuevo_tipo)
        elif opcion == "8":
            tipo = input("Ingrese el tipo de proyecto a eliminar: ")
            eliminar_tipo_proyecto(tipo)
        elif opcion == "9":
            nombreProf = input("Ingrese el nombre del profesor: ")
            insertar_profesor(nombreProf)
        elif opcion == "10":
            obtener_profesores()
        elif opcion == "11":
            idprofesor = input("Ingrese el ID del profesor a actualizar: ")
            nuevo_nombre = input("Ingrese el nuevo nombre del profesor: ")
            actualizar_profesor(idprofesor, nuevo_nombre)
        elif opcion == "12":
            idprofesor = input("Ingrese el ID del profesor a eliminar: ")
            eliminar_profesor(idprofesor)
        elif opcion == "13":
            idprofesor = input("Ingrese el ID del profesor: ")
            clave = input("Ingrese la clave del proyecto: ")
            calificacion = float(input("Ingrese la calificación: "))
            rol = input("Ingrese el rol del profesor en el proyecto: ")
            insertar_profesor_proy(idprofesor, clave, calificacion, rol)
        elif opcion == "14":
            obtener_profesores_proy()
        elif opcion == "15":
            idprofesor = input("Ingrese el ID del profesor: ")
            clave = input("Ingrese la clave del proyecto: ")
            calificacion = float(input("Ingrese la nueva calificación: "))
            rol = input("Ingrese el nuevo rol del profesor en el proyecto: ")
            actualizar_profesor_proy(idprofesor, clave, calificacion, rol)
        elif opcion == "16":
            idprofesor = input("Ingrese el ID del profesor: ")
            clave = input("Ingrese la clave del proyecto: ")
            eliminar_profesor_proy(idprofesor, clave)
        elif opcion == "17":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")