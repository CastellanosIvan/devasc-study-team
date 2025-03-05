import mariadb

try:
    # Conexión a la base de datos
    conexion = mariadb.connect(
        host="localhost",     # Dirección del servidor MariaDB
        user="root",          # Usuario de la base de datos
        password="mysql",     # Contraseña del usuario
        database="dbtaller",  # Nombre de la base de datos
        port=3307             # Puerto de MariaDB (por defecto es 3307)
    )

    print("Conexión exitosa a MariaDB")

    cursor = conexion.cursor()

    # Operación CREATE (Insertar)
    try:
        cursor.execute("INSERT INTO lineainv VALUES (?, ?)", ("IA001", "Inteligencia Artificial"))
        conexion.commit()
        print("Línea de investigación insertada correctamente.")
    except mariadb.Error as e:
        print(f"Error al insertar: {e}")

    # Operación READ (Leer)
    try:
        cursor.execute("SELECT * FROM lineainv")
        resultado = cursor.fetchall()
        print("Líneas de investigación:")
        for fila in resultado:
            print(f"Clave: {fila[0]}, Nombre: {fila[1]}")
    except mariadb.Error as e:
        print(f"Error al leer: {e}")

    # Operación UPDATE (Actualizar)
    try:
        cursor.execute("UPDATE lineainv SET nombre = ? WHERE clavein = ?", ("Machine Learning", "IA001"))
        conexion.commit()
        print("Línea de investigación actualizada correctamente.")
    except mariadb.Error as e:
        print(f"Error al actualizar: {e}")

    # Operación DELETE (Eliminar)
    try:
        cursor.execute("DELETE FROM lineainv WHERE clavein = ?", ("IA001",))
        conexion.commit()
        print("Línea de investigación eliminada correctamente.")
    except mariadb.Error as e:
        print(f"Error al eliminar: {e}")

    cursor.close()
    conexion.close()

except mariadb.Error as e:
    print(f"Error al conectar a MariaDB: {e}")
