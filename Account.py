"""
รายงานความคืบหน้า Term Project 2

นายธณรัฐ เพียรชัยภูมิ 643040011-1
นายพีระณัฐ ศรีสรรพ์ 643040249-8
นางสาวภูริชญดา สนิทชน 643040251-1
"""
import csv
import pandas as pd
import tabulate
import numpy as np
import os
import matplotlib.pyplot as plt
import datetime as dt


class openAccount:


    # ฟังก์ชั่นหลัก
    def choice(self, choose, file_name):
        if choose == 1:
            print('พิมพ์วันที่และจำนวนเงินที่ต้องการ\n'
                  'โดยพิมพ์รูปแบบนี้ ตัวอย่าง\n'
                  'วันที่: 25/3/2022 คือ วันที่ 25 เดือน 3 ปี ค.ศ.2022\n'
                  'หากต้องการบันทึกเป็นวันที่ปัจจุบันพิมพ์ td\n'
                  'เงิน: +200 คือรายรับ 200\n'
                  '    -300 คือรายจ่าย 300\n'
                  'หากจะยกเลิกให้พิมพ์ pass ในช่อง วันที่ต้องการบันทึก')
            day = input('วันที่ต้องการบันทึก :')
            try:
                if day != 'pass':
                    if day.lower() == 'td':
                        day = dt.date.today()
                    else:
                        day = self.date_create(day)
                    money = int(input('จำนวนเงิน :'))
                    description = input('รายละเอียด :')
                else:
                    print(" ")
                    pass
                self.incomeOutcome(day, money, description, file_name)
            except:
                pass
        elif choose == 2:
            print('ต้องการตรวจสอบยอดเป็นรายวันพิมพ์ 1\n'
                  'ต้องการตรวจสอบยอดเป็นรายเดือนพิมพ์ 2\n'
                  'ต้องการตรวจสอบยอดทั้งหมดพิมพ์ 3\n'
                  'หากต้องการกลับไปยังหน้าเดิมก่อนหน้าพิมพ์ 4')
            choose2 = int(input(':'))
            if choose2 == 1:
                print('พิมพ์วันที่ที่ท่านต้องการตรวจสอบยอด \n'
                      'รูปแบบดังนี้ ตัวอย่าง 25/3/2022')
                dayInput = input(':')
                self.show_file_month_day(dayInput, file_name)
                self.plotDay(dayInput, file_name)
            elif choose2 == 2:
                print('พิมพ์เดือนที่ท่านต้องการตรวจสอบยอด \n'
                      'รูปแบบดังนี้ ตัวอย่าง 3/2022 คือ เดือน 3 ปี ค.ศ.2022')
                monthInput = input(':')
                self.show_file_month_day(monthInput, file_name)
                self.plotMonth(monthInput, file_name)
            elif choose2 == 3:
                self.showAll(file_name)
            elif choose2 == 4:
                pass
            else:
                print('สิ่งที่ผู้ใช้ป้อนไม่อยู่ในระบบ!!! กรุณาป้อนข้อมูลตามที่กำหนด\n')
        else:
            pass

    # ฟังก์ชั่นย่อย
    def show_file_month_day(self, day_month, file_name):
        try:
            df = pd.read_csv(file_name)
            try:
                day_month = self.date_create(day_month)
            except:
                day_month = "1/"+day_month
                day_create = self.date_create(day_month)
                day_month = str(day_create)[-2]
            self.showTotal(df)
            df = df.drop(columns='Money')
            final_df = df.loc[df['Date'].str.contains(str(day_month), na=False)]
            print(tabulate.tabulate(final_df, headers='keys', showindex=False), "\n")
        except:
            print("ไม่สามารถอ่านไฟล์ได้ อาจเป็นไฟล์ที่ไม่มีข้อมูลหรือข้อมูลเสียหาย\n")

    def showAll(self, file_name):
        try:
            df = pd.read_csv(file_name)
            self.showTotal(df)
            df = df.drop(columns='Money')
            print(tabulate.tabulate(df, headers='keys', showindex=False), "\n")
        except:
            print("ไม่สามารถอ่านไฟล์ได้ อาจเป็นไฟล์ที่ไม่มีข้อมูลหรือข้อมูลเสียหาย\n")

    def incomeOutcome(self, Date, Money, Description, Filename):

        df = pd.read_csv(Filename)
        col = ['No.', 'Date', 'Description', 'Income', 'Expense', 'Total', 'Money']
        if Money > 0:
            Income = Money
            Expense = ' '
        elif Money < 0:
            Income = ' '
            Expense = Money * (-1)
        Total = 0

        newData = np.array([(len(df) + 1, Date, Description, Income, Expense, Total, Money)])
        newDF = pd.DataFrame(data=newData, columns=col)
        df = pd.concat([df, newDF])
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values(by='Date')

        df['No.'] = np.arange(1, len(df) + 1)

        showDF = newDF.drop(columns=["Total", "Money"])
        print(showDF)
        print("\nผู้ใช้แน่ใจหรือไม่ที่จะบันทึกรายการนี้? พิมพ์ Y หากแน่ใจ")
        make_sure = input(":")
        if make_sure.upper() == 'Y':
            df.to_csv(Filename, index=False)
        else:
            pass

    def showTotal(self, data):
        Total = 0
        for i in range(len(data)):
            Total = Total + data.iloc[i, -1]
            data.iloc[i, -2] = Total

    def checkFolder(self):
        try:
            if not os.path.exists('D:\AccountFile'):
                print("ทางโปรแกรมพบว่าท่านไม่มีไฟล์ที่ใช้จัดเก็บข้อมูลสำหรับโปรแกรม\n"
                      "จึงขออนุญาติสร้างโฟลเดอร์เก็บข้อมูล\n"
                      "ท่านต้องการสร้างโฟล์เดอร์ไว้ที่ไดรฟ์ไหนระหว่าง C หรือ D")
                drive_name = input(":")
                os.makedirs(drive_name.upper()+':\AccountFile')
        except OSError:
            pass

    def writeFile(self):
        name = input('พิมพ์ชื่อไฟล์ที่ต้องการจะตั้ง :')
        file_name = 'D:\AccountFile/' + name + '.csv'
        col = ['No.', 'Date', 'Description', 'Income', 'Expense', 'Total']
        f = open(file_name, 'w')
        writer = csv.writer(f)
        writer.writerow(col)
        return file_name

    def selectingFile(self):
        print("รายชื่อไฟล์ที่มีอยู่:")
        for i in os.listdir(r'D:\AccountFile'):
            print(i[:-4])
        print('\nพิมพ์ชื่อไฟล์ที่ต้องการจะใช้')
        name = input(':')
        fname = name + '.csv'
        if fname in os.listdir(r'D:\AccountFile'):
            file_name = 'D:\AccountFile/' + name + '.csv'
        else:
            print("ไม่มีไฟล์ที่ท่านระบุอยู่ในระบบ กรุณาสร้างไฟล์เพื่อบันทึก")
        return file_name

    def plotDay(self, day, file_name):
        df = pd.read_csv(file_name)
        day = str(self.date_create(day))
        df = df.loc[df['Date'].str.contains(day, na=False)]
        self.showTotal(df)
        no = []
        total = []
        for i in range(len(df)):
            newdf = df.loc[df['Date'].str.contains(day, na=False)]
            no.append(i + 1)
            total.append(list(newdf['Total'])[i])

        fig = plt.figure(figsize=(15, 5))
        ax = fig.add_subplot(111)
        ax.plot(no, total, marker='*')
        plt.xticks(no)
        plt.title("Total money of the account in the date " + str(day))
        plt.xlabel("Terms of receipt of income - expense (Time)")
        plt.ylabel("Amount (Baht)")
        plt.show()

    def plotMonth(self, month, file_name):
        month_date_list = self.date_list(month)
        df = pd.read_csv(file_name)

        day = np.arange(1, len(month_date_list) + 1)
        total = []
        plot_total = []
        self.showTotal(df)
        for i in range(len(day)):
            newdf = df.loc[df['Date'].str.contains(month_date_list[i], na=False)]
            total.append(newdf['Total'].sum())
        for i in range(len(total)):
            try:
                plot_total.append(total[i] + plot_total[i - 1])
            except:
                plot_total.append(total[i] + 0)

        fig = plt.figure(figsize=(15, 5))
        ax = fig.add_subplot(111)
        ax.plot(day, plot_total, marker='*')
        plt.ylim(min(total), max(total) * 3 / 2)
        plt.xlim(1, 31)
        plt.title("Total money of the account in the month " + str(month))
        plt.xlabel("Date of receipt of income - expense (Date)")
        plt.ylabel("Amount (Baht)")
        plt.show()

    def strat_menu(self):
        print('    โปรแกรมบันทึกรายรับรายจ่าย\n'
              '\n'
              '          จัดทำโดย               \n'
              'นายธณรัฐ เพียรชัยภูมิ 643040011-1\n'
              'นายพีระณัฐ ศรีสรรพ์ 643040249-8\n'
              'นางสาวภูริชญดา สนิทชน 643040251-1\n')

        try:
            input("กดที่ปุ่ม <Enter> เพื่อไปใช้งานโปรแกรม")
        except SyntaxError:
            pass

    def date_create(self, day_input):
        day_list = day_input.split("/")
        date = dt.date(int(day_list[2]), int(day_list[1]), int(day_list[0]))
        return date

    def date_list(self, month_input):
        date_list = []
        month_list = month_input.split("/")
        for i in range(31):
            try:
                date = dt.date(int(month_list[1]), int(month_list[0]), i + 1)
                date_list.append(str(date))
            except:
                pass
        return date_list

    # ฟังก์ชั่นการทำงานของโปรแกรม
    def __init__(self):
        self.strat_menu()
        self.checkFolder()
        while True:
            print("ผู้ใช้ต้องการดำเนินการกับไฟล์ที่มีหรือต้องการสร้างไฟล์ใหม่?\n"
                  "ต้องการดำเนินการกับไฟล์ที่มีอยู่พิมพ์ 1\n"
                  "ต้องการสร้างไฟล์ใหม่ในการบันทึกพิมพ์ 2\n"
                  "ปิดการทำงานของโปรแกรมพิมพ์ 3")

            try:
                file_select = int(input(':'))
                if file_select == 1:
                    file_name = self.selectingFile()
                elif file_select == 2:
                    file_name = self.writeFile()
                elif file_select == 3:
                    break
                else:
                    print('สิ่งที่ผู้ใช้ป้อนไม่อยู่ในระบบ!!! กรุณาป้อนข้อมูลตามที่กำหนด\n')

                while True:

                    print('พิมพ์ 1 เพื่อบันทึกรายรับ รายจ่าย\n'
                          'พิมพ์ 2 เพื่อเรีกดูบัญชี\n'
                          'พิมพ์ 3 เพื่อกลับไปยังหน้าจัดการไฟล์\n'
                          'หมายเหตุ: หากมีการกรอกข้อมูลผิดพลาด โปรแกรมจะกลับมายังหน้าต่างนี้ทันที\n')
                    Finput = input(':')

                    try:
                        if int(Finput) == 3:
                            break
                        elif int(Finput) in [1, 2]:
                            self.choice(int(Finput), file_name)
                        else:
                            print('สิ่งที่ผู้ใช้ป้อนไม่อยู่ในระบบ!!! กรุณาป้อนข้อมูลตามที่กำหนด\n')
                    except:
                        print('สิ่งที่ผู้ใช้ป้อนไม่อยู่ในระบบ!!! กรุณาป้อนข้อมูลตามที่กำหนด\n')
            except:
                print('สิ่งที่ผู้ใช้ป้อนไม่อยู่ในระบบ!!! กรุณาป้อนข้อมูลตามที่กำหนด\n')

openAccount()
