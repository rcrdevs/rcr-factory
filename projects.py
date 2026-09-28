# -*- coding: utf-8 -*-
"""
Registro dos projetos que aparecem na Oficina.

Para adicionar um novo projeto, basta acrescentar um dict na lista PROJECTS —
nada mais no app precisa mudar.

Campos de cada projeto:
- url_env / url_default: onde o app está rodando. `url_env` é o nome da
  variável de ambiente que pode sobrescrever a URL (ver .env.example);
  `url_default` é o valor usado se a variável não estiver definida — como
  todos os projetos abaixo já estão publicados, o default já aponta pra URL
  real online.
- categoria: controla em qual coluna do quadro Kanban o card aparece.
  Só existem 3 valores válidos: "legacy" | "on-holding" | "under-dev"
  (ver CATEGORIAS logo abaixo). O Kanban é só visual — pra mover um projeto
  de coluna, edita esse campo aqui, não tem drag-and-drop nem banco de dados.
- status: "online" | "offline" — se o deploy está no ar.
- repo_url: link do repositório no GitHub, mostrado no card.
- ano: ano de referência do projeto, mostrado no card.
"""
import os

# Colunas do quadro Kanban, na ordem em que aparecem na tela.
# "cor" é só a chave usada no CSS (.of-kanban__col--<cor>), não muda o slug.
CATEGORIAS = [
    {"slug": "under-dev", "nome": "Under Dev", "cor": "green"},
    {"slug": "on-holding", "nome": "On Holding", "cor": "yellow"},
    {"slug": "legacy", "nome": "Legacy", "cor": "blue"},
]

PROJECTS = [
    {
        "id": "life-builder",
        "codigo": "LB-01",
        "nome": "Life Builder Assistant",
        "tagline": "Builds, missões diárias por área e progresso por ciclo para evoluir na vida real.",
        "descricao": (
            "Sistema de builds com missões geradas por ciclo de 14 dias, quiz "
            "personalizado por IA para temas de estudo, dieta com substituição "
            "de refeições e cálculo nutricional ao vivo, e recomendações com "
            "links reais de compra."
        ),
        "status": "online",
        "categoria": "under-dev",
        "ano": 2026,
        "tags": ["Flask", "SQLite", "IA"],
        "repo_url": "https://github.com/rcrdevs/life-builder-assistant",
        "url_env": "LIFE_BUILDER_URL",
        "url_default": "https://life-builder-assistant.onrender.com/",
        "embeddable": True,  # False = abre em nova aba em vez de iframe
    },
    {
        "id": "password-generator",
        "codigo": "PG-01",
        "nome": "Password Generator",
        "tagline": "Gerador de senhas seguras, direto ao ponto.",
        "descricao": (
            "Gera senhas fortes com regras configuráveis de tamanho e tipos de "
            "caractere — um dos primeiros projetos da bancada, hoje congelado "
            "como referência (categoria legacy)."
        ),
        "status": "online",
        "categoria": "legacy",
        "ano": 2022,
        "tags": ["Python", "Flask"],
        "repo_url": "https://github.com/rcrdevs/Password-Generator",
        "url_env": "PASSWORD_GENERATOR_URL",
        "url_default": "https://password-generator-6wq7.onrender.com/",
        "embeddable": True,
    },
    {
        "id": "dashboards-real-estate",
        "codigo": "DRE-01",
        "nome": "Dashboards Real Estate",
        "tagline": "Dashboards e visualizações de dados do mercado imobiliário.",
        "descricao": (
            "Painéis interativos com indicadores e gráficos sobre o mercado "
            "imobiliário — projeto legacy, mantido no ar como portfólio."
        ),
        "status": "online",
        "categoria": "legacy",
        "ano": 2023,
        "tags": ["Python", "Dash", "Plotly"],
        "repo_url": "https://github.com/rcrdevs/Dashboards-Real-Estate",
        "url_env": "DASHBOARDS_REAL_ESTATE_URL",
        "url_default": "https://dashboards-real-estate.onrender.com/",
        "embeddable": True,
    },
    {
        "id": "kripta-haus",
        "codigo": "KH-01",
        "nome": "Kripta Haus",
        "tagline": "Projeto em pausa, aguardando retomada.",
        "descricao": (
            "App publicado e funcionando, mas em compasso de espera — entra na "
            "coluna on-holding até voltar a receber trabalho ativo."
        ),
        "status": "online",
        "categoria": "on-holding",
        "ano": 2026,
        "tags": ["Next.js", "Vercel"],
        "repo_url": "https://github.com/rcrdevs/KriptaHaus",
        "url_env": "KRIPTA_HAUS_URL",
        "url_default": "https://kripta-haus.vercel.app/",
        "embeddable": True,
    },
]


def resolve_url(project):
    return os.environ.get(project["url_env"], project["url_default"])


def get_project(project_id):
    return next((p for p in PROJECTS if p["id"] == project_id), None)


def get_categoria(slug):
    return next((c for c in CATEGORIAS if c["slug"] == slug), None)
