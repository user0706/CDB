from PyQt5 import uic
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *
import sys
import json
from functions import *

#####################
## CHANGE PASSWORD ##
#####################
def passwordMsg(msg_text, sub_msg_text):
	msg = QMessageBox()
	msg.setIcon(QMessageBox.Information)
	
	msg.setText(msg_text)
	msg.setInformativeText(sub_msg_text)
	msg.setWindowTitle("Password status")
	msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
	msg.exec_()


def changeProfilePassword(self, cfg_data):
	current_profile = str(self.comboBox_profile.currentText())
	if self.lineEdit_current_password.text()=="" and self.lineEdit_new_password.text()=="":
		pass
	else:
		if self.lineEdit_current_password.text()==cfg_data.profiles[current_profile.lower()]["password"] and self.lineEdit_new_password.text().strip()!="":
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

###################
## AUTHORIZATION ##
###################
def loadAuthority():
	with open('lib/authority.json', 'r', encoding='utf-8') as json_file:
		data = json.load(json_file)
	return data

def setProfilesToComboBox(self):
    authority_data = loadAuthority()
    profile_list = authority_data.keys()
    self.comboBox_login_profiles.clear()
    self.comboBox_profile.clear()
    self.comboBox_login_profiles.addItems(profile_list)
    self.comboBox_profile.addItems(profile_list)

def authorization(self, current_profile):
    authority_data = loadAuthority()
    authority_profile = authority_data[current_profile]
    self.toolButton_add_photo.setEnabled(authority_profile["add_photo"])
    self.toolButton_open_photo_location.setEnabled(authority_profile["open_photo_location"])
    self.lineEdit_item_name.setEnabled(authority_profile["item_name"])
    self.lineEdit_manufacturer.setEnabled(authority_profile["manufacturer"])
    self.lineEdit_item_location.setEnabled(authority_profile["item_location"])
    self.doubleSpinBox_quantity.setEnabled(authority_profile["quantity"])
    self.lineEdit_quantity_per_package.setEnabled(authority_profile["quantity_per_package"])
    self.lineEdit_supplier.setEnabled(authority_profile["supplier"])
    self.lineEdit_distributor.setEnabled(authority_profile["distributor"])
    self.lineEdit_more_info.setEnabled(authority_profile["more_info"])
    self.lineEdit_keywords.setEnabled(authority_profile["keywords"])
    self.lineEdit_msds_path.setEnabled(authority_profile["msds_path"])
    self.toolButton_upload_msds.setEnabled(authority_profile["upload_msds"])
    self.toolButton_open_msds_in_folder.setEnabled(authority_profile["open_msds_in_folder"])
    self.pushButton_submit.setEnabled(authority_profile["submit"])
    self.pushButton_delete.setEnabled(authority_profile["delete"])
    self.widget_prohibition.setEnabled(authority_profile["prohibition"])
    self.frame_warning.setEnabled(authority_profile["warning"])
    self.frame_mandatory.setEnabled(authority_profile["mandatory"])
    self.frame_emergency.setEnabled(authority_profile["emergency"])
    self.frame_firefighting.setEnabled(authority_profile["firefighting"])
    self.frame_chemical.setEnabled(authority_profile["chemical"])
    self.actionConfiguration.setEnabled(authority_profile["configuration"])
    self.groupBox_initialization.setEnabled(authority_profile["initialisation"])
    self.groupBox_profiles.setEnabled(authority_profile["profiles"])
    self.groupBox_style.setEnabled(authority_profile["style"])
