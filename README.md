# POC — Model Context Protocol (MCP)

Preuve de concept réalisée dans le cadre du Learning Lab M2 DFS.
Démontre qu'un LLM peut appeler des outils externes de façon autonome via le protocole MCP.

## C'est quoi ?

Un serveur MCP local exposant **5 outils** à Claude Desktop :

- `read_note` : lit un fichier .txt dans le dossier notes/
- `get_weather` : retourne la météo en temps réel via api.open-meteo.com
- `list_notes` : liste tous les fichiers disponibles dans notes/
- `search_notes` : cherche un mot-clé dans tous les fichiers
- `get_date` : retourne la date et l'heure actuelles

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

## Script de démo (5 questions)

Poser ces questions dans Claude Desktop (onglet Chat) dans l'ordre :

**1. Découverte**
`Utilise list_notes pour me dire quels documents tu as à disposition.`
→ Claude liste les 6 fichiers disponibles

**2. Recherche intelligente**
`Utilise search_notes pour trouver tous les documents qui parlent de budget.`
→ Claude explore tous les fichiers et trouve budget.txt

**3. Lecture de données privées**
`Lis le fichier equipe.txt et dis-moi qui est le tech lead du projet.`
→ Claude lit le fichier local et répond sans injection manuelle

**4. Combinaison multi-outils**
`Utilise get_date et get_weather pour me dire si l'équipe de Villejuif devrait travailler en présentiel aujourd'hui.`
→ Claude combine 2 outils en une seule réponse

**5. Démo avant/après (moment pédagogique)**
`Quel temps fait-il à Paris ?`
→ Claude utilise sa recherche web (pas ton outil)
`Utilise get_weather pour me donner la météo à Paris.`
→ Claude utilise ton outil MCP — illustre l'importance des descriptions

→ Claude utilise ton outil MCP — illustre l'importance des descriptions

## État des lieux

Ce qui marche :

- [x] `read_note` — lecture fichier local avec chemin absolu
- [x] `get_weather` — appel API open-meteo en temps réel
- [x] `list_notes` — liste tous les fichiers du dossier notes/
- [x] `search_notes` — recherche par mot-clé dans tous les fichiers
- [x] `get_date` — date et heure système en temps réel
- [x] Combinaison multi-outils en une seule réponse autonome

Known Issues :

- Villes limitées à Paris, Lyon, Marseille, Villejuif (coordonnées codées en dur)
- Claude peut ignorer `get_weather` et utiliser sa recherche web si le prompt n'est pas explicite
- Pas de gestion des accents dans les noms de fichiers (ex: reunion.txt et non réunion.txt)

## Stack technique

- Python 3.14
- SDK MCP officiel Anthropic (`mcp`)
- `httpx` (appels HTTP async)
- `datetime` (date système)
- Claude Desktop (client MCP)
- API open-meteo.com (gratuite, sans clé API)

## Résultats

KPI 1 OUI — Claude appelle l'outil correct sans injection manuelle de données.
KPI 2 OUI — Claude combine plusieurs outils automatiquement en une seule réponse.
