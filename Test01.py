import csv
import pandas as pd
import tabulate
import numpy as np
import os

def checkFolder():
    try:
        if not os.path.exists('D:\AccountFile'):
            os.makedirs('D:\AccountFile')
    except OSError:
        pass

def WriteFile():
    name = input('พิมพ์ชื่อไฟล์ที่ต้องการจะตั้ง')
    file_name = 'D:\AccountFile/' + name + '.csv'

    col = ['No.', 'Day', 'Description', 'Income', 'Expense', 'Total']
    f = open(file_name, 'w')

    writer = csv.writer(f)

    writer.writerow(col)

    return file_name


def selectingFile():
    print("รายชื่อไฟล์ที่มีอยู่:")
    for i in os.listdir(r'D:\AccountFile'):
        print(i[:-4])
    print('\nพิมพ์ชื่อไฟล์ที่ต้องการจะใช้')
    name = input(':')
    fname = name + '.csv'
    if fname in os.listdir(r'D:\AccountFile'):
        file_name = 'D:\AccountFile/' + name + '.csv'
    else:
        pass
    return file_name



# ฟังก์ชั่นหลัก
def Choice(choose, Filename):
    if choose == 1 :
        print('พิมพ์วันที่และจำนวนเงินที่ต้องการ\n'
              'โดยพิมพ์รูปแบบนี้ ตัวอย่าง\n'
              'วันที่: 2565/3/25 คือ วันที่ 25 เดือน 3 ปี 2565\n'
              'เงิน: +200 คือรายรับ 200\n'
              '    -300 คือรายจ่าย 300\n'
              'หากจะยกเลิกให้พิมพ์ pass ในช่อง วันที่ต้องการบันทึก')
        day = input('วันที่ต้องการบันทึก :')
        money = int(input('จำนวนเงิน :'))
        description = input('รายละเอียด :')
        IncomeOutcome(day, money, description, Filename)
    elif choose == 2 :
        print('ต้องการตรวจสอบยอดเป็นรายวันพิมพ์ 1\n'
              'ต้องการตรวจสอบยอดเป็นรายเดือนพิมพ์ 2\n'
              'ต้องการตรวจสอบยอดทั้งหมดพิมพ์ 3\n'
              'หากต้องการกลับไปยังหน้าเดิมก่อนหน้าพิมพ์ 4')
        choose2 =int(input(':'))
        if choose2 == 1:
            print('พิมพ์วันที่ที่ท่านต้องการตรวจสอบยอด \n'
                  'รูปแบบดังนี้ ตัวอย่าง 2565/3/25')
            dayInput = input(':')
            showAccountDay(dayInput, Filename)
        elif choose2 == 2:
            print('พิมพ์เดือนที่ท่านต้องการตรวจสอบยอด \n'
                  'รูปแบบดังนี้ ตัวอย่าง 2565/3 คือ เดือน 3 ปี 2565')
            monthInput = input(':')
            showAccountMonth(monthInput, Filename)
        elif choose2 == 3:
            showAll(Filename)
        elif choose2 == 4:
            pass
        else:
            print('สิ่งที่ผู้ใช้ป้อนไม่อยู่ในระบบ!!! กรุณาป้อนข้อมูลตามที่กำหนด\n')
    else:
        print('ERROR')

# ฟังก์ชั่นย่อย
def IncomeOutcome(Day, Money, Description, Filename):

    df = pd.read_csv(Filename)
    col = ['No.', 'Day', 'Description', 'Income', 'Expense', 'Total']
    if Money > 0 :
        Income = Money
        Expense = ' '
    elif Money < 0 :
        Income = ' '
        Expense = Money*(-1)
    if len(df) == 0:
        Total = 0
    elif len(df) != 0:
        Total = df['Total'][len(df)-1]


    Total = Total + Money

    newData = np.array([(len(df)+1, Day, Description, Income, Expense, Total)])
    newDF = pd.DataFrame(data=newData, columns=col)
    df = pd.concat([df, newDF])
    df = df.sort_values(['Day'])
    df['No.'] = np.arange(1, len(df)+1)

    df.to_csv(Filename, index=False)

def showAccountDay(day, Filename):
    df = pd.read_csv(Filename)
    Daydf = df.loc[df['Day'] == day]
    print(tabulate.tabulate(Daydf, headers='keys', showindex=False),"\n")


def showAccountMonth(month, Filename):
    df = pd.read_csv(Filename)
    Monthdf = df.loc[df['Day'].str.contains(month, na=False)]
    print(tabulate.tabulate(Monthdf, headers='keys', showindex=False),"\n")

def showAll(Filename):
    df = pd.read_csv(Filename)
    print(tabulate.tabulate(df, headers='keys', showindex=False),"\n")

#ฟังก์ชั่นการทำงานของโปรแกรม
def main():
    checkFolder()
    while True:
        print("ผู้ใช้ต้องการดำเนินการกับไฟล์ที่มีหรือต้องการสร้างไฟล์ใหม่\n"
              "ต้องการดำเนินการกับไฟล์ที่มีอยู่พิมพ์ 1\n"
              "ต้องการสร้างไฟล์ใหม่ในการบันทึกพิมพ์ 2\n"
              "ปิดการทำงานของโปรแกรมพิมพ์ 3")

        try:
            file_select = int(input(':'))
            if file_select == 1:
                file_name = selectingFile()
            elif file_select == 2:
                file_name = WriteFile()
            elif file_select == 3:
                break
            else:
                print('สิ่งที่ผู้ใช้ป้อนไม่อยู่ในระบบ!!! กรุณาป้อนข้อมูลตามที่กำหนด\n')

            while True:

                print('พิมพ์ 1 เพื่อบันทึกรายรับ รายจ่าย\n'
            'พิมพ์ 2 เพื่อเรีกดูบัญชี\n'
            'พิมพ์ 3 เพื่อกลับไปยังหน้าจัดการไฟล์\n'
              'หมายเหตุ: หากมีการกรอกข้อมูลผิดพลาด โปรแกรมจะกลับมายังหน้าต่างนี้ทันที')
                Finput = input(':')

                try:
                    if int(Finput) == 3:
                        break
                    elif int(Finput) in [1, 2]:
                        Choice(int(Finput), file_name)
                    else:
                        print('สิ่งที่ผู้ใช้ป้อนไม่อยู่ในระบบ!!! กรุณาป้อนข้อมูลตามที่กำหนด\n')
                except:
                    print('สิ่งที่ผู้ใช้ป้อนไม่อยู่ในระบบ!!! กรุณาป้อนข้อมูลตามที่กำหนด\n')
        except:
            print('สิ่งที่ผู้ใช้ป้อนไม่อยู่ในระบบ!!! กรุณาป้อนข้อมูลตามที่กำหนด\n')
main()