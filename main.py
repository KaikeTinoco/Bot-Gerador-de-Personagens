import os
import dotenv
from google import genai
dotenv.load_dotenv()
GEMINI_API_KEY =  os.environ.get("CHAVE_GOOGLE")
client = genai.Client(api_key=GEMINI_API_KEY)
chat = client.chats.create(model="gemini-2.0-flash")

with open("data/Instrucoes.md", "r", encoding="utf-8") as f:
    instrucoes = f.read()

with open("data/LivroJogador.md", "r", encoding="utf-8") as f:
    livroJogador = f.read()


def criarPersonagem(descrição):
     response = client.models.generate_content(
         model="gemini-2.0-flash",
         contents=[livroJogador, instrucoes, descrição, "Com base nos dados enviados, leia as instruções e o livro do jogador e gere um personagem para o usuário"]
     )

    #A API salva o personagem
     print (response.text)

    
    

vauban = '''{
  "nome": "Vauban",
  "idade": 25,
  "sexo": "Masculino",
  "raca": "Anão da Colina",
  "classe": "Clérigo",
  "subclasse": "Domínio da Forja",
  "nivel": 3,
  "tendencia": "Neutro Bom",
  "antecedente": "Artesão de Guilda",
  "origem": "Vilarejo de Falkreath",
  "atributos": {
    "forca": 14,
    "destreza": 10,
    "constituicao": 17,
    "inteligencia": 12,
    "sabedoria": 14,
    "carisma": 8
  },
  "modificadores": {
    "forca": 2,
    "destreza": 0,
    "constituicao": 3,
    "inteligencia": 1,
    "sabedoria": 2,
    "carisma": -1
  },
  "vida": {
    "pontos_de_vida": 27,
    "dado_de_vida": "3d8"
  },
  "classe_armadura": {
    "base": 16,
    "escudo": 2,
    "bencao_da_forja": 1,
    "total": 19
  },
  "proficiencias": {
    "salvaguardas": ["Sabedoria", "Carisma"],
    "armas": ["Armas simples"],
    "armaduras": ["Armaduras pesadas", "Escudos"],
    "pericias": ["Intuição", "Persuasão"],
    "ferramentas": ["Ferramentas de Ferreiro", "Ferramentas de Culinária"],
    "idiomas": ["Comum", "Anão"]
  },
  "equipamentos": [
    "Martelo de Guerra",
    "Escudo",
    "Armadura de Cota de Malha",
    "Ferramentas de Ferreiro",
    "Ferramentas de Culinária",
    "Kit de Cura",
    "Mochila de Taverneiro",
    "Símbolo sagrado (talher de prata)"
  ],
  "magia": {
    "cd_magia": 12,
    "ataque_magico": "+4",
    "espacos": {
      "nivel_1": 4,
      "nivel_2": 2
    },
    "truques": ["Orientação", "Palavra Curadora", "Luz"],
    "nivel_1": ["Cura pelas Mãos", "Escudo de Fé", "Santuário"],
    "nivel_2": ["Acalmar Emoções", "Arma Espiritual"]
  },
  "caracteristicas": {
    "tracos": [
      "Sou prático, direto e cuido bem do que é meu. Especialmente minha cozinha.",
      "Nada é mais valioso do que compartilhar uma boa refeição com aliados."
    ],
    "ideais": [
      "Comunidade: Ajudar minha vila, proteger meus clientes, servir algo quente mesmo em tempos difíceis."
    ],
    "vinculo": "A taverna é meu legado, mas o calor da forja ainda chama meu nome.",
    "defeitos": "Tenho dificuldade em confiar em forasteiros — especialmente os que não respeitam o ofício manual."
  }
}'''

def fichaRecusada(descricao):
        while True:
            #Primeiro a API busca o personagem que vai ser alterado
            response = chat.send_message(f"Você é um bot gerador de personagens para rpg, o usuário quer fazer a seguinte alteração {descricao}, no seguinte personagem {vauban}. leia os arquivos {[livroJogador, instrucoes]} e faça as alterações desejadas" )
            print(response.text)
            #a variavel 'response' é enviada a API para então o usuário e ele valida 
            #se for validado, o personagem é atualizado no banco e o loop quebra
            #para teste, vou aprovar a alteração
            feedbackUser = True
            if (feedbackUser == True):
                #salva o pesonagem
                break


fichaRecusada("alterne o nome do personagem para Erik")