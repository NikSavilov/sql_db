import sys, math, mysql.connector

cnx = mysql.connector.connect(user='root', password='root',
                              host='localhost',
                              database='shop')
cursor = cnx.cursor()
cursor.execute("SELECT id, model, screen_size from phones")
phones = cursor.fetchall()
print('ID', '\t' ,'Model')
for i in range(len(phones)):
    print(phones[i][0], '\t', phones[i][1])
phone_id = 0;
try:
    while (phone_id != -1):
        # Выбираем модель для подбора чехла.
        print("Enter phone's id:"),
        phone_id = input()
        if int(phone_id) in range(len(phones)):
            cur_size = phones[int(phone_id)-1][2]
            print("Size: ", cur_size)
            cursor.execute("SELECT model, price FROM cases WHERE ((low_size <="+str(cur_size)+") AND (high_size>="+str(cur_size)+")) ORDER BY price")
            cases = cursor.fetchall()
            print("Suitable model(s):")
            for i in range(len(cases)):
                print(cases[i][0],"  -  ",cases[i][1],"p.")
        else:
            print("Choose existing model")
except BaseException:
    print("Error")

cursor.execute("select tmp.MODELS, tmp.Lcase from (select phones.model AS MODELS, cases.low_size AS Lcase from phones left join cases on ((phones.screen_size >= cases.low_size) and (phones.screen_size<=cases.high_size)) group by phones.model) AS tmp where tmp.Lcase is null")
no_cases = cursor.fetchall()
print("Devices with no suitable cases: ")
for i in range(len(no_cases)):
    print(no_cases[i][0])
cnx.close()
