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

def authorization(self, cfg_data):
    current_profile = cfg_data.profiles["current_profile"]
    #if 