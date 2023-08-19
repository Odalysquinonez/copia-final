
from statistics import mode

from PySide6 import QtCore
from PySide6.QtCore import QDate
from PySide6.QtGui import QIntValidator, QRegularExpressionValidator
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox

from UI.Vtn_principal import Ui_VTNWindow
from datos.estudiante_dao import EstudianteDao
from dominio.Docente import Docente
from dominio.Estudiante import Estudiante


class PersonaPrincipal(QMainWindow):

    def __init__(self):
        super(PersonaPrincipal, self).__init__()
        self.ui = Ui_VTNWindow()
        self.ui.setupUi(self)
        self.ui.stb_menu_barra_estado.showMessage("Bienvenido", 2000)
        self.ui.btn_Grabar.clicked.connect(self.grabar)
        self.ui.txt_cedula.setValidator(QIntValidator())
        self.ui.btn_buscar_cedula.clicked.connect(self.buscar_x_cedula)
        self.ui.btn_calculo.clicked.connect(self.calculos_estatura)
        self.ui.btn_calculo.clicked.connect(self.calculos_peso)
        self.ui.btn_calculo.clicked.connect(self.calculos_edad)
        correo_exp = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        validator = QRegularExpressionValidator(correo_exp, self)
        self.ui.txt_email.setValidator(validator)



    def grabar(self):
        tipo_persona = self.ui.cb_tipo_persona.currentText()
        if not self.ui.txt_Nombre.text() or not self.ui.txt_Apellido.text() \
                or len(self.ui.txt_cedula.text()) < 10 or not self.ui.txt_email.text():
            print("Completar Datos")
            QMessageBox.warning(self, 'Advertencia', 'Falta de llenar los datos obligatorios')
            return

        persona = None
        if tipo_persona == "Docente":
            persona = Docente()
        else:
            persona = Estudiante()

        persona.nombre = self.ui.txt_Nombre.text()
        persona.apellido = self.ui.txt_Apellido.text()
        persona.cedula = self.ui.txt_cedula.text()
        persona.email = self.ui.txt_email.text()
        persona.carrera = self.ui.txt_carrera.text()
        persona.estatura = self.ui.sp_estatura_2.value()
        persona.peso = self.ui.sp_peso.value()
        persona.fecha_nacimiento = self.ui.date_fecha_nacimiento.date().toString("yyyy-MM-dd")



        respuesta = None
        try:
            respuesta = EstudianteDao.insertar_estudiante(persona)
        except Exception as e:
            print(e)

        if respuesta and respuesta['exito']:
            self.ui.txt_Nombre.clear()
            self.ui.txt_Apellido.clear()
            self.ui.txt_cedula.clear()
            self.ui.txt_email.clear()
            self.ui.txt_carrera.clear()
            self.ui.sp_estatura_2.setValue(0)
            self.ui.date_fecha_nacimiento.setDate(QtCore.QDate())
            self.ui.sp_peso.setValue(0)
            self.ui.stb_menu_barra_estado.showMessage("Grabado con Éxito", 2000)
        else:
            QMessageBox.critical(self, 'Error', respuesta['mensaje'])

    def buscar_x_cedula(self):
        cedula = self.ui.txt_cedula.text()
        e = Estudiante(cedula=cedula)
        e = EstudianteDao.seleccionar_por_cedula(e)
        self.ui.txt_Nombre.setText(e.nombre)
        self.ui.txt_Apellido.setText(e.apellido)
        self.ui.txt_email.setText(e.email)
        self.ui.txt_carrera.setText(e.carrera)
        self.ui.cb_tipo_persona.setCurrentText('Estudiante')
        self.ui.sp_estatura_2.setValue(e.estatura)
        fecha_nacimiento = e.fecha_nacimiento
        year = fecha_nacimiento.year
        month = fecha_nacimiento.month
        day = fecha_nacimiento.day
        self.ui.date_fecha_nacimiento.setDate(QDate(year, month, day))
        self.ui.sp_peso.setValue(e.peso)


    def calculos_estatura(self):
        estudiantes = EstudianteDao.seleccionar_estudiantes()
        cantidad_estudiantes = len(estudiantes)
        suma_estaturas = sum(estudiante.estatura for estudiante in estudiantes)
        estaturas = [estudiante.estatura for estudiante in estudiantes]
        promedio_estatura = suma_estaturas / cantidad_estudiantes
        media_estatura = sorted(estaturas)[cantidad_estudiantes // 2]
        moda_estatura = mode(estaturas)
        minimo_estatura = min(estaturas)
        maximo_estatura = max(estaturas)

        print('')
        print(f'------------ESTATURA---------------------')
        print(f'Promedio de estaturas: {promedio_estatura}')
        print(f'Media de estaturas: {media_estatura}')
        print(f'Moda de estaturas: {moda_estatura}')
        print(f'Mínimo de estaturas: {minimo_estatura}')
        print(f'Máximo de estaturas: {maximo_estatura}')

    def calculos_peso(self):
        estudiantes = EstudianteDao.seleccionar_estudiantes()
        cantidad_estudiantes = len(estudiantes)
        suma_pesos = sum(estudiante.peso for estudiante in estudiantes)
        pesos = [estudiante.peso for estudiante in estudiantes]
        promedio_peso = suma_pesos / cantidad_estudiantes
        media_peso = sorted(pesos)[cantidad_estudiantes // 2]
        moda_peso = mode(pesos)
        minimo_peso = min(pesos)
        maximo_peso = max(pesos)

        print('')
        print('------------PESO---------------------')
        print(f'Promedio de pesos: {promedio_peso}')
        print(f'Media de pesos: {media_peso}')
        print(f'Moda de pesos: {moda_peso}')
        print(f'Mínimo de pesos: {minimo_peso}')
        print(f'Máximo de pesos: {maximo_peso}')

    def calculos_edad(self):

        edades = EstudianteDao.obtener_edades_todos_estudiantes()

        if edades is None or len(edades) == 0:
            print("No se obtuvieron edades.")
            return


        edades_validas = [edad for edad in edades if edad is not None]

        if not edades_validas:
            print("No hay edades válidas para calcular promedio.")
            return

        suma_edades = sum(edades_validas)
        cantidad_edades = len(edades_validas)
        promedio_edades = suma_edades / cantidad_edades

        if len(edades_validas) > 1:
            moda_edades = max(set(edades_validas), key=edades_validas.count)

        else:
            moda_edades = edades_validas[0]


        maximo_edades = max(edades_validas)
        minimo_edades = min(edades_validas)

        print('')
        print("\n---------- CALCULOS DE EDAD -------------")
        print(f'- Total de edades      : {suma_edades}')
        print(f'- La media de edades   : {promedio_edades:,.2f}')
        print(f'- La moda de edades    : {moda_edades}')
        print(f'- El mínimo de edades  : {minimo_edades}')
        print(f'- El máximo de edades  : {maximo_edades}')


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mainWindow = PersonaPrincipal()
    mainWindow.show()
    sys.exit(app.exec())
