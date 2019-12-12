# 用于计算燕文wish-c平邮国际运费-避免出错
# 义乌燕文WISH报价单20191025版.xlsx
#coding:gbk

import openpyxl
import pandas as pd
import math

path = '义乌燕文WISH报价单20191025版.xlsx'

def getPrice(country, weight):
    excel_data = pd.read_excel(path, None)  # 读取数据,设置None可以生成一个字典，字典中的key值即为sheet名字，此时不用使用DataFram，会报错

    # print(excel_data.keys())
    # print(len(excel_data.keys()))
    columns_length = len(excel_data.keys())  # 获取列的长度

    if 'WISH燕文C平邮小包' in excel_data.keys():
        sheet_data = pd.DataFrame(pd.read_excel(path, 'WISH燕文C平邮小包'))  # 获得每一个sheet中的内容
        # print(sheet_data)
        # print(sheet_data['WISH燕文C平邮小包'])
        print(sheet_data.loc[sheet_data['WISH燕文C平邮小包'] == country])
        print(sheet_data.loc[sheet_data['WISH燕文C平邮小包'] == country]['Unnamed: 3'])

        price = 0
        start_price = float(sheet_data.loc[sheet_data['WISH燕文C平邮小包'] == country]['Unnamed: 1'])
        unit_price_30_80 = float(sheet_data.loc[sheet_data['WISH燕文C平邮小包'] == country]['Unnamed: 2']) / 1000
        unit_price_80_2k = float(sheet_data.loc[sheet_data['WISH燕文C平邮小包'] == country]['Unnamed: 3']) / 1000

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
        return str(math.ceil(price))

if __name__ == '__main__':
    for i in range(5):
        country = input("请输入国家:")
        print(country)
        weight = input("请输入重量(单位g):")
        print(weight)
        print('价格为:', getPrice(country, float(weight)))
