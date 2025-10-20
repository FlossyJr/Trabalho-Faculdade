// main.js — interação da página de sugestões de drinks


const form = document.getElementById('ingredients-form');
const input = document.getElementById('ingredients-input');
const result = document.getElementById('result');


if (form) {
form.addEventListener('submit', async (e) => {
e.preventDefault();
const ingredients = input.value.trim();
if (!ingredients) {
result.textContent = 'Arr! Escreve algum ingrediente, marujo!';
return;
}


result.textContent = '☠️ O barman pirata está pensando...';


try {
const resp = await fetch('/api/suggest', {
method: 'POST',
headers: {
'Content-Type': 'application/json',
},
body: JSON.stringify({ ingredients }),
});


const data = await resp.json();
if (resp.ok) {
result.textContent = data.suggestion;
} else {
result.textContent = data.error || 'Arr! Algo deu errado na taverna!';
}
} catch (error) {
result.textContent = 'Arr! O mar revolto impediu a conexão!';
}
});
}