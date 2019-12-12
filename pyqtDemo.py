import math
import sys

from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLineEdit, QInputDialog, QFileDialog, QMessageBox
from PyQt5 import QtWidgets
import pandas as pd

from PyQt5.QtCore import QStringListModel

import freight
import calculationFreight



class pyQt(QtWidgets.QMainWindow):


    def __init__(self):
        super(pyQt, self).__init__()
        self.InitUI()

        self.countryPrice = {}  # 定义一个国家运费对应的字典

    def InitUI(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = freight.Ui_MainWindow()
        self.ui.setupUi(self)  # 像自己在日自己
        self.ui.label.setText('运费为:')


        self.countryList = ['法国','意大利','德国','英国','波兰','美国','俄罗斯','巴西','西班牙','澳大利亚','加拿大','荷兰','芬兰',
                            '捷克','斯洛伐克','挪威','葡萄牙','俄罗斯','瑞士','丹麦','比利时','奥地利','匈牙利']

        self.ui.pushButton.clicked.connect(self.onButtonClicked)
        self.ui.pushButton_2.clicked.connect(self.onButton_2Clicked)

    def onButtonClicked(self):
        # text_country = self.ui.lineEdit.text()
        # # print('text_country', text_country)
        # text_weight = self.ui.lineEdit_2.text()
        # print('text_weight', text_weight)
        # print('lineEdit', self.ui.lineEdit.text())
        # if self.ui.lineEdit.text() is '':
        #     print('showDialog')
        #     self.showDialog('国家或重量不能为空')
        #     return

        if self.ui.lineEdit_2.text() is '':
            print('showDialog')
            self.showDialog('重量不能为空')
            return

        # text_country = self.ui.lineEdit.text()
        # print('text_country', text_country)

        text_weight = self.ui.lineEdit_2.text()
        print('text_weight', text_weight)
        print('self.currentSheetName', self.currentSheetName)

        if self.currentSheetName:

            # self.getCommonCountriesCPingYouPrice(float(text_weight))
            self.getPrice(self.currentSheetName,float(text_weight))

            # price = self.getPrice(self.currentSheetName, text_country, float(text_weight))
            # print('getprice', price)
            # if price:
            #     self.ui.label.setText('运费为:' + price)
            #     self.ui.label_5.setText('计算成功:国家-' + str(text_country) + ",重量-" + str(text_weight))


    def onButton_2Clicked(self):
        self.fileName, filetype = QFileDialog.getOpenFileName(self,
                                                          "选取文件",
                                                          "./",
                                                          "All Files (*.xlsx);;Text Files (*.txt)")  # 设置文件扩展名过滤,注意用双分号间隔
        if self.fileName:
            self.ui.label_6.setText(self.fileName)
            print(self.fileName, filetype)
            self.getExcelAllSheets()


    def getExcelAllSheets(self):
        self.excel_data = pd.read_excel(self.fileName, None)  # 读取数据,设置None可以生成一个字典，字典中的key值即为sheet名字，此时不用使用DataFram，会报错
        print(self.excel_data.keys())
        self.setComboBoxData(self.excel_data.keys())

    def setComboBoxData(self, data):
        # 下拉框的数据
        # self.ui.comboBox.setItemData(self,0,data)
        self.ui.comboBox.addItems(data)
        self.ui.comboBox.setCurrentIndex(1)  # 设置默认值
        self.ui.comboBox.currentText()  # 获得当前内容
        print('select combox',self.ui.comboBox.currentText())
        self.currentSheetName = self.ui.comboBox.currentText()  # 在这里给combobox一个默认值
        self.ui.comboBox.currentIndexChanged.connect(self.onComboBoxCurrentIndexChanged)

    def onComboBoxCurrentIndexChanged(self):
        print('select combox', self.ui.comboBox.currentText())
        self.currentSheetName = self.ui.comboBox.currentText()


    def showDialog(self, message):
        # reply = QMessageBox.question(self, '提示', message,
        #                              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        reply = QMessageBox.question(self, '提示', message,
                                     QMessageBox.Ok)
        if reply == QMessageBox.Yes:
            # event.accept()
            pass
        else:
            # event.ignore()
            pass

    def getPrice(self, sheetName, weight):
        if 'C平邮' not in str(sheetName):
            self.showDialog('请选择燕文c平邮渠道')
            return

        if 'C平邮' in str(sheetName):
            return self.getCommonCountriesCPingYouPrice(weight)

    def getCPingYouPrice(self,sheetName, country, weight):
        if sheetName in self.excel_data.keys():
            sheet_data = pd.DataFrame(pd.read_excel(self.fileName, sheetName))  # 获得每一个sheet中的内容
            # print(sheet_data)
            # print(sheet_data['WISH燕文C平邮小包'])

            if sheet_data.loc[sheet_data[sheetName] == country] is None:
                self.showDialog('没找到国家为--%s', country)
                return
            print(sheet_data.loc[sheet_data[sheetName] == country])
            print(sheet_data.loc[sheet_data[sheetName] == country]['Unnamed: 3'])

            price = 0
            start_price = float(sheet_data.loc[sheet_data[sheetName] == country]['Unnamed: 1'])
            unit_price_30_80 = float(sheet_data.loc[sheet_data[sheetName] == country]['Unnamed: 2']) / 1000
            unit_price_80_2k = float(sheet_data.loc[sheet_data[sheetName] == country]['Unnamed: 3']) / 1000

            print('start_price=', start_price)
            if weight <= 30:
                price = start_price
                print(price)
            elif weight > 30 and weight <= 80:
                price = start_price + (weight - 30) * unit_price_30_80
                print(price)
            elif weight > 80:
                price = start_price + 50 * unit_price_30_80 + (weight - 80) * unit_price_80_2k
                print(price)
            print('getprice', str(math.ceil(price)))
            # return str(math.ceil(price))

            self.countryPrice[str(country)] = str(math.ceil(price))
            return str(country) + '---' + str(weight) + 'g---' + str(math.ceil(price))

    def getCommonCountriesCPingYouPrice(self,text_weight):  #  获取常见国家的c 平邮运费

        slm = QStringListModel()
        self.qList = []
        for country in self.countryList:
            info = self.getCPingYouPrice(self.currentSheetName,country,float(text_weight))
            self.qList.append(info)
        print('qlist',self.qList)
        slm.setStringList(self.qList)  # 将数据设置到model
        self.ui.listView.setModel(slm)  ##绑定 listView 和 model

        max_prices_country = max(zip(self.countryPrice.values(), self.countryPrice.keys()))

        print('sum(self.countryPrice.values())', self.get_average(self.countryPrice.values()))

        # average_price_country = math.ceil(sum(self.countryPrice.values()) / len(self.countryList))
        self.ui.label.setText('运费平均值为:' + str(self.get_average(self.countryPrice.values())))
        self.ui.label_5.setText('运费最大值:国家--' + str(max_prices_country[1]) + ",金额为--"
                                + str(max_prices_country[0]) + "重量为--"+str(text_weight) + "g")

    def get_average(self, list):
        sum = 0
        for item in list:
            sum += float(item)
        return sum / len(list)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # ex = Demo()
    form = pyQt()
    form.show()  #
    sys.exit(app.exec_())