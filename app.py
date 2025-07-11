import os
import dotenv
from google import genai
import json
import re
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_client import api_client
from CoffeMaster import data_splitter, interpretador
dotenv.load_dotenv()
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings


GEMINI_API_KEY =  os.environ.get("CHAVE_GOOGLE")
client = genai.Client(api_key=GEMINI_API_KEY)

with open("Bot_Gerador_de_Personagens\data\Instrucoes.md", "r", encoding="utf-8") as f:
    instrucoes = f.read()




def extrair_json_de_markdown(texto_ia):
    match = re.search(r"```json\s*(\{.*?\})\s*```", texto_ia, re.DOTALL)
    if match:
        json_str = match.group(1)
        return json.loads(json_str)
    else:
         raise ValueError("JSON não encontrado na resposta da IA.")




def criarPersonagem(descricao):
    pergunta = interpretador.fazer_pergunta(f"o jogador quer criar um personagem com a seguinte descrição {descricao}")
    geral = data_splitter.fazer_busca(pergunta)
    classes = f"qual a melhor classe e sublasse para criar um personagem com a seguinte descrição? {descricao}"
    classes_resposta = data_splitter.fazer_busca(classes)
    habilidades = f"qual as melhores habilidades e magias para criar um personagem com a seguinte descrição? {descricao}"
    habilidades_resposta = data_splitter.fazer_busca(habilidades)
    equipamentos = f"quais os melhores equipamentos para criar um personagem com a seguinte descrição? {descricao}"
    equipamentos_resposta = data_splitter.fazer_busca(equipamentos)
    dados = [geral, classes_resposta, habilidades_resposta, equipamentos_resposta]
    dados_text = []
    for documento in dados:
        dados_temp = "\n\n".join([doc.page_content for doc in documento])
        dados_text.append(dados_temp)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[dados_text, instrucoes, descricao,"Com base nos dados enviados, leia as instruções e o livro do jogador e gere um personagem para o usuário"]
    )
    print(extrair_json_de_markdown(response.text))
    return extrair_json_de_markdown(response.text)

def criarNpc(descricao):
    pergunta = interpretador.fazer_pergunta(f"o jogador quer criar um NPC com a seguinte descrição {descricao}")
    geral = data_splitter.fazer_busca(pergunta)
    classes = f"qual a melhor classe e sublasse para criar um NPC com a seguinte descrição? {descricao}"
    classes_resposta = data_splitter.fazer_busca(classes)
    habilidades = f"qual as melhores habilidades e magias para criar um NPC com a seguinte descrição? {descricao}"
    habilidades_resposta = data_splitter.fazer_busca(habilidades)
    equipamentos = f"quais os melhores equipamentos para criar um NPC com a seguinte descrição? {descricao}"
    equipamentos_resposta = data_splitter.fazer_busca(equipamentos)
    dados = [geral, classes_resposta, habilidades_resposta, equipamentos_resposta]
    dados_text = []
    for documento in dados:
        dados_temp = "\n\n".join([doc.page_content for doc in documento])
        dados_text.append(dados_temp)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[dados_text, instrucoes, descricao,"Com base nos dados enviados, leia as instruções e o livro do jogador e gere um NPC para o usuário"]
    )
    print(extrair_json_de_markdown(response.text))
    return extrair_json_de_markdown(response.text)
     
    
    


  

def alterarFicha(descricao, personagemNome, campanhaNome):
            personagem = api_client.buscarPersonagem(campanhaNome, personagemNome)
            prompt = f"Você é um bot gerador de personagens para rpg, o usuário quer fazer a seguinte alteração {descricao}, no seguinte personagem {personagem}. leia os arquivos {[ instrucoes]} e faça as alterações desejadas" 
            response = client.models.generate_content(
                  model="gemini-2.0-flash",
                  contents=[prompt]
            )
            print(extrair_json_de_markdown(response.text))
            return api_client.atualizarPersonagem(campanhaNome, extrair_json_de_markdown(response.text))

