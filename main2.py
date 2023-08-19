import sys
from PySide6.QtWidgets import QApplication
from servicio.persona_principal import PersonaPrincipal

app = QApplication(sys.argv)
vtn_principal: PersonaPrincipal = PersonaPrincipal()
vtn_principal.show()
sys.exit(app.exec())
