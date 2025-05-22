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
     
    
    


  

def alterarFicha(descricao, personagemNome, campanhaNome):
            personagem = api_client.buscarPersonagem(campanhaNome, personagemNome)
            response = chat.send_message(f"Você é um bot gerador de personagens para rpg, o usuário quer fazer a seguinte alteração {descricao}, no seguinte personagem {personagem}. leia os arquivos {[livroJogador, instrucoes]} e faça as alterações desejadas" )
            print(extrair_json_de_markdown(response.text))
            api_client.atualizarPersonagem(campanhaNome, extrair_json_de_markdown(response.text))



alterarFicha("altere o nome dele para Jackson", "Edward", "Engrenagens da Ascensao: Uma Saga Steampunk")