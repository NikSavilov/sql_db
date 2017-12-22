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
			print('{0}\t{1:40} {2}'.format(phones[i][0], phones[i][1], phones[i][2]))
		phone_id = 0
		try:
			# Выбираем модель для подбора чехла.
			print("Enter phone's id:", end=" ")
			phone_id = int(input()) - 1
			print("\n")
			if phone_id in range(len(phones)):
				cur_size = phones[phone_id][2]
				print("Size: ", cur_size)
				cursor.execute("SELECT model, price FROM cases WHERE ((low_size <="+str(cur_size)+") AND (high_size>="+str(cur_size)+")) ORDER BY price")
				cases = cursor.fetchall()
				print("Suitable model(s):\n")
				for i in range(len(cases)):
					print(cases[i][0],"  -  ",cases[i][1],"p.")
				print("\n")
			else:
				print("Choose existing model\n")
		except BaseException:
			print("Error")
	if int(request) == 2:
		cursor.execute("select tmp.MODELS from (select phones.model AS MODELS, cases.low_size AS Lcase from phones left join cases on ((phones.screen_size >= cases.low_size) and (phones.screen_size<=cases.high_size)) group by phones.model) AS tmp where tmp.Lcase is null")
		no_cases = cursor.fetchall()
		print("Devices with no suitable cases: ")
		for i in range(len(no_cases)):
			print(no_cases[i][0])
		if len(no_cases) != 0:
			print("Potential contributors are:")
			cursor.execute("SELECT * FROM (SELECT nam, DATE_ADD(contributers.last_delievery, INTERVAL contributers.deliev_freq DAY) as C_DATE, phone FROM contributers order by C_DATE) AS tmp WHERE C_DATE > CURDATE() limit 3")
			potential_contributors = cursor.fetchall()
			print("\nContributor\t\tDate\t\tPhone")
			for i in range(len(potential_contributors)):
				print('{0:20} {1:18} {2}'.format(potential_contributors[i][0], str(potential_contributors[i][1]), potential_contributors[i][2]))

cnx.close()
a = input()