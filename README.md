# POC — Model Context Protocol (MCP)

Preuve de concept réalisée dans le cadre du Learning Lab M2 DFS.
Démontre qu'un LLM peut appeler des outils externes de façon autonome via le protocole MCP.

## C'est quoi ?

Un serveur MCP local exposant 2 outils à Claude Desktop :

- `read_note` : lit un fichier .txt dans le dossier notes/
- `get_weather` : retourne la météo via api.open-meteo.com

## Installation

```bash
# Cloner le repo
git clone https://github.com/sarahotmane/poc-mcp.git
cd poc-mcp

# Créer et activer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows : venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

## Lancement

```bash
python serveur_mcp.py
```

Le serveur démarre et attend une connexion d'un client MCP (Claude Desktop).

## Configuration Claude Desktop

Modifier le fichier `~/Library/Application Support/Claude/claude_desktop_config.json` :

```json
{
  "mcpServers": {
    "poc-mcp": {
      "command": "/chemin/absolu/vers/poc-mcp/venv/bin/python",
      "args": ["/chemin/absolu/vers/poc-mcp/serveur_mcp.py"]
    }
  }
}
```

Remplace `/chemin/absolu/vers/poc-mcp` par le résultat de `pwd` dans ton dossier projet.
Puis quitte et relance Claude Desktop.

Pour vérifier que la connexion est établie :

```bash
tail -f ~/Library/Logs/Claude/mcp-server-poc-mcp.log
```

Tu dois voir : `Server started and connected successfully`

## Test de la démo

Poser ces 3 questions dans Claude Desktop (onglet Chat) :

1. `Lis ma note projet.txt et résume-la`
   → Claude appelle `read_note` automatiquement

2. `Utilise l'outil get_weather pour me donner la température à Paris`
   → Claude appelle `get_weather` et retourne la météo en temps réel

3. `Lis ma note reunion.txt et dis-moi s'il fait beau à Paris aujourd'hui`
   → Claude combine les 2 outils en une seule réponse

## État des lieux

Ce qui marche :

- [x] `read_note` — lecture fichier local avec chemin absolu
- [x] `get_weather` — appel API open-meteo en temps réel
- [x] Combinaison des 2 outils en une seule réponse autonome

Known Issues :

- Villes limitées à Paris, Lyon, Marseille, Villejuif (coordonnées codées en dur)
- Claude peut ignorer `get_weather` et utiliser sa recherche web si le prompt n'est pas explicite
- Pas de gestion des accents dans les noms de fichiers (ex: reunion.txt et non réunion.txt)

## Stack technique

- Python 3.14
- SDK MCP officiel Anthropic (`mcp`)
- `httpx` (appels HTTP async)
- Claude Desktop (client MCP)
- API open-meteo.com (gratuite, sans clé API)

## Résultats

KPI 1 OUI — Claude appelle l'outil correct sur 3/3 questions sans injection manuelle de données.
KPI 2 OUI — Claude combine `read_note` + `get_weather` automatiquement sur la question 3.
