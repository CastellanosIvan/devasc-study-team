import sys
import mysql.connector
from mysql.connector import Error
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QLabel, QLineEdit, QTableWidget,
    QTableWidgetItem, QMessageBox, QDialog, QFormLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette

class CRUDWidget(QWidget):
    def __init__(self, table_name, columns, parent=None):
        super().__init__(parent)
        self.table_name = table_name
        self.columns = columns
        self.db_connection = parent.db_connection if parent and hasattr(parent, 'db_connection') else None
        self.setup_ui()
        if self.db_connection and self.db_connection.is_connected():
            self.load_data()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel(f"Administración de {self.table_name}")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Table view
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels(self.columns)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        layout.addWidget(self.table)
        
        # Form for add/edit
        self.form_layout = QFormLayout()
        self.inputs = {}
        
        for column in self.columns:
            self.inputs[column] = QLineEdit()
            self.form_layout.addRow(f"{column}:", self.inputs[column])
        
        layout.addLayout(self.form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Agregar")
        self.add_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.add_button.clicked.connect(self.add_record)
        
        self.edit_button = QPushButton("Editar")
        self.edit_button.setStyleSheet("background-color: #2196F3; color: white;")
        self.edit_button.clicked.connect(self.edit_record)
        
        self.delete_button = QPushButton("Eliminar")
        self.delete_button.setStyleSheet("background-color: #f44336; color: white;")
        self.delete_button.clicked.connect(self.delete_record)
        
        self.clear_button = QPushButton("Limpiar")
        self.clear_button.setStyleSheet("background-color: #FF9800; color: white;")
        self.clear_button.clicked.connect(self.clear_form)
        
        self.back_button = QPushButton("Regresar")
        self.back_button.setStyleSheet("background-color: #9E9E9E; color: white;")
        self.back_button.clicked.connect(self.go_back)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.back_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        # Connect table selection to form
        self.table.itemSelectionChanged.connect(self.table_selection_changed)
    
    def table_selection_changed(self):
        selected = self.table.selectedItems()
        if selected:
            row = selected[0].row()
            for i, column in enumerate(self.columns):
                self.inputs[column].setText(self.table.item(row, i).text())
    
    def load_data(self):
        if not self.db_connection or not self.db_connection.is_connected():
            QMessageBox.warning(self, "Error", "No hay conexión a la base de datos")
            return
            
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name}")
            data = cursor.fetchall()
            
            self.table.setRowCount(len(data))
            for row_idx, row_data in enumerate(data):
                for col_idx, col_data in enumerate(row_data):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
            
            self.table.resizeColumnsToContents()
        except Error as err:
            QMessageBox.critical(self, "Error", f"Error al cargar datos: {err}")
    
    def add_record(self):
        if not self.db_connection or not self.db_connection.is_connected():
            QMessageBox.warning(self, "Error", "No hay conexión a la base de datos")
            return
            
        try:
            cursor = self.db_connection.cursor()
            columns = ", ".join(self.columns)
            placeholders = ", ".join(["%s"] * len(self.columns))
            values = [self.inputs[col].text() for col in self.columns]
            
            query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(query, values)
            self.db_connection.commit()
            
            QMessageBox.information(self, "Éxito", "Registro agregado correctamente")
            self.load_data()
            self.clear_form()
        except Error as err:
            QMessageBox.critical(self, "Error", f"Error al agregar registro: {err}")
    
    def edit_record(self):
        if not self.db_connection or not self.db_connection.is_connected():
            QMessageBox.warning(self, "Error", "No hay conexión a la base de datos")
            return
            
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Advertencia", "Seleccione un registro para editar")
            return
            
        try:
            cursor = self.db_connection.cursor()
            row = selected[0].row()
            id_column = self.columns[0]
            
            set_clause = ", ".join([f"{col}=%s" for col in self.columns[1:]])
            values = [self.inputs[col].text() for col in self.columns[1:]]
            values.append(self.table.item(row, 0).text())
            
            query = f"UPDATE {self.table_name} SET {set_clause} WHERE {id_column}=%s"
            cursor.execute(query, values)
            self.db_connection.commit()
            
            QMessageBox.information(self, "Éxito", "Registro actualizado correctamente")
            self.load_data()
        except Error as err:
            QMessageBox.critical(self, "Error", f"Error al actualizar registro: {err}")
    
    def delete_record(self):
        if not self.db_connection or not self.db_connection.is_connected():
            QMessageBox.warning(self, "Error", "No hay conexión a la base de datos")
            return
            
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Advertencia", "Seleccione un registro para eliminar")
            return
            
        reply = QMessageBox.question(
            self, "Confirmar", 
            "¿Está seguro de que desea eliminar este registro?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                cursor = self.db_connection.cursor()
                row = selected[0].row()
                id_column = self.columns[0]
                id_value = self.table.item(row, 0).text()
                
                query = f"DELETE FROM {self.table_name} WHERE {id_column}=%s"
                cursor.execute(query, (id_value,))
                self.db_connection.commit()
                
                QMessageBox.information(self, "Éxito", "Registro eliminado correctamente")
                self.load_data()
                self.clear_form()
            except Error as err:
                QMessageBox.critical(self, "Error", f"Error al eliminar registro: {err}")
    
    def clear_form(self):
        for input_field in self.inputs.values():
            input_field.clear()
        self.table.clearSelection()
    
    def go_back(self):
        if self.parent() and hasattr(self.parent(), 'setCurrentIndex'):
            self.parent().setCurrentIndex(0)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión Comex")
        self.setFixedSize(900, 650)
        
        # Establecer color de fondo neutro
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
        self.setPalette(palette)
        
        self.db_connection = None
        self.init_ui()
        self.connect_to_database()  # Conexión automática al iniciar
        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.stacked_widget = QStackedWidget()
        
        # Página del menú principal
        menu_page = QWidget()
        menu_layout = QVBoxLayout()
        menu_layout.setContentsMargins(50, 50, 50, 50)
        menu_layout.setSpacing(20)
        
        title = QLabel("Sistema de Gestión Comex")
        title.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: #2c3e50;
            margin-bottom: 30px;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        menu_layout.addWidget(title)
        
        # Botones para cada tabla
        self.btn_categorias = QPushButton("Categorías")
        self.btn_articulos = QPushButton("Artículos")
        self.btn_clientes = QPushButton("Clientes")
        self.btn_ventas = QPushButton("Ventas")
        self.btn_detalle_ventas = QPushButton("Detalle de Ventas")
        self.btn_conectar = QPushButton("Reconectar a BD")
        
        # Estilos para los botones
        button_style = """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 15px;
                font-size: 16px;
                border-radius: 5px;
                min-width: 250px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """
        
        for btn in [
            self.btn_categorias, 
            self.btn_articulos, 
            self.btn_clientes,
            self.btn_ventas, 
            self.btn_detalle_ventas, 
            self.btn_conectar
        ]:
            btn.setStyleSheet(button_style)
            menu_layout.addWidget(btn)
        
        menu_layout.addStretch()
        menu_page.setLayout(menu_layout)
        
        # Añadir páginas al stacked widget
        self.stacked_widget.addWidget(menu_page)
        
        # Crear widgets CRUD para cada tabla
        self.categorias_widget = CRUDWidget("Categoria", ["idcategoria", "nombre"], self)
        self.articulos_widget = CRUDWidget(
            "Articulos", 
            ["codigo", "nombre", "precio", "costo", "existencia", "unidad", "idcategoria"], 
            self
        )
        self.clientes_widget = CRUDWidget(
            "Clientes", 
            ["telefono", "nombre", "direccion", "rfc", "correo"], 
            self
        )
        self.ventas_widget = CRUDWidget(
            "Ventas", 
            ["ventas", "fecha", "importe", "iva", "total", "telefono"], 
            self
        )
        self.detalle_ventas_widget = CRUDWidget(
            "Detalle_Ventas", 
            ["ventas", "codigo", "cantidad", "precio", "importe"], 
            self
        )
        
        self.stacked_widget.addWidget(self.categorias_widget)
        self.stacked_widget.addWidget(self.articulos_widget)
        self.stacked_widget.addWidget(self.clientes_widget)
        self.stacked_widget.addWidget(self.ventas_widget)
        self.stacked_widget.addWidget(self.detalle_ventas_widget)
        
        # Conectar botones a las páginas correspondientes
        self.btn_categorias.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.btn_articulos.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.btn_clientes.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.btn_ventas.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))
        self.btn_detalle_ventas.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(5))
        self.btn_conectar.clicked.connect(self.connect_to_database)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        central_widget.setLayout(main_layout)
    
    def connect_to_database(self):
        try:
            # Cerrar conexión existente si hay una
            if self.db_connection and self.db_connection.is_connected():
                self.db_connection.close()
            
            # Establecer nueva conexión con tus datos
            self.db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="mysql",
                database="comex"
            )
            
            # Verificar conexión
            if self.db_connection.is_connected():
                # Actualizar conexión en todos los widgets CRUD
                for i in range(1, self.stacked_widget.count()):
                    widget = self.stacked_widget.widget(i)
                    if hasattr(widget, 'db_connection'):
                        widget.db_connection = self.db_connection
                        widget.load_data()
                
                QMessageBox.information(
                    self, 
                    "Éxito", 
                    "¡Conectado a la base de datos Comex!\n"
                    "Host: localhost\n"
                    "Usuario: root"
                )
            else:
                QMessageBox.critical(self, "Error", "No se pudo establecer la conexión")
                
        except Error as err:
            error_msg = "Error de conexión:\n"
            
            if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                error_msg += "Usuario o contraseña incorrectos\n"
            elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                error_msg += "La base de datos 'comex' no existe\n"
            else:
                error_msg += f"Detalles: {err}\n"
            
            error_msg += "\nConfiguración usada:\n"
            error_msg += "Host: localhost\n"
            error_msg += "Usuario: root\n"
            error_msg += "Base de datos: comex"
            
            QMessageBox.critical(self, "Error", error_msg)
            self.db_connection = None
    
    def closeEvent(self, event):
        if self.db_connection and self.db_connection.is_connected():
            self.db_connection.close()
        event.accept()

def main():
    app = QApplication(sys.argv)
    
    # Establecer un estilo consistente
    app.setStyle("Fusion")
    
    # Configurar paleta de colores
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(233, 231, 227))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(76, 175, 80))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()