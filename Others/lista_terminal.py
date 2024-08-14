#!/usr/bin python3

import argparse
import sys
from tabulate import tabulate as tab
import datetime

name_file = 'names.txt'

def arguments():
	# Processa os argumentos de linha de comando e retorna um dicionário com os valores.
	informations = {'name':'', 'telephone': 0, 'show': 0, 'remove': '','obs': '', 'sobs': ''}
	description = argparse.ArgumentParser(description='Cadastro de contatos. Para cadastrar é necessario nome/apelido e o numero de telefone com DDD e digito 9.')
	description.add_argument('-n','--name', type=str, default='&', help='Informe o nome.')
	description.add_argument('-t','--telephone', type=int, default=0, help='Informe o telefone com o DDD e o digito 9.\nEx.: 61912345678')
	description.add_argument('-s','--show', type=int, default=0, help='Mostra os contatos salvos, apenas coloque 1.\nEx.: -s=1')
	description.add_argument('-rm','--remove', type=str, default='', help='Apaga um contato pelo nome, confira na agenda o nome. Letras maiusculas e minusculas importam.')
	description.add_argument('-so','--sobs', type=str, default='', help='Mostra uma observação de um contato, como: mãe, pai, pizzaria, quadra 22, etc.')
	description.add_argument('-o','--obs', type=str, default='', help='Adiciona uma observação de um contato, como: mãe, pai, pizzaria, quadra 22, etc.')
	informations['name'], informations['telephone']= str(description.parse_args().name).title(), str(description.parse_args().telephone)
	informations['show'], informations['remove']= description.parse_args().show, str(description.parse_args().remove).title()
	informations['obs'], informations['sobs'] = (description.parse_args().obs).title(), (description.parse_args().sobs).title()
	return informations


def open_files():
	try:
		with open(name_file, "r") as arq:
			contact = arq.readlines()
			if contact[0] == '':
				pass
			return contact
	except IndexError as e:
		print('Lista de contatos Vazia.')
		return sys.exit()
	except FileNotFoundError:
		print("Arquivo não encontrado. Vamos criá-lo...")
		file()
		return []
	except IOError as e:
		print(f"Erro ao abrir o arquivo: {e}")
		return sys.exit()


def file():
	# Cria o arquivo caso não exista.
	try:
		with open(name_file, 'w') as arq:
			arq.write('')
	except Exception as e:
		print(f"Erro ao criar o arquivo, O erro encontrado foi: {e}")


def phone_number_validation(data):
	# Verifica a autenticidade do número, com base no DDD e codigo 9, tendo os 11 digitos totais.
	ddds = {
    'Distrito Federal': ['61'],
    'Goiás': ['62', '64'],
    'Mato Grosso': ['65', '66'],
    'Mato Grosso do Sul': ['67'],
    'Alagoas': ['82'],
    'Bahia': ['71', '73', '74', '75', '77'],
    'Ceará': ['85', '88'],
    'Maranhão': ['98', '99'],
    'Paraíba': ['83'],
    'Pernambuco': ['81', '87'],
    'Piauí': ['86', '89'],
    'Rio Grande do Norte': ['84'],
    'Sergipe': ['79'],
    'Acre': ['68'],
    'Amapá': ['96'],
    'Amazonas': ['92', '97'],
    'Pará': ['91', '93', '94'],
    'Rondônia': ['69'],
    'Roraima': ['95'],
    'Tocantins': ['63'],
    'Espírito Santo': ['27', '28'],
    'Minas Gerais': ['31', '32', '33', '34', '35', '37', '38'],
    'Rio de Janeiro': ['21', '22', '24'],
    'São Paulo': ['11', '12', '13', '14', '15', '16', '17', '18', '19'],
    'Paraná': ['41', '42', '43', '44', '45', '46'],
    'Rio Grande do Sul': ['51', '53', '54', '55'],
    'Santa Catarina': ['47', '48', '49']}
	for key, values in ddds.items():
		if data[:2] in values:
			conf = [1,f'{key}']
			break
		else:
			conf = [0]
	if data[2] == '9' and len(data) == 11 and conf[0] == 1:
		return conf
	else:
		print('\nVerifique se inseriu todos os 11 digitos, incluindo DDD e o digito 9.\nPara mais informações utilize o --help ou -h')
		conf = [0]
		return conf


