import pandas as pd
import tabulate
import numpy as np

# ฟังก์ชั่นหลัก
def Choice(choose):
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
        IncomeOutcome(day, money, description)
    elif choose == 2 :
        print('ต้องการตรวจสอบยอดเป็นรายวันพิมพ์ 1\n'
              'ต้องการตรวจสอบยอดเป็นรายเดือนพิมพ์ 2\n'
              'ต้องการตรวจสอบยอดเป็นทั้งหมดพิมพ์ 3')
        choose2 =int(input(':'))
        if choose2 == 1:
            print('พิมพ์วันที่ที่ท่านต้องการตรวจสอบยอด \n'
                  'รูปแบบดังนี้ ตัวอย่าง 2565/3/25')
            dayInput = input(':')
            showAccountDay(dayInput)
        elif choose2 == 2:
            print('พิมพ์เดือนที่ท่านต้องการตรวจสอบยอด \n'
                  'รูปแบบดังนี้ ตัวอย่าง 2565/3 คือ เดือน 3 ปี 2565')
            monthInput = input(':')
            showAccountMonth(monthInput)
        elif choose2 == 3:
            showAll()
        else:
            print('สิ่งที่ผู้ใช้ป้อนไม่อยู่ในระบบ!!! กรุณาป้อนข้อมูลตามที่กำหนด\n')
    else:
        print('ERROR')

# ฟังก์ชั่นย่อย
def IncomeOutcome(Day, Money,Description ):
    df = pd.read_csv('D:\AccountFile/Accounted.csv')


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

    df.to_csv('D:\AccountFile/Accounted.csv', index=False)

def showAccountDay(day):
    df = pd.read_csv('D:\AccountFile/Accounted.csv')
    Daydf = df.loc[df['Day'] == day]
    print(tabulate.tabulate(Daydf, headers='keys', showindex=False))


def showAccountMonth(month):
    df = pd.read_csv('D:\AccountFile/Accounted.csv')
    Monthdf = df.loc[df['Day'].str.contains(month, na=False)]
    print(tabulate.tabulate(Monthdf, headers='keys', showindex=False))

def showAll():
    df = pd.read_csv('D:\AccountFile/Accounted.csv')
    print(tabulate.tabulate(df, headers='keys', showindex=False))



while True :
    print('พิมพ์ 1 เพื่อบันทึกรายรับ รายจ่าย\n'
          'พิมพ์ 2 เพื่อเรีกดูบัญชี\n'
          'พิมพ์ 3 เพื่อปิดการทำงาน')
    Finput = input(':')

    try:
        if int(Finput) == 3:
            break
        elif int(Finput) in [1, 2]:
            Choice(int(Finput))
        else:
            print('สิ่งที่ผู้ใช้ป้อนไม่อยู่ในระบบ!!! กรุณาป้อนข้อมูลตามที่กำหนด\n')
    except:
        print('สิ่งที่ผู้ใช้ป้อนไม่อยู่ในระบบ!!! กรุณาป้อนข้อมูลตามที่กำหนด\n')
