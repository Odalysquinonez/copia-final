from datetime import datetime, date

from pyodbc import IntegrityError, ProgrammingError

from datos.conexion import Conexion
from dominio.Estudiante import Estudiante


class EstudianteDao:
    _INSERTAR = "INSERT INTO Estudiantes (cedula, nombre, apellido, email, carrera, activo, estatura, peso, fecha_nacimiento, edad) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?)"
    _SELECCIONAR_X_CEDULA = "select id, cedula, nombre, apellido, email, carrera, activo, estatura, peso, fecha_nacimiento, edad from Estudiantes " \
                            "where cedula = ?"
    _SELECCIONAR = "select id, cedula, nombre, apellido, email, carrera, activo, estatura, peso, fecha_nacimiento, edad from Estudiantes where activo = 1"
    _N_EDADES = 'SELECT edad FROM Estudiantes'
    @classmethod
    def insertar_estudiante(cls, estudiante):
        respuesta = {"exito": False, "mensaje": ""}
        flag_exito = False
        mensaje = ""
        try:
            with Conexion.obtenerCursor() as cursor:
                datos = (estudiante.cedula, estudiante.nombre, estudiante.apellido, estudiante.email, estudiante.carrera
                         , estudiante.activo, estudiante.estatura, estudiante.peso, estudiante.fecha_nacimiento)
                cursor.execute(cls._INSERTAR, datos)
                edad = cls.calcular_edad(estudiante.fecha_nacimiento)
                cursor.execute("UPDATE Estudiantes SET edad = ? WHERE cedula = ?", (edad, estudiante.cedula))

                flag_exito = True
                mensaje = "INGRESO EXITOSO"
        except IntegrityError as e:
            flag_exito = False
            if e.__str__().find("Cedula") > 0:
                print("CEDULA YA INGRESADA.")
                mensaje = "cedula ya ingresada"
            elif e.__str__().find("Email") > 0:
                print("EMAIL YA INGRESADA.")
                mensaje = "email ya ingresada"
            else:
                print("ERROR DE INTEGRIDAD")
                mensaje = "Error de integridad"
        except ProgrammingError as e:
            flag_exito = False
            print("Los datos Ingresados no son del tamaño permitido")
            mensaje = "Los datos Ingresados no son del tamaño permitido"
        except Exception as e:
            flag_exito = False
            print(e)
        finally:
            respuesta["exito"] = flag_exito
            respuesta["mensaje"] = mensaje
            return respuesta

    @classmethod
    def seleccionar_por_cedula(cls, estudiante):
        persona_encontrada = None
        try:
            with Conexion.obtenerConexion() as cursor:
                datos = (estudiante.cedula,)
                resultado = cursor.execute(cls._SELECCIONAR_X_CEDULA, datos)
                persona_encontrada = resultado.fetchone()
                estudiante.email = persona_encontrada[4]
                estudiante.nombre = persona_encontrada[2]
                estudiante.apellido = persona_encontrada[3]
                estudiante.carrera = persona_encontrada[5]
                estudiante.activo = persona_encontrada[6]
                estudiante.cedula = persona_encontrada[1]
                estudiante.id = persona_encontrada[0]
                estudiante.estatura = persona_encontrada[7]
                estudiante.peso = persona_encontrada [8]
                estudiante.fecha_nacimiento = persona_encontrada[9]


        except Exception as e:
            print(e)
        finally:
            return estudiante
    @classmethod
    def seleccionar_estudiantes(cls):
        lista_estudiantes = list()
        try:
            with Conexion.obtenerCursor() as cursor:
                resultado = cursor.execute(cls._SELECCIONAR)
                registros = resultado.fetchall()
                #print(registros)
                for tupla_estudiante in registros:
                    #print(tupla_estudiante)
                    #if tupla_estudiante:
                    estudiante = Estudiante()
                    estudiante.id = tupla_estudiante[0]
                    estudiante.cedula = tupla_estudiante[1]
                    estudiante.nombre = tupla_estudiante[2]
                    estudiante.apellido = tupla_estudiante[3]
                    estudiante.email = tupla_estudiante[4]
                    estudiante.carrera = tupla_estudiante[5]
                    estudiante.activo = tupla_estudiante[6]
                    estudiante.estatura = tupla_estudiante[7]
                    estudiante.peso = tupla_estudiante[8]
                    estudiante.fecha_nacimiento = tupla_estudiante[9]
                    #print(estudiante)
                    lista_estudiantes.append(estudiante)
        except Exception as e:
            lista_estudiantes = None
            #print(e)
        finally:
            return lista_estudiantes

    @classmethod
    def calcular_edad(cls, fecha_nacimiento):
        try:
            birthdate = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
            today = date.today()  # Cambio: utiliza date.today() para obtener la fecha actual
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            return age
        except Exception as e:
            print(f'Error al calcular la edad: {str(e)}')
            return None

    @classmethod
    def obtener_edades_todos_estudiantes(cls):
        tedades = []
        try:
            with Conexion.obtenerCursor() as cursor:
                resultado = cursor.execute(cls._N_EDADES)
                tedades = [tupla_estudiante[0] for tupla_estudiante in resultado.fetchall()]
        except Exception as e:
            print(e)
        finally:
            return tedades


if __name__ == '__main__':
    #e1 = Estudiante()
    #e1.cedula = '0934843339'
    #e1.nombre = 'Juan'
    #e1.apellido = 'Cruz'
    #e1.email = 'jceuz@gmail.com'
    #e1.carrera = 'ADN'
    #e1.activo = True
    # EstudianteDao.insertar_estudiante(e1)
    #persona_encontrada = EstudianteDao.seleccionar_por_cedula(e1)
    #print(persona_encontrada)
    estudiantes = EstudianteDao.seleccionar_estudiantes()
    #print(estudiantes)
    for estudiante in estudiantes:
        print(estudiante)

        edad = EstudianteDao.calcular_edad(str(estudiante.fecha_nacimiento))
        if edad is not None:
            print(f"Edad: {edad}")
        else:
            print("Edad no disponible")