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


prompt = """
Crie uma ficha para este personagem:

Edwyn é um humano de 32 anos, ex-membro de uma ordem de cavaleiros que foi dissolvida após uma guerra sangrenta. Desde então, trabalha como mercenário e guarda-costas para nobres em viagens perigosas. Apesar da aparência severa, possui um forte senso de honra e evita combates desnecessários. É silencioso, leal e extremamente resistente. Ele carrega uma armadura velha da ordem destruída e um escudo decorado com um brasão riscado. Seu estilo de combate é focado em defesa e controle de campo, mas é capaz de causar dano quando necessário.

Crie o personagem no nível 3, seguindo fielmente as regras do Livro do Jogador, sem adaptações. A ficha deve estar estruturada em JSON. Priorize durabilidade, defesa e utilidade em combate. Não use nada que não esteja nas regras padrão. Se o conceito do personagem não puder ser fielmente representado, siga as regras e explique brevemente o motivo (caso seja necessário).
"""


def criarHistoria(descrição):
     response = client.models.generate_content(
         model="gemini-2.0-flash",
         contents=[livroJogador, instrucoes, descrição, "Com base nos dados enviados, leia as instruções e o livro do jogador e gere um personagem para o usuário"]
     )

     print (response.text)


criarHistoria(prompt)
    