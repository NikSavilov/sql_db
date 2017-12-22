import sys, math, mysql.connector

cnx = mysql.connector.connect(user='dl.hosting.492', password='YxnIccn8hbDM',
							  host='194.67.223.165',
							  database='dl_hosting_492_shop')
request = 1
print("Choose action:")
print("1) Suggest case.\n2) Show phones with no cases.\n")
while (request != 0):
	request = input()
	cursor = cnx.cursor()
	if int(request) == 1:
		cursor.execute("SELECT id, model, screen_size from phones")
		phones = cursor.fetchall()
		print('ID', '\t', 'Model')
		for i in range(len(phones)):
			print(phones[i][0], '\t', phones[i][1])
		phone_id = 0
		try:
			# Выбираем модель для подбора чехла.
			print("Enter phone's id:"),
			phone_id = input()
			if int(phone_id) in range(len(phones)):
				cur_size = phones[int(phone_id)][2]
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
	if int(request) == 2:
		cursor.execute("select tmp.MODELS, tmp.Lcase from (select phones.model AS MODELS, cases.low_size AS Lcase from phones left join cases on ((phones.screen_size >= cases.low_size) and (phones.screen_size<=cases.high_size)) group by phones.model) AS tmp where tmp.Lcase is null")
		no_cases = cursor.fetchall()
		print("Devices with no suitable cases: ")
		for i in range(len(no_cases)):
			print(no_cases[i][0])
		if len(no_cases) != 0:
			print("Potential contributors are:")
			cursor.execute("SELECT * FROM (SELECT nam, DATE_ADD(contributers.last_delievery, INTERVAL contributers.deliev_freq DAY) as C_DATE, phone FROM contributers order by C_DATE) AS tmp WHERE C_DATE > CURDATE() limit 3")
			potential_contributors = cursor.fetchall()
			for i in range(len(potential_contributors)):
				print(potential_contributors[i][0], potential_contributors[i][1])

cnx.close()
a = input()