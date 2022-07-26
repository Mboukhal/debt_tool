#!/usr/bin/env python3

"""

	Programe for debt saving 1.0

"""

from os import path, mkdir, remove, rmdir
from sys import argv
from time import strftime
from pandas import read_csv, DataFrame
from utils import *

main_dir = path.abspath(path.dirname(argv[0]))
src_dir = path.join(main_dir, 'src')
csv_file = path.join(src_dir, 'debt.csv')
log_file = path.join(src_dir, 'debt.log')

if not path.exists(src_dir):
	mkdir(src_dir, 0o777)

def log_file_add(msg_log):
	msg_log = msg_log + ": " + strftime("%d-%m-%Y %H:%M:%S") + '\n'
	with open(log_file, 'a') as f:
		f.write(msg_log)
	# print (msg_log)

def print_list():
	if path.exists(csv_file):
		df = read_csv(csv_file)
		print(df.tail(5))
		print('\n')
		return
	print ("Welcome to debt saver v0.1\n")
	
def add_to_csv():
	print_list()
	# list of culmns
	new_row = { 'Name':[], 'Debt':[], 'Date':[], 'Phone':[] }
	print('Enter [C] for cancel\n\n')
	
	new_row['Name'] = [(input('Enter Name:\n\t>> '))]
	if len(new_row['Name'][0]) == 1 and new_row['Name'][0][0] == 'C':
		return
	x = 1
	while x:
		new_row['Debt'] = [(input('Enter debt:\n\t>> '))]
		if len(new_row['Debt'][0]) == 1 and new_row['Debt'][0][0] == 'C':
			return
		try:
			new_row['Debt'][0] = float(new_row['Debt'][0])
		except ValueError:
			print ('`', new_row['Debt'][0], '` not expected expresion!')
		else:
			x = 0
	
	new_row['Debt'][0] = "${:,.2f}".format(float(new_row['Debt'][0])) 
	date_c = strftime("%d-%m-%Y %H:%M")
	new_row['Date'] = [(input(f'Enter date default date [{date_c}]:\n\t>> ') or date_c)]
	if len(new_row['Date'][0]) == 1 and new_row['Date'][0][0] == 'C':
		return
	
	new_row['Phone'] = [(input(f'Enter phone number:\n\t>> ') or 'Non')]
	if len(new_row['Phone'][0]) == 1 and new_row['Phone'][0][0] == 'C':
		return
	log_file_add(f"Debt added: [{new_row['Name'][0]}] [{new_row['Debt'][0]}] [{new_row['Date'][0]}] [{new_row['Phone'][0]}] ")
	new_df = DataFrame(new_row)
	if not path.exists(src_dir):
		mkdir(src_dir, 0o777)
	if path.exists(csv_file):
		df = read_csv(csv_file)
		df = df.append(new_df, ignore_index=True)
		df.to_csv(csv_file, index=False)
		return
	new_df.to_csv(csv_file, index=False)
	
def print_list_all():
	log_file_add("List viewed")
	if path.exists(csv_file):
		df = read_csv(csv_file)
		print(df.sort_values(by=['Name']))
		print('\n')
		debt_list = df['Debt'].tolist()
		total = 0
		for sum_list in debt_list:
			total = total + float(sum_list[1:].replace(',', ''))
		print('\n')
		print('\t\tTotal of debts:\t${:,.2f}'.format(total))
		print()
		pause('Press any key to return...')
		return
	print ("No file named \{debt.csv\}")

def delet_all():
	if path.exists(csv_file):
		print_list()
		confirm = str(input('Are you sure you want to delet all [ y/n ]: ' or ''))
		if confirm == 'y':
			csv = str(input(f'Press [y] to remove {csv_file}:\n\t>> ' or ''))
			if csv == 'y':
				remove(csv_file)
			log = str(input(f'Press [y] to remove {log_file}:\n\t>> ' or ''))
			if log == 'y':
				remove(log_file)
			if log == 'y' and csv == 'y':
				rmdir(src_dir)
				pause('All data deleted.\n')
			return
	pause('Deleting canceled!\n')
	
def delet_from_csv():
	if path.exists(csv_file):
		df = read_csv(csv_file)
		print(df)
		print('\n')
		choise = [int(input('Enter id to remove or enter to cancel:\n\t>> '))]
		if choise == '':
			return
		s = df.loc[choise[0]]
		try:
			df.drop(index=choise, axis=0, inplace=True)
		except Exception:
			clear_console()
			print(f"Error {choise} not in list!")
			pause()
			return
		print(s)
		x = input('Press enter to confirm or [c] to cancel:\n' or 'y')
		if x == 'y':
			df.to_csv(csv_file, index=False)
			pause('data deleted.\n')
			return
	print ("No data to delete!")

def main():
	cmd = ''
	log_file_add("Debt opened")
	while cmd != 'q':
		clear_console()
		print_list()
		print("\t1. Add debt.")
		print("\t2. List debt.")
		print("\t3. Delet debt.")
		print("\t4. delete All.")
		print("\t5. open source folder.")
		print("\tq. quit.")
		print()
		cmd = input('>> ')
		if len(cmd) > 1:
			cmd = cmd[0]
		clear_console()
		if cmd == '1':
			add_to_csv()
		if cmd == '2':
			print_list_all()
		if cmd == '3':
			delet_from_csv()
		if cmd == '4':
			delet_all()
		if cmd == '5':
			open_src(src_dir)
			log_file_add("Source folder opened")
		if cmd == 'q':
			log_file_add("Debt closed")
			exit(0)

if __name__ == '__main__':
	main()