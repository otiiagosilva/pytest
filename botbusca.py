import telebot
import requests
import re
import time
import io
import json
from PIL import Image
import io
import base64

bot = telebot.TeleBot("5998015531:AAGUzJ-0XefFAEJ_VaShSBBm-eNIlc1Npqc", parse_mode=None)

PRIVADO = [950764540]

###################################

GRUPO = [-1001238994280]

###################################

EXCEPT = [950764540]



# Função para exibir o menu
@bot.message_handler(commands=['busca'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()

    # Criação dos botões com comandos e exemplos
    btn_nome = telebot.types.InlineKeyboardButton('/nome - Consultar nome', callback_data='consultar_nome')
    markup.add(btn_nome)
    
    btn_telefone = telebot.types.InlineKeyboardButton('/tel Consultar telefone', callback_data='consultar_telefone')
    markup.add(btn_telefone)
    
    btn_telefone1 = telebot.types.InlineKeyboardButton('/tel1 - Consultar telefone1', callback_data='consultar_telefone1')
    markup.add(btn_telefone1)
    
    btn_foto = telebot.types.InlineKeyboardButton('/foto - Consultar foto por nome', callback_data='consultar_foto')
    markup.add(btn_foto)
    
    btn_cpffree1 = telebot.types.InlineKeyboardButton('/cpf1 - Consultar cpffree1', callback_data='consultar_cpffree1')
    markup.add(btn_cpffree1)
    
    btn_cpffree = telebot.types.InlineKeyboardButton('/cpf - Consultar cpffree', callback_data='consultar_cpffree')
    markup.add(btn_cpffree)

  
    # Adicionar texto sobre a conformidade com a LGPD
    lgpd_text = "O 🆂🅺🆈🅽🅴🆁🅳 está de acordo com a lei LGPD (Lei geral de proteção de dados pessoais nº13.709) aprovada em agosto de 2018!\n\nOfereço esse serviço para fins particulares e não econômicos (custo é para desenvolvimento do projeto e mão de obra da hospedagem do servidor)."
    
    # Enviar a mensagem com o menu e o texto da LGPD
    bot.send_message(message.chat.id, lgpd_text, reply_markup=markup)

# Função para processar os botões de callback
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id

    if call.data == 'consultar_nome':
        bot.send_message(chat_id, 'Exemplo: /nome MARIA HILDA ALVES DE LUNA')
    elif call.data == 'consultar_telefone':
        bot.send_message(chat_id, 'Exemplo: /tel1 11947694236')
    elif call.data == 'consultar_telefone1':
        bot.send_message(chat_id, 'Exemplo: /tel 81988515542')
    elif call.data == 'consultar_foto':
        bot.send_message(chat_id, 'Exemplo: /foto Fabianna dos Santos Sobreira Ambires')
    elif call.data == 'consultar_cpffree1':
        bot.send_message(chat_id, 'Exemplo: /cpf1 17934419449')
    elif call.data == 'consultar_cpffree':
        bot.send_message(chat_id, 'Exemplo: /cpf 01065963300')



@bot.message_handler(commands=['nome', 'NOME', 'telefone', 'tel', 'tel1','telefone1', 'foto', 'cpffree1', 'cpf1', 'cpffree','cpf'])
def processar_comandos(message):
    chat_id = message.chat.id 
    liberado_nome = PRIVADO + GRUPO + EXCEPT

    if chat_id in liberado_nome:
        args = message.text.split(' ')
        comando = args[0]

        if comando == '/nome' or comando == '/NOME':
            consultar_nome(message, args)

        elif comando == '/telefone'  or comando == '/tel':
            consultar_telefone(message, args)

        elif comando == '/telefone1' or comando == '/tel1':
            consultar_telefone1(message, args)

        elif comando == '/foto':
            consultar_foto(message, args)

        elif comando == '/cpffree1' or comando == '/cpf1':
            consultar_cpffree1(message, args)

        elif comando == '/cpffree' or comando == '/cpf':
            consultar_cpffree(message, args)
            
def consultar_nome(message):
    chat_id = message.chat.id
    liberado_nome = PRIVADO + GRUPO + EXCEPT

    if chat_id in liberado_nome:
        bot.send_message(chat_id, '<code>CONSULTANDO...</code>', parse_mode='HTML')

        nome_comando = message.text.replace("/nome ", "")

        try:
            url = f'http://apifree.minerdxc.tk:8080/api/nomes?nome={nome_comando}'
            response = requests.get(url).json()

            if response.get('statusCode') == 200 and "resultado" in response and isinstance(response["resultado"], list):
                text = "<b>🔎 CONSULTA DE NOME 🔎</b>\n\n"

                for pessoa in response['resultado']:
                    text += "▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱\n"
                    text += f"<b>• NOME</b>: {pessoa['Nome']}\n"
                    text += f"<b>• CPF</b>: {pessoa['CPF']}\n"
                    text += f"<b>• Data de Nascimento</b>: {pessoa['Data de Nascimento']}\n"
                    text += "▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱\n\n"

                bot.send_message(chat_id, text, parse_mode='HTML')

            else:
                bot.send_message(chat_id, "NOME NÃO ENCONTRADO")
        except Exception as e:
            print(e)
            bot.send_message(chat_id, "Erro ao consultar o nome")

def consultar_telefone(message, args):
    chat_id = message.chat.id
    liberado_nome = PRIVADO + GRUPO + EXCEPT

    if chat_id in liberado_nome:
        if len(args) < 2:
            bot.send_message(
                chat_id,
                'Por favor, forneça um número de telefone após o comando /telefone.',
                parse_mode='Markdown'  # Adicione esta linha para que o Markdown funcione corretamente
            )
            return

        bot.send_message(
            chat_id,
            '⚠️ *Aguarde, esta consulta pode demorar!*',
            parse_mode='Markdown'  # Adicione esta linha para que o Markdown funcione corretamente
        )

        telef = args[1]

        # Verifique se o telefone fornecido possui apenas números
        if not telef.isdigit():
            bot.send_message(
                chat_id,
                "Telefone inválido. Por favor, insira apenas números (sem espaços ou caracteres especiais)."
            )
            return

        # Verifique se o telefone fornecido tem 10 ou 11 dígitos
        if len(telef) < 10 or len(telef) > 11:
            bot.send_message(
                chat_id,
                "Telefone inválido. Por favor, insira um número de telefone com 10 ou 11 dígitos."
            )
            return

        try:
            start_time = time.time()  # Registrar o momento inicial

            response = requests.get(
                f'http://apifree.minerdxc.tk:8080/api/telefones1?telefone={telef}'
            )

            end_time = time.time()  # Registrar o momento após a chamada da API
            elapsed_time = end_time - start_time  # Calcular o tempo decorrido em segundos

            data = response.json()

            # Enviar a resposta da API para o bot, incluindo o tempo de resposta em segundos
            bot.send_message(
                chat_id,
                f"{data['message']}\nTempo de resposta da API: {elapsed_time:.2f} segundos",
                parse_mode='Markdown'  # Adicione esta linha para que o Markdown funcione corretamente
            )
        except Exception as e:
            print("Erro ao consultar telefone:", str(e))
            bot.send_message(
                chat_id,
                "Ocorreu um erro ao consultar o telefone. Por favor, tente novamente mais tarde.",
                parse_mode='Markdown'  # Adicione esta linha para que o Markdown funcione corretamente
            )


def consultar_telefone1(message, args):
    chat_id = message.chat.id
    liberado_nome = PRIVADO + GRUPO + EXCEPT

    if chat_id in liberado_nome:
        if len(args) < 2:
            bot.send_message(
                chat_id,
                "Uso incorreto do comando. Digite /telefone1 seguido pelo número de telefone desejado."
            )
            return

        telefs = args[1]

        # Verifique se o telefone fornecido possui apenas números
        if not telefs.isdigit():
            bot.send_message(
                chat_id,
                "Telefone inválido. Por favor, insira apenas números (sem espaços ou caracteres especiais)."
            )
            return

        # Verifique se o telefone fornecido tem 10 ou 11 dígitos
        if len(telefs) < 10 or len(telefs) > 11:
            bot.send_message(
                chat_id,
                "Telefone inválido. Por favor, insira um número de telefone com 10 ou 11 dígitos."
            )
            return

        try:
            start_time = time.time()  # Registrar o momento inicial

            response = requests.get(
                f'http://apifree.minerdxc.tk:8080/api/telefone?numero={telefs}'
            )

            end_time = time.time()  # Registrar o momento após a chamada da API
            elapsed_time = end_time - start_time  # Calcular o tempo decorrido em segundos

            data = response.json()

            # Enviar a resposta da API para o bot, incluindo o tempo de resposta em segundos
            bot.send_message(
                chat_id,
                f"{data['message']}\nTempo de resposta da API: {elapsed_time:.2f} segundos"
            )
        except Exception as e:
            print("Erro ao consultar telefone:", str(e))
            bot.send_message(
                chat_id,
                "Ocorreu um erro ao consultar o telefone. Por favor, tente novamente mais tarde."
            )


def consultar_foto(message, args):
    chat_id = message.chat.id
    liberado_nome = PRIVADO + GRUPO + EXCEPT

    if chat_id in liberado_nome:
        nomeCidadao = ' '.join(args[1:])  # O nome do cidadão a ser buscado

        try:
            response = requests.get(
                f'http://apifree.minerdxc.tk:8080/api/foto?no_cidadao={nomeCidadao}'
            )
            data = response.json()

            if data.get('foto'):
                imageBase64 = data['foto']  # Foto em formato base64
                buffer = io.BytesIO(base64.b64decode(imageBase64))

                # Criar um objeto de imagem com o Pillow
                image = Image.open(buffer)
                
                # Salvar a imagem em um arquivo (opcional)
                image.save('foto_cidadao.jpg')
                
                # Enviar a foto como mensagem para o remetente
                bot.send_photo(chat_id, image, caption='Foto do cidadão')
            else:
                # Caso a API não retorne uma foto
                bot.reply_to(message, 'Foto não encontrada para esse cidadão.')
        except Exception as e:
            print('Erro ao buscar foto:', str(e))
            bot.reply_to(message, 'Ocorreu um erro ao buscar a foto.')

            

def consultar_nome(message, args):
    chat_id = message.chat.id
    liberado_nome = PRIVADO + GRUPO + EXCEPT

    if chat_id in liberado_nome:
        bot.reply_to(message, '<code>CONSULTANDO...</code>', parse_mode='HTML')

        nome_comando = ' '.join(args[1:])

        try:
            startTime = time.perf_counter()  # Registrar o momento inicial

            url = f'http://apifree.minerdxc.tk:8080/api/nomes?nome={nome_comando}'
            response = requests.get(url).json()

            endTime = time.perf_counter()  # Registrar o momento após a chamada da API
            elapsedTime = endTime - startTime  # Calcular o tempo decorrido em segundos
            elapsedTimeMinutes = elapsedTime / 60  # Converter para minutos

            data = response.get('message', '')  # Acesse a propriedade "message" da resposta

            # Use expressões regulares para extrair informações relevantes
            matches = re.findall(r'Nome: (.*?)\nCPF: (.*?)\nData de Nascimento: (.*?)\n', data)

            if matches:
                formattedResult = '\n'.join([f"Nome: {match[0]}\nCPF: {match[1]}\nData de Nascimento: {match[2]}" for match in matches])

                # Enviar os resultados como uma mensagem formatada
                bot.reply_to(message, f'<b>🔎 CONSULTA DE NOME 🔎</b>\n\n{formattedResult}\nTempo de resposta da API: {elapsedTimeMinutes:.2f} minutos', parse_mode='HTML')
            else:
                bot.reply_to(message, "Nenhum resultado encontrado para o nome fornecido.")
        except Exception as e:
            print(e)
            bot.reply_to(message, "Ocorreu um erro ao consultar o nome")

def consultar_cpffree1(message, args):
    chat_id = message.chat.id
    liberado_nome = PRIVADO + GRUPO + EXCEPT

    if chat_id in liberado_nome:
        if len(args) < 2:
            bot.reply_to(message, 'Por favor, forneça um número de CPF após o comando /cpffree1.')
            return

        cpf_comando = args[1]

        if not cpf_comando.isdigit() or len(cpf_comando) != 11:
            bot.reply_to(message, '<b>DIGITE UM CPF VÁLIDO!</b>', parse_mode='HTML')
        else:
            try:
                url = f'http://apifree.minerdxc.tk:8080/api/cpf2?cpf={cpf_comando}'
                response = requests.get(url).json()
                if "message" in response:
                    bot.reply_to(message, response["message"])
                else:
                    bot.reply_to(message, str(response))  # Envia a resposta da API diretamente
            except Exception:
                bot.reply_to(message, "ERRO AO CONSULTAR CPF")




def consultar_cpffree(message, args):
    chat_id = message.chat.id
    liberado_nome = PRIVADO + GRUPO + EXCEPT

    if chat_id in liberado_nome:
        nome5 = ' '.join(args[1:])

        try:
            response = requests.get(f'http://apifree.minerdxc.tk:8080/api/cpf?cpf={nome5}')
            data = response.json()

            if data:
                formattedResult = 'Resultados da consulta CPF:\n'

                for entry in data:
                    formattedResult += '\n'  # Linha em branco entre cada entrada

                    # Use expressões regulares para extrair chaves e valores dentro das chaves {}
                    matches = re.findall(r'{(.*?)}', entry)

                    if matches:
                        for match in matches:
                            keyValuePairs = match.split(',')

                            # Formate cada par chave-valor
                            formattedPairs = []

                            for pair in keyValuePairs:
                                parts = pair.split(':', 1)
                                if len(parts) == 2:
                                    key, value = parts
                                    formattedKey = f'<b>{key.strip()}</b>'
                                    formattedPairs.append(f'{formattedKey}: {value.strip()}')

                            formattedResult += '\n'.join(formattedPairs)

                # Remova os espaços desnecessários entre as chaves e os valores
                formattedResult = formattedResult.replace('*:', '*')

                bot.reply_to(message, formattedResult, parse_mode='HTML')
            else:
                bot.reply_to(message, 'Nenhum resultado encontrado para o CPF fornecido.')
        except Exception as e:
            print('Erro ao consultar CPF:', str(e))
            bot.reply_to(message, 'Ocorreu um erro ao consultar o CPF.')

print('BOT ONLINE SKYNERD BUSCA @batmonn ✅!!!')

bot.polling(none_stop = True)