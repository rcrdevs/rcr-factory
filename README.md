# Oficina

A bancada de testes dos seus projetos — um quadro Kanban de 3 colunas
(**Legacy**, **On Holding**, **Under Dev**) com um card por app, preview ao
vivo da página e link direto pro repositório. Cada card abre o app embutido
(via iframe) sem precisar decorar portas e URLs.

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

- 🔵 **Legacy** (azul) — projetos congelados, mantidos no ar como portfólio.
- 🟡 **On Holding** (amarelo) — publicados, mas em pausa.
- 🟢 **Under Dev** (verde) — em desenvolvimento ativo.

Pra mudar um projeto de coluna, edita o campo `"categoria"` dele em
`projects.py` (valores válidos: `"legacy"`, `"on-holding"`, `"under-dev"`).
Nada mais no código precisa mudar.

## Preview dos cards

A miniatura de cada card é um screenshot ao vivo da própria URL pública do
projeto, gerado sob demanda pelo serviço [thum.io](https://thum.io) — não
precisa gerar nem hospedar nenhuma imagem manualmente. Se o serviço não
conseguir capturar a página (app fora do ar, bloqueio, etc.), o card cai
graciosamente pra um estado "sem preview".

## Como rodar

### Docker (recomendado)

```bash
cp .env.example .env
docker compose up -d --build
```

Acesse **http://localhost:5050**.

> Importante: o iframe carrega no navegador de quem está acessando a
> Oficina, não no servidor dela. Todos os projetos catalogados já estão
> publicados (Render/Vercel), então isso só importa se você adicionar um
> projeto que ainda roda em `localhost`.

### Python direto

```bash
pip install -r requirements.txt
python app.py
```

## Adicionando um novo projeto

Abra `projects.py` e acrescente um dict na lista `PROJECTS`:

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
    "repo_url": "https://github.com/seu-usuario/meu-app",
    "url_env": "MEU_APP_URL",        # nome da variável de ambiente com a URL
    "url_default": "https://meu-app.onrender.com/",
    "embeddable": True,              # False = abre em nova aba em vez de iframe
}
```

Se o app novo bloquear ser exibido em iframe (por causa de cabeçalhos de
segurança como `X-Frame-Options` ou uma Content-Security-Policy própria),
marque `"embeddable": False` — a Oficina mostra um botão de "abrir em nova
aba" em vez de tentar embutir.

## Deploy no Render

1. Suba este repositório pro GitHub.
2. No Render, **New → Web Service**, conecte o repo.
3. Environment: **Docker** (o `Dockerfile` já está pronto) — ou, se preferir
   sem Docker: Build command `pip install -r requirements.txt`, Start command
   `gunicorn --bind 0.0.0.0:$PORT app:app`.
4. Não é obrigatório configurar nenhuma variável de ambiente — os defaults em
   `projects.py` já apontam pras URLs reais. Só defina as variáveis do
   `.env.example` se quiser sobrescrever alguma URL sem editar código.

## Por que os apps não usam a mesma identidade visual da Oficina?

De propósito: a Oficina é a "casa", neutra, feita pra hospedar qualquer
projeto sem competir com a identidade visual de cada um. Cada app mantém a
cara que fizer sentido pra ele.
