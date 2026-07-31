# Oficina

Minha bancada de testes — um quadro Kanban de 3 colunas (**Legacy**, **On
Holding**, **Under Dev**) com um card por app, identidade visual própria por
projeto e link direto pro repositório. Cada card abre o app embutido (via
iframe) sem eu precisar decorar portas e URLs.

## Projetos catalogados

| Projeto | Repo | Status | Coluna | Ano |
|---|---|---|---|---|
| Life Builder Assistant | [rcrdevs/life-builder-assistant](https://github.com/rcrdevs/life-builder-assistant) | online | Under Dev | 2026 |
| Kripta Haus | [rcrdevs/KriptaHaus](https://github.com/rcrdevs/KriptaHaus) | online | On Holding | 2026 |
| Password Generator | [rcrdevs/Password-Generator](https://github.com/rcrdevs/Password-Generator) | online | Legacy | 2022 |
| Dashboards Real Estate | [rcrdevs/Dashboards-Real-Estate](https://github.com/rcrdevs/Dashboards-Real-Estate) | online | Legacy | 2023 |

## O quadro Kanban

O quadro é **só visual** — não tem drag-and-drop nem banco de dados. As 3
colunas são fixas e coloridas:

- 🔵 **Legacy** (azul) — projetos congelados, que mantenho no ar como portfólio.
- 🟡 **On Holding** (amarelo) — publicados, mas em pausa.
- 🟢 **Under Dev** (verde) — em desenvolvimento ativo.

Pra mudar um projeto de coluna, edito o campo `"categoria"` dele em
`projects.py` (valores válidos: `"legacy"`, `"on-holding"`, `"under-dev"`).
Nada mais no código precisa mudar.

## Preview dos cards

Testei usar um serviço de screenshot ao vivo, mas os apps no plano free do
Render dormem e demoram pra acordar — o preview vinha inconsistente ou
cortado, e como cada captura tinha um tamanho diferente, os cards ficavam
desalinhados. Troquei por uma identidade visual gerada localmente: monograma
do nome do projeto sobre um gradiente com a cor da coluna (a mesma lógica de
cores do Kanban), sempre no mesmo tamanho (`aspect-ratio: 16/9`), sem
depender de nenhum serviço externo nem quebrar se algum app estiver fora do
ar.

## Como rodo localmente

### Docker (recomendado)

```bash
cp .env.example .env
docker compose up -d --build
```

Acesso em **http://localhost:5050**.

> O iframe carrega no navegador de quem acessa a Oficina, não no servidor
> dela. Todos os projetos catalogados já estão publicados (Render/Vercel),
> então isso só importa se eu adicionar um projeto que ainda roda em
> `localhost`.

### Python direto

```bash
pip install -r requirements.txt
python app.py
```

## Como adiciono um novo projeto

Abro `projects.py` e acrescento um dict na lista `PROJECTS`:

```python
{
    "id": "meu-app",                 # usado na URL /app/meu-app
    "codigo": "MA-01",               # código de catálogo mostrado no card
    "nome": "Meu App",
    "tagline": "Uma frase curta que resume o que ele faz.",
    "descricao": "Um parágrafo um pouco mais longo, para quem quer entender antes de clicar.",
    "status": "online",              # "online" | "offline"
    "categoria": "under-dev",        # "legacy" | "on-holding" | "under-dev"
    "ano": 2026,
    "tags": ["Flask", "Postgres"],
    "repo_url": "https://github.com/rcrdevs/meu-app",
    "url_env": "MEU_APP_URL",        # nome da variável de ambiente com a URL
    "url_default": "https://meu-app.onrender.com/",
    "embeddable": True,              # False = abre em nova aba em vez de iframe
}
```

Se o app novo bloquear ser exibido em iframe (por causa de cabeçalhos de
segurança como `X-Frame-Options` ou uma Content-Security-Policy própria),
marco `"embeddable": False` — a Oficina mostra um botão de "abrir em nova
aba" em vez de tentar embutir.

## Deploy no Render

1. Subo este repositório pro GitHub.
2. No Render: **New → Web Service**, conecto o repo.
3. Environment: **Docker** (o `Dockerfile` já está pronto) — ou, sem Docker:
   Build command `pip install -r requirements.txt`, Start command
   `gunicorn --bind 0.0.0.0:$PORT app:app`.
4. Não preciso configurar nenhuma variável de ambiente — os defaults em
   `projects.py` já apontam pras URLs reais. Só uso as variáveis do
   `.env.example` se quiser sobrescrever alguma URL sem editar código.

## Por que os apps não usam a mesma identidade visual da Oficina?

De propósito: a Oficina é a "casa", neutra, feita pra hospedar qualquer
projeto sem competir com a identidade visual de cada um. Cada app mantém a
cara que fizer sentido pra ele.
