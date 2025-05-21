import os
import dotenv
from google import genai
import json
import re
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_client import api_client

dotenv.load_dotenv()
GEMINI_API_KEY =  os.environ.get("CHAVE_GOOGLE")
client = genai.Client(api_key=GEMINI_API_KEY)
chat = client.chats.create(model="gemini-2.0-flash")

with open("Bot Gerador de Personagens\data\Instrucoes.md", "r", encoding="utf-8") as f:
    instrucoes = f.read()

with open("Bot Gerador de Personagens\data\LivroJogador.md", "r", encoding="utf-8") as f:
    livroJogador = f.read()

with open("Bot Gerador de Personagens\data\Monstros_formatado.md", "r", encoding="utf-8") as f:
    monstros = f.read()


def extrair_json_de_markdown(texto_ia):
    match = re.search(r"```json\s*(\{.*?\})\s*```", texto_ia, re.DOTALL)
    if match:
        json_str = match.group(1)
        return json.loads(json_str)
    else:
        raise ValueError("JSON não encontrado na resposta da IA.")


def criarPersonagem(descrição, campanhaId):
     response = client.models.generate_content(
         model="gemini-2.0-flash",
         contents=[livroJogador, instrucoes, descrição, "Com base nos dados enviados, leia as instruções e o livro do jogador e gere um personagem para o usuário"]
     )
     print(extrair_json_de_markdown(response.text))
     api_client.criarPersonagem(extrair_json_de_markdown(response.text), campanhaId)
     
    
    


  

def fichaRecusada(descricao, personagem):
        while True:
            #Primeiro a API busca o personagem que vai ser alterado
            response = chat.send_message(f"Você é um bot gerador de personagens para rpg, o usuário quer fazer a seguinte alteração {descricao}, no seguinte personagem {personagem}. leia os arquivos {[livroJogador, instrucoes]} e faça as alterações desejadas" )
            print(response.text)
            #a variavel 'response' é enviada a API para então o usuário e ele valida 
            #se for validado, o personagem é atualizado no banco e o loop quebra
            #para teste, vou aprovar a alteração
            feedbackUser = True
            if (feedbackUser == True):
                #salva o pesonagem
                break

prompt = '''Dante, um dono de uma nova cafeteria chamada Grillbys, é um humano com descendência anã (mas ainda não descobriu) de tamanho normal (1.75m) com um corpo visivelmente forte, mas que esconde os musculos por baixo de uma camada de gordura,
 que é o barista e cozinheiro da cafeteteria. Ele tem 25 anos e além de trabalhar no Grillbys, esta tentando aprender a ser um ferreiro especializado nas novas tecnologias que estão surgindo e gosta de praticar lutas com alguns de seus clientes que são aventureiros ou mercenários; 
Ele trabalha sozinho no Grillbys e gosta de cozinhar e fazer bebidas para seus clientes, além de conversar e interagir com os clientes mais proximos, é amado por todos seus clientes. Dante acredita que pode ajudar os outros dando um bom alimento e bebida,
junto de um ouvido amigo para ouvir o próximo e ama o que faz, mas sente um leve disconforto na sua vida atual pois acha que não é tão relevante ou famoso. Dante será mais focado em defesa e suporte, mas ainda com potencial de causar dano caso necessário.
faça ele no nível 3 '''

criarPersonagem(prompt, 7)