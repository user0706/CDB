# This Python file uses the following encoding: utf-8
from PyQt5 import uic
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *
from myqt import *
import sys

from functions import *

SELECTED_PHOTO_PATH = ""
SELECTED_MSDS_PATH = ""
DATA_PATH = ""

item_changed_template = ""

class Ui(QMainWindow):
	def __init__(self):
		super(Ui, self).__init__()
		uic.loadUi('mainwindow.ui', self)

		self.splitter.setSizes([800,280])
		setProfilesToComboBox(self)
		self.lineEdit_current_password.setEchoMode(QLineEdit.Password)
		self.lineEdit_new_password.setEchoMode(QLineEdit.Password)
		self.lineEdit_login_password.setEchoMode(QLineEdit.Password)
		self.actionConfiguration.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(2))
		self.actionLog_Out.triggered.connect(lambda: onLogout(self))
		self.pushButton_cancel.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
		self.pushButton_log_out.clicked.connect(lambda: onLogout(self))
		self.pushButton_add_data_path.clicked.connect(lambda: onAddDataPath(self))
		self.pushButton_apply.clicked.connect(lambda: onApplay(self, app))
		self.pushButton_login.clicked.connect(lambda: onLogin(self))

		setCFG(self, app)

		# RIGHT AREA
		item_data_template = Bunch({"photo_path": "","item_name":"","manufacturer_name":"","item_location":"","current_quantity":"","quantity_per_package":"","supplier":"","distributor":"","more_info":"","keywords":[],"msds_path":"","safety_labels":{"prohibition":[],"warning":[],"mandatory":[],"emergency":[],"firefighting":[],"chemical":[]}})
		prohibitionList = ["No access for unauthorised persons","Smoking and naked flames forbidden","No smoking","No access for pedestrians","Not drinkable","Do not extinguish with water","No access for industrial vehicles","Do not touch"]
		warningList = ["a","b","b"]
		mandatoryList = ["a","b","b"]
		emergencyList = ["a","b","b"]
		firefightingList = ["a","b","b"]
		chemicalList = ["a","b","b"]

		self.prohibitionComboBox = CheckableComboBox()
		self.warningComboBox = CheckableComboBox()
		self.mandatoryComboBox = CheckableComboBox()
		self.emergencyComboBox = CheckableComboBox()
		self.firefightingComboBox = CheckableComboBox()
		self.chemicalComboBox = CheckableComboBox()

		updateComboBox(self.prohibitionComboBox, prohibitionList, self.verticalLayout_Prohibition)
		updateComboBox(self.warningComboBox, warningList, self.verticalLayout_Warning)
		updateComboBox(self.mandatoryComboBox, mandatoryList, self.verticalLayout_Mandatory)
		updateComboBox(self.emergencyComboBox, emergencyList, self.verticalLayout_Emergency)
		updateComboBox(self.firefightingComboBox, firefightingList, self.verticalLayout_Firefighting)
		updateComboBox(self.chemicalComboBox, chemicalList, self.verticalLayout_Chemical)

		self.toolButton_add_photo.clicked.connect(lambda: onAddPhoto(self))
		self.toolButton_upload_msds.clicked.connect(lambda: onMSDSPath(self))
		self.pushButton_submit.clicked.connect(lambda: onSubmit(self,
																(self.prohibitionComboBox, prohibitionList),
																(self.warningComboBox, warningList),
																(self.mandatoryComboBox, mandatoryList),
																(self.emergencyComboBox, emergencyList),
																(self.firefightingComboBox, firefightingList),
																(self.chemicalComboBox, chemicalList),
																item_data_template))


		# LEFT AREA
		data = loadData()
		self.layout = FlowLayout(self.widget_items)
		for key, value in data.items():
			item_card = YooHoo(value["photo_path"], value["item_name"])
			self.layout.addWidget(item_card)

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = Ui()
	window.show()
	app.exec_()