def write_file(data='', validation=True):
	# Inseri no arquivo os novos dados, e reescreve os dados dependendo de alguma chamada de fnção, caso necessario.
	try:
		values = day_hour()
		with open(name_file, 'a') as arq:
			if validation:
				arq.writelines(f'{data[0]};{data[1]};{data[2]}\n')
				print(f'\nContato {data[0]} cadastrado com o número {data[1]}.\nData: {values[0]} Hora: {values[1]}')
				return [data[0], data[1], values[0], values[1]]
			else:
				arq.writelines(f'{contact[0]};{contact[1]};{contact[2]};{contact[3]}\n' for contact in data)
				print(f'\nAlteração no banco de dados concluida.\nData: {values[0]} Hora: {values[1]}')
				return [values[0], values[1]]
	except Exception as e:
		print(f"Erro no arquivo. Erro encontrado foi: {e}")


def formattation_file():
	# Faz a busca e tras os dados do arquivo, organizando e processando os dados, colocando numa lista ordenada.
	inf = []
	arquivo = open_files()
	for contact in arquivo:
		contact = contact.replace("\n", "").split(";")
		if len(contact) == 3:
			contact.append('')
		inf.append(contact)
	organize_inf = sorted(inf)
	return organize_inf


def formattation_contacts(data=''):
	# Organiza os dados para serem colocados em uma tabela pra melhor visualização.
	arq = formattation_file()
	indices = ['Nomes', 'Telefone', 'Estado', 'Observações']
	if data == '':
		contatos = [(i + 1, name, telephone, state, observation) for i, (name, telephone, state, observation) in enumerate(arq)]
	else:
		contatos = [(i + 1, name, telephone, state, observation) for i, (name, telephone, state, observation) in enumerate(data)]
	table = tab(contatos, headers=['Nro'] + indices, tablefmt="pipe")
	print(table)

def validation_names(name='',data=''):
	# Busca dividir nomes iguais, para passar listas com contagem, nomes iguais e nomes diferentes. Cada um separado dentro da lista.
	contact_x = []
	contact_y = []
	cont = 0
	for numb in range(len(data)):
		if name == data[numb][0]:
			cont += 1
			contact_x.append(data[numb])
		else:
			contact_y.append(data[numb])
	return [cont, contact_x, contact_y]


def remove_contact(name=''):
	# Faz remoção de um contato, apartir do seu nome. Caso tenha mais de um igual, abre possibilidade de escolha para excluir.
	arq = formattation_file()
	values = validation_names(name=name, data=arq)
	if values[0] > 1:
		formattation_contacts(data=values[1])
		ask = int(input('Escolha qual excluir pelo seu codigo da lista.\n|-> '))
		print(f'Contato {values[1][ask-1][0]} com telefone {values[1][ask-1][1]}, excluido com sucesso.')
		values[1].pop(ask-1)
		values[2].extend(values[1])
	else:
		print(f'Contato {values[1][0][0]} com telefone {values[1][0][1]}, excluido com sucesso.')
	file()
	return write_file(data=values[2], validation=False)


def add_observation(name=''):
	# Adiciona uma observação para um contato, mesmo ele já cadastrado.
	arq = formattation_file()
	values = validation_names(name=name,data=arq)
	if values[0] > 1:
		formattation_contacts(data=values[1])
		ask = int(input('Escolha qual contato deseja alterar a observação.\n|-> '))
		new_obs = input('Qual a nova observação.\n|-> ')
		values[1][ask-1][3] = new_obs
	file()
	return write_file(data=values[1], validation=False)


def show_observations(name=''):
	# Mostra observações colocadas pelo próprio usuario em cada contato, alguns podem possuir ou não.
	arq = formattation_file()
	for inf in arq:
		if name == inf[0]:
			try:
				print(f'{inf[0]} | {inf[3]}')
			except IndexError as e:
				print('Contato não possui observação')


def day_hour():
	# Função de atualização de hora e dia.
	values = datetime.datetime.now()
	hours = values.strftime("%H:%M:%S")
	day = values.strftime("%d:%m:%Y")
	return [day, hours]


def main():
	inf = arguments()
	if inf['show'] == 1:
		formattation_contacts()
	elif inf['remove'] != '':
		remove_contact(name=inf['remove'])
	elif inf['sobs'] != '':
		show_observations(inf['sobs'])
	elif inf['obs'] != '':
		add_observation(inf['obs'])
	else:
		if '&' in inf['name'] or inf['telephone'] == '0':
			print('\n\n\tOcorreu um erro, utilize o -h ou --help para maiores informações')
		else:
			ddos = phone_number_validation(inf['telephone'])
			if ddos[0] == 1:
				inf['estado'] = ddos[1]
				transformation = [inf['name'], inf['telephone'], inf['estado']]
				write_file(data=transformation, validation=True)
			else:
				pass

if __name__ == '__main__':
	main()

"""
Implementações:

	1- Trocar local de armaenamento, de arquivo para banco de dados.
	2- Alterar nome ou numero.
	3- Apagar mais de um contato por vez.
	5- Criar um Favoritador, onde será possivel colocar contatos como favorito.

"""
