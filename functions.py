from PyQt5 import uic
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *
from myqt import *
import sys
import main
import json
import qdarkstyle

# NOTE: dotati zastitu ako se ne izabere data file da se zadrzi prethodna putanja

class Bunch(dict):
	'''
	:Bunch je identicno kao i dict sa razlikom sto su elementi kod dict, objekti kod Bunch
	:Primer => test['a'] je isto kao i test.a
	'''
	def __init__(self, *args, **kws):
		super(Bunch, self).__init__(*args, **kws)
		self.__dict__ = self

#################
## MAIN SCREEN ##
#################

def updateComboBox(cb, cb_items, layout):
	'''
	:Dodavanje checkbox elemenata u combobox
	'''
	for i, v in enumerate(cb_items):
		cb.addItem(str(v))
		item = cb.model().item(i,0)
		item.setCheckState(False)
	layout.addWidget(cb)

def onAddPhoto(self):
	main.SELECTED_PHOTO_PATH = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Image files (*.jpg *.png)")[0]
def onMSDSPath(self):
	main.SELECTED_MSDS_PATH = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Image files (*.pdf)")[0]

def loadData():
	with open('lib/data.json') as json_file:
		data = json.load(json_file)
	return data
def getCardData():
	data = loadData()
	return data.keys()

class YooHoo(QToolButton):
	def __init__(self, photo, name): #fields je lista Qt lineEdit objekata na koje se ispisuju info iy baye
		super(YooHoo, self).__init__()
		self.setText(name)
		self.setIconSize(QSize(100, 100));
		self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
		self.setIcon(QIcon(photo))
		self.setCursor(QCursor(Qt.PointingHandCursor))
		self.clicked.connect(lambda: self.onClick(self.item_id, self.fields))

def onSubmit(self, prohibition,warning,mandatory,emergency,firefighting,chemical, template):
	template.photo_path = main.SELECTED_MSDS_PATH
	template.item_name = self.lineEdit_item_name.text()
	template.manufacturer_name = self.lineEdit_manufacturer.text()
	template.item_location = self.lineEdit_item_location.text()
	template.current_quantity = self.doubleSpinBox_quantity.value()
	template.quantity_per_package = self.lineEdit_quantit_per_package.text()
	template.supplier = self.lineEdit_supplier.text()
	template.distributor = self.lineEdit_distributor.text()
	template.more_info = self.lineEdit_more_info.text()
	template.keywords = [i.lstrip().rstrip() for i in self.lineEdit_keywords.text().split(",")]
	template.msds_path = main.SELECTED_MSDS_PATH
	template.safety_labels["prohibition"] = prohibition[0].getCheckedList(prohibition[1])
	template.safety_labels["warning"] = warning[0].getCheckedList(warning[1])
	template.safety_labels["mandatory"] = mandatory[0].getCheckedList(mandatory[1])
	template.safety_labels["emergency" ]= emergency[0].getCheckedList(emergency[1])
	template.safety_labels["firefighting"] = firefighting[0].getCheckedList(firefighting[1])
	template.safety_labels["chemical"] = chemical[0].getCheckedList(chemical[1])

	print(template)

##########################
## CONFIGURATION SCREEN ##
##########################

def dataPathOption(self):
	if self.radioButton_local.isChecked():
		return "Local"
	elif self.radioButton_url.isChecked():
		return "URL"
	#elif self.radioButton_api.isChecked():
	#	return "API"

def loadCFG():
	with open('lib/cfg.json', 'r', encoding='utf-8') as json_file:
		data = json.load(json_file)
	return data

def writeCFG(data):
	with open('lib/cfg.json', 'w', encoding='utf-8') as f:
		json.dump(data, f, ensure_ascii=False, indent=4)

def setCFG(self, app):
	cfg_data = Bunch(loadCFG())
	path_option = cfg_data.initialisation["path_option"]
	if path_option == "Local":
		self.radioButton_local.setChecked(True)
	elif path_option == "URL":
		self.radioButton_url.setChecked(True)
	#elif path_option == "API":
	#	self.radioButton_api.setChecked(True)

	# Set profile to memorised one
	self.comboBox_profile.setCurrentIndex([self.comboBox_profile.itemText(i) for i in range(self.comboBox_profile.count())].index(cfg_data.profiles["current_profile"]))

	# Set data path to memorised one
	self.lineEdit_data_path.setText(cfg_data.initialisation["path"])

	# Set theme to memorised one
	self.comboBox_theme.setCurrentIndex([self.comboBox_theme.itemText(i) for i in range(self.comboBox_theme.count())].index(cfg_data.style["theme"]))
	onTheme(self, app)

def onAddDataPath(self):
	data_path = QFileDialog.getOpenFileName(self, 'Open file', self.lineEdit_data_path.text(),"JSON file (*.json)")[0]
	self.lineEdit_data_path.setText(data_path)
	main.DATA_PATH = data_path

def passwordMsg(msg_text, sub_msg_text):
	print("tu sam")
	msg = QMessageBox()
	msg.setIcon(QMessageBox.Information)
	
	msg.setText(msg_text)
	msg.setInformativeText(sub_msg_text)
	msg.setWindowTitle("Password status")
	msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
	msg.exec_()


def changeProfilePassword(self, cfg_data):
	current_profile = str(self.comboBox_profile.currentText())
	if self.lineEdit_current_password.text()==None and self.lineEdit_new_password.text()==None:
		pass
	elif self.lineEdit_current_password.text()==cfg_data.profiles[current_profile.lower()]["password"] and self.lineEdit_new_password.text().strip()!="":
		msg_text = "Password has been changed seccesfuly."
		sub_msg_text = "The password for the {} profile was changed successfully.".format(str(self.comboBox_profile.currentText()))
		cfg_data.profiles[current_profile.lower()]["password"]=self.lineEdit_new_password.text()
	elif self.lineEdit_current_password.text()==cfg_data.profiles[current_profile.lower()]["password"] and self.lineEdit_new_password.text().strip()=="":
		msg_text = "Password has not changed."
		sub_msg_text = "The new password must not be a space or a blank field."
	elif self.lineEdit_current_password.text()!=cfg_data.profiles[current_profile.lower()]["password"]:
		msg_text = "Password has not changed."
		sub_msg_text = "The current password entered is incorrect."
	else:
		print("error")
	
	passwordMsg(msg_text, sub_msg_text)
	return cfg_data

def onTheme(self, app):
	selected_theme = self.comboBox_theme.currentText()
	if selected_theme=="Light":
		app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5', palette=qdarkstyle.light.palette.LightPalette))
	if selected_theme=="Dark":
		app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5', palette=qdarkstyle.dark.palette.DarkPalette))
	if selected_theme=="System":
		app.setStyleSheet(qdarkstyle._apply_os_patches(palette=qdarkstyle.light.palette.LightPalette))
	
	return selected_theme
		

def onApplay(self, app):
	cfg_data = Bunch(loadCFG())
	cfg_data.initialisation["path_option"] = dataPathOption(self)
	cfg_data.initialisation["path"] = self.lineEdit_data_path.text()
	#cfg_data.initialisation["language"] = str(self.comboBox_language.currentText())
	#cfg_data.initialisation["date_format"] = str(self.comboBox_data_format.currentText())
	cfg_data.profiles["current_profile"] = str(self.comboBox_profile.currentText())
	cfg_data = changeProfilePassword(self, cfg_data)
	cfg_data.style["theme"] = onTheme(self, app)

	writeCFG(cfg_data)

	print(cfg_data)