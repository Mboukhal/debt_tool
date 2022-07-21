#!/usr/bin/env python3

"""

	Programe for debt saving 1.0

"""

import os
import time
import pandas as pd

csv_file = os.path.join(os.getcwd(), 'src/debt.csv')
log_file = os.path.join(os.getcwd(), 'src/debt.log')

print (log_file)
def pause(msg):
	if os.name == 'posix': # if mac os
		os.system(f"/bin/bash -c 'read -s -n 1 -p \"{msg}\"'")
	elif os.name == 'nt': # if windows
		os.system(f"echo \"{msg}\" ;pause")

def log_file_add(msg_log):
	msg_log = msg_log + ": " + time.strftime("%d-%m-%Y %H:%M:%S") + '\n'
	with open(log_file, 'a') as f:
		f.write(msg_log)
	# print (msg_log)

def print_list():
	if os.path.exists(csv_file):
		df = pd.read_csv(csv_file)
		print(df.tail(5))
		print('\n')
		return
	print ("Welcome to debt saver.\n")
	
def add_to_csv():
	print_list()
	new_row = { 'Name':[], 'Debt':[], 'Date':[] }
	print('Enter [C] for cancel\n\n')
	new_row['Name'] = [str((input('Enter Name:\n\t>> ')))]
	if len(new_row['Name'][0]) == 1 and new_row['Name'][0][0] == 'C':
		return
	new_row['Debt'][0] = 0
	while int(new_row['Debt'][0]) or float(new_row['Debt'][0]):
		new_row['Debt'] = [(input('Enter debt:\n\t>> '))]
	if (not (new_row['Debt'][0].isnumeric())) and new_row['Debt'][0][0] == 'C':
		return
	new_row['Debt'][0] = str(new_row['Debt'][0]) + '$'
	date_c = time.strftime("%d-%m-%Y %H:%M")
	new_row['Date'] = [(input(f'Enter date default date [{date_c}]:\n\t>> ') or date_c)]
	if len(new_row['Date'][0]) == 1 and new_row['Date'][0][0] == 'C':
		return
	log_file_add(f"Debt added: [{new_row['Name'][0]}] [{new_row['Debt'][0]}] [{new_row['Date'][0]}] ")
	new_df = pd.DataFrame(new_row)
	print (new_row)
	if os.path.exists(csv_file):
		df = pd.read_csv(csv_file)
		df = df.append(new_df, ignore_index=True)
		df.to_csv(csv_file, index=False)
		return
	new_df.to_csv(csv_file, index=False)
	
def print_list_all():
	if os.path.exists(csv_file):
		df = pd.read_csv(csv_file)
		print(df)
		print('\n')
		log_file_add("List viewed")
		pause('Press any key to continue...\n')
		return
	print ("No file named \{debt.csv\}")

def delet_all():
	if os.path.exists(csv_file):
		print_list()
		confirm = str(input('Are you sure you want to delet all [ yes / no ]: ' or 'no'))
		if confirm == 'yes':
			confirm = str(input('last stape delet all [ yes / no ]: ' or 'no'))
			if confirm == 'yes':
				os.remove(csv_file)
				pause('All data deleted.\n')
	pause('No data to delete!\n')
	
def delet_from_csv():
	if os.path.exists(csv_file):
		df = pd.read_csv(csv_file)
		print(df)
		print('\n')
		choise = [int(input('Enter id to remove:\n\t>> '))]
		s = df.loc[choise[0]]
		try:
			df.drop(index=choise, axis=0, inplace=True)
		except Exception:
			os.system('clear')
			print(f"Error {choise} not in list!")
			pause()
			return
		print(s)
		pause('\ndeleted.')
		df.to_csv(csv_file, index=False)
		return
	print ("No data to delete!")

def main():
	cmd = ''
	log_file_add("Debt opened")
	while cmd != 'q':
		os.system('clear')
		print_list()
		print("\t1. Add debt.")
		print("\t2. List debt.")
		print("\t3. Delet debt.")
		print("\t4. delete All.")
		print("\nPress Enter to quit.")
		print()
		cmd = input('>> ')
		os.system('clear')
		if cmd == '1':
			add_to_csv()
		if cmd == '2':
			print_list_all()
		if cmd == '3':
			delet_from_csv()
		if cmd == '4':
			delet_all()
		if cmd == '':
			print("\n")
			cmd = input('Enter [y] to conferme quit: ' or n)
			if cmd == 'y':
				log_file_add("Debt closed")
				exit(0)

if __name__ == '__main__':
	main()