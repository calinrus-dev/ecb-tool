from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize


def normal_button(text, object_name):
	button = QPushButton(text)
	button.setObjectName(object_name)
	button.setFixedSize(200, 100)
	return button


def action_button(text, object_name):
	button = QPushButton(text)
	button.setObjectName(object_name)
	button.setFixedSize(200, 100)
	button.setStyleSheet(
		"QPushButton { width: 200px; height: 100px; border: none; border-radius: 20px; color: white; "
		"font-size: 20px; font-weight: bold; letter-spacing: 1px; padding: 20px; }"
		"QPushButton#run_button { background-color: #2196F3; }"
		"QPushButton#run_button:hover { background-color: #1976D2; }"
		"QPushButton#stop_button { background-color: #F44336; }"
		"QPushButton#stop_button:hover { background-color: #D32F2F; }"
		"QPushButton#save_button { background-color: #4CAF50; }"
		"QPushButton#save_button:hover { background-color: #388E3C; }"
		"QPushButton#close_button { background-color: #FF9800; }"
		"QPushButton#close_button:hover { background-color: #F57C00; }"
		"QPushButton#import_button { background-color: #9C27B0; }"
		"QPushButton#import_button:hover { background-color: #7B1FA2; }"
		"QPushButton#generate_button { background-color: #03A9F4; }"
		"QPushButton#generate_button:hover { background-color: #0288D1; }"
	)
	return button


def large_button(text, object_name):
	button = QPushButton(text)
	button.setObjectName(object_name)
	button.setFixedSize(250, 120)
	button.setStyleSheet(
		"QPushButton { width: 250px; height: 120px; border: none; border-radius: 25px; color: white; "
		"font-size: 22px; font-weight: bold; letter-spacing: 1px; padding: 25px; }"
		"QPushButton#large_button { background-color: #FF5722; }"
		"QPushButton#large_button:hover { background-color: #D84315; }"
	)
	return button


def small_button(text, object_name):
	button = QPushButton(text)
	button.setObjectName(object_name)
	button.setFixedSize(150, 80)
	button.setStyleSheet(
		"QPushButton { width: 150px; height: 80px; border: none; border-radius: 15px; color: white; "
		"font-size: 16px; font-weight: bold; letter-spacing: 1px; padding: 15px; }"
		"QPushButton#small_button { background-color: #8BC34A; }"
		"QPushButton#small_button:hover { background-color: #689F38; }"
	)
	return button


def icon_button(text, object_name, icon_path):
	button = QPushButton(text)
	button.setObjectName(object_name)
	button.setFixedSize(200, 100)
	button.setStyleSheet(
		"QPushButton { width: 200px; height: 100px; border: none; border-radius: 20px; color: white; "
		"font-size: 18px; font-weight: bold; letter-spacing: 1px; }"
		"QPushButton#icon_button { background-color: #607D8B; }"
		"QPushButton#icon_button:hover { background-color: #455A64; }"
	)
	button.setIconSize(QSize(30, 30))
	button.setIcon(QIcon(icon_path))
	return button


__all__ = [
	"normal_button",
	"action_button",
	"large_button",
	"small_button",
	"icon_button",
]
