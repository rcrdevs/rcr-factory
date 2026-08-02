# -*- coding: utf-8 -*-
"""
Estatísticas públicas do GitHub pros projetos catalogados (linguagens usadas,
total de commits). Usa só a API pública (sem autenticação, então sujeita ao
limite de 60 requisições/hora por IP do GitHub) e guarda o resultado em
memória por 1h -- se o GitHub estiver lento, indisponível ou o limite bater,
a função devolve o que tiver conseguido (ou nada) em vez de quebrar a
página; quem chama decide o que exibir.
"""
import time
from concurrent.futures import ThreadPoolExecutor

import requests

GITHUB_API = "https://api.github.com"
_TIMEOUT = 4
_CACHE_TTL = 3600  # 1h
_cache = {"data": None, "fetched_at": 0}


def _commit_count(repo):
    try:
        r = requests.get(
            f"{GITHUB_API}/repos/{repo}/commits", params={"per_page": 1}, timeout=_TIMEOUT
        )
        if r.status_code != 200:
            return None
        link = r.headers.get("Link", "")
        for part in link.split(","):
            if 'rel="last"' in part:
                url = part.split(";")[0].strip("<> ")
                return int(url.split("page=")[-1].split("&")[0])
        return len(r.json())  # sem Link header = so essa pagina (0 ou 1 commit)
    except Exception:
        return None


def _languages(repo):
    try:
        r = requests.get(f"{GITHUB_API}/repos/{repo}/languages", timeout=_TIMEOUT)
        if r.status_code != 200:
            return {}
        return r.json()
    except Exception:
        return {}


def _fetch_repo(repo):
    return repo, _languages(repo), _commit_count(repo)


def get_stats(repos, force=False):
    now = time.time()
    if not force and _cache["data"] is not None and (now - _cache["fetched_at"] < _CACHE_TTL):
        return _cache["data"]

    lang_bytes = {}
    total_commits = 0
    commits_ok = True

    with ThreadPoolExecutor(max_workers=max(len(repos), 1)) as pool:
        for _repo, langs, commits in pool.map(_fetch_repo, repos):
            for lang, n in langs.items():
                lang_bytes[lang] = lang_bytes.get(lang, 0) + n
            if commits is None:
                commits_ok = False
            else:
                total_commits += commits

    total_bytes = sum(lang_bytes.values())
    languages = []
    if total_bytes:
        for lang, n in sorted(lang_bytes.items(), key=lambda kv: kv[1], reverse=True):
            languages.append({"nome": lang, "pct": round(n * 100 / total_bytes, 1)})

    data = {
        "languages": languages,
        "total_commits": total_commits if commits_ok and total_commits else None,
    }
    _cache["data"] = data
    _cache["fetched_at"] = now
    return data
