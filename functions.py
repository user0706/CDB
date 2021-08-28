from PyQt5 import uic
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *
from myqt import *
import sys
import main
import json

class Bunch(dict):
	'''
	:Bunch je identicno kao i dict sa razlikom sto su elementi kod dict, objekti kod Bunch
	:Primer => test['a'] je isto kao i test.a
	'''
	def __init__(self, *args, **kws):
		super(Bunch, self).__init__(*args, **kws)
		self.__dict__ = self

def updateComboBox(cb, cb_items, layout):
	'''
	:Dodavanje checkbox elemenata u combobox
	'''
	for i, v in enumerate(cb_items):
		cb.addItem(str(v))
		item = cb.model().item(i,0)
		item.setCheckState(Qt.Unchecked)
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