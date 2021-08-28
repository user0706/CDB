from PyQt5 import uic
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *
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
















class CheckableComboBox(QComboBox):
	def __init__(self):
		super().__init__()
		self._changed = False
		self.view().pressed.connect(self.handleItemPressed)

	def setItemChecked(self, index, checked=False):
		item = self.model().item(index, self.modelColumn()) # QStandardItem object
		if checked:
			item.setCheckState(Qt.Checked)
		else:
			item.setCheckState(Qt.Unchecked)

	def handleItemPressed(self, index):
		item = self.model().itemFromIndex(index)
		if item.checkState() == Qt.Checked:
			item.setCheckState(Qt.Unchecked)
		else:
			item.setCheckState(Qt.Checked)
		self._changed = True

	def hidePopup(self):
		if not self._changed:
			super().hidePopup()
		self._changed = False

	def getCheckedList(self, cb_items):
		return_list = []
		for index, value in enumerate(cb_items):
			item = self.model().item(index, self.modelColumn())
			if item.checkState() == Qt.Checked:
				return_list.append(value)
		return return_list


#Layout with floating elements
class FlowLayout(QLayout):
	def __init__(self, parent=None, margin=-1, hspacing=-1, vspacing=-1):
		super(FlowLayout, self).__init__(parent)
		self._hspacing = hspacing
		self._vspacing = vspacing
		self._items = []
		self.setContentsMargins(margin, margin, margin, margin)

	def __del__(self):
		del self._items[:]

	def addItem(self, item):
		self._items.append(item)

	def horizontalSpacing(self):
		if self._hspacing >= 0:
			return self._hspacing
		else:
			return self.smartSpacing(
				QStyle.PM_LayoutHorizontalSpacing)

	def verticalSpacing(self):
		if self._vspacing >= 0:
			return self._vspacing
		else:
			return self.smartSpacing(
				QStyle.PM_LayoutVerticalSpacing)

	def count(self):
		return len(self._items)

	def itemAt(self, index):
		if 0 <= index < len(self._items):
			return self._items[index]

	def takeAt(self, index):
		if 0 <= index < len(self._items):
			return self._items.pop(index)

	def expandingDirections(self):
		return Qt.Orientations(0)

	def hasHeightForWidth(self):
		return True

	def heightForWidth(self, width):
		return self.doLayout(QRect(0, 0, width, 0), True)

	def setGeometry(self, rect):
		super(FlowLayout, self).setGeometry(rect)
		self.doLayout(rect, False)

	def sizeHint(self):
		return self.minimumSize()

	def minimumSize(self):
		size = QSize()
		for item in self._items:
			size = size.expandedTo(item.minimumSize())
		left, top, right, bottom = self.getContentsMargins()
		size += QSize(left + right, top + bottom)
		return size

	def doLayout(self, rect, testonly):
		left, top, right, bottom = self.getContentsMargins()
		effective = rect.adjusted(+left, +top, -right, -bottom)
		x = effective.x()
		y = effective.y()
		lineheight = 0
		for item in self._items:
			widget = item.widget()
			hspace = self.horizontalSpacing()
			if hspace == -1:
				hspace = widget.style().layoutSpacing(
					QSizePolicy.PushButton,
					QSizePolicy.PushButton, Qt.Horizontal)
			vspace = self.verticalSpacing()
			if vspace == -1:
				vspace = widget.style().layoutSpacing(
					QSizePolicy.PushButton,
					QSizePolicy.PushButton, Qt.Vertical)
			nextX = x + item.sizeHint().width() + hspace
			if nextX - hspace > effective.right() and lineheight > 0:
				x = effective.x()
				y = y + lineheight + vspace
				nextX = x + item.sizeHint().width() + hspace
				lineheight = 0
			if not testonly:
				item.setGeometry(
					QRect(QPoint(x, y), item.sizeHint()))
			x = nextX
			lineheight = max(lineheight, item.sizeHint().height())
		return y + lineheight - rect.y() + bottom

	def smartSpacing(self, pm):
		parent = self.parent()
		if parent is None:
			return -1
		elif parent.isWidgetType():
			return parent.style().pixelMetric(pm, None, parent)
		else:
			return parent.spacing()