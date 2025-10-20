import os
import requests


GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_API_URL = os.getenv('GEMINI_API_URL', 'https://api.gemini.example/v1/generate')


DEFAULT_HEADERS = {
'Authorization': f'Bearer {GEMINI_API_KEY}' if GEMINI_API_KEY else '',
'Content-Type': 'application/json'
}


PIRATE_INSTRUCTIONS = (
"Você é um barman pirata. Sempre responda em português brasileiro com sotaque pirata: use interjeições como 'Arr!', "
"chame o usuário de 'marujo' quando fizer sentido, e prefira termos como 'rum', 'cachaça', 'caneco', 'barril'. "
"Dê uma receita curta (nome do drink, ingredientes e modo de preparo) e tempo estimado. Seja criativo, divertido, mas claro."
)


# pós-processamento mínimo para garantir 'pirata'
REPLACEMENTS = {
'você': 'tu',
'você.': 'tu, marujo.',
}




def ensure_pirate_tone(text: str) -> str:
# pequenas substituições
out = text
for k, v in REPLACEMENTS.items():
out = out.replace(k, v)
if 'Arr!' not in out:
out = 'Arr! ' + out
return out




def suggest_recipe(ingredients_list):
prompt = PIRATE_INSTRUCTIONS + "


Ingredientes do usuário: " + ', '.join(ingredients_list) + "


Responda no formato:
Nome do Drink:
Ingredientes:
Modo de preparo:
Tempo estimado:
"


payload = {
'prompt': prompt,
'max_tokens': 300
}


# chamada simples POST — adapte conforme a API real do Gemini/SDK
resp = requests.post(GEMINI_API_URL, json=payload, headers=DEFAULT_HEADERS, timeout=15)
if resp.status_code != 200:
return f"Arr! Erro ao conversar com o modelo: {resp.status_code}"


data = resp.json()
# tenta extrair texto de resposta — adapte conforme o retorno real
text = data.get('text') or data.get('output') or ''
if not text:
# fallback
text = data.get('choices', [{}])[0].get('text', '') if isinstance(data.get('choices'), list) else ''
if not text:
return 'Arr! O modelo não respondeu direito.'


return ensure_pirate_tone(text)