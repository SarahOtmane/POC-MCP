# Journal de bord — POC MCP

## Pourquoi ce projet ?

Explorer le Model Context Protocol (MCP) d'Anthropic, un protocole standard qui permet à un LLM de se connecter à des outils externes de façon découplée et réutilisable.

Contexte : développeuse full stack sans expérience LLM, apprentissage from scratch du paradigme "exposer des outils plutôt qu'orchestrer".

---

## Session 1 — Setup (date : 24/06/2026)

**Durée : 30min**

Ce que j'ai fait :

- [x] Init Git + .gitignore
- [x] Création virtualenv Python
- [x] pip install mcp httpx
- [x] Premier serveur vide qui démarre

Problèmes rencontrés :
→ aucun

Solution trouvée :
→ /

---

## Session 2 — Outil read_note (date : 24/06/2026)

**Durée : 30min**

Ce que j'ai fait :

- [x] Codé read_note(filename)
- [x] Testé avec fichier existant
- [x] Testé avec fichier inexistant

Problèmes rencontrés :
→ Le serveur ne trouvait pas projet.txt car il cherchait notes/ relativement au répertoire de lancement, pas au dossier du projet.

Solution trouvée :
→ Utiliser un chemin absolu avec BASE_DIR = os.path.dirname(os.path.abspath(**file**)) puis filepath = os.path.join(BASE_DIR, "notes", filename). Leçon : toujours utiliser des chemins absolus dans un serveur MCP.

---

## Session 3 — Outil get_weather (date : 24/06/2026)

**Durée : 30min**

Ce que j'ai fait :

- [x] Codé get_weather(city)
- [x] Testé l'appel API open-meteo
- [x] Vérification des données retournées

Problèmes rencontrés :
→ Quand je posais "Quel temps fait-il à Paris ?", Claude utilisait sa recherche web intégrée au lieu de mon outil MCP. Le LLM choisit l'outil qu'il juge le plus adapté — si la description n'est pas assez précise ou si une autre capacité lui semble plus pertinente, il l'ignore.

Solution trouvée :
→ Reformuler le prompt pour nommer explicitement l'outil : "Utilise l'outil get_weather pour me donner la température à Paris." Leçon : la description des outils MCP doit être très précise pour guider le LLM.

---

## Session 4 — Intégration Claude Desktop (date : 24/06/2026)

**Durée : 30min**

Ce que j'ai fait :

- [x] Configuré claude_desktop_config.json
- [x] Relancé Claude Desktop
- [x] Vérifié que les outils apparaissent dans les logs

Problèmes rencontrés :
→ L'icône marteau n'apparaissait pas dans l'interface malgré une connexion réussie. Confusion entre compte Free et compte Pro dans Claude Desktop — le serveur MCP était configuré mais sur le mauvais compte.

Solution trouvée :
→ Vérifier les logs avec tail -f ~/Library/Logs/Claude/mcp\*.log pour confirmer la connexion. Se connecter avec le bon compte (Pro). La ligne "Server started and connected successfully" dans les logs confirme que tout fonctionne même sans indicateur visuel.

---

## Session 5 — Tests et démo (date : 24/06/2026)

**Durée : 1h**

Questions testées :

1. "Lis ma note projet.txt et résume-la"
   → Résultat :
   "Voici le résumé de ta note projet.txt : Il s'agit d'un POC (Proof of Concept) appelé Learning Lab, dont l'objectif est de démontrer qu'un LLM peut, via le protocole MCP, lire des fichiers locaux et appeler des APIs externes."

2. "Utilise l'outil get_weather pour me donner la température à Paris."
   → Résultat :
   "Il fait actuellement 39,9°C à Paris, avec un vent de 7,6 km/h."

3. "Lis ma note reunion.txt et dis-moi s'il fait beau à Paris aujourd'hui"
   → Résultat : (deux outils appelés automatiquement en une seule réponse)
   "La réunion du 24 juin a permis de valider le périmètre du POC. Il fait 39,9°C avec un vent de 7,6 km/h — il fait beau mais extrêmement chaud !"

KPI 1 validé ? OUI — Claude appelle l'outil correct sur 3/3 questions sans données injectées dans le prompt.
KPI 2 validé ? OUI — Claude combine les 2 outils (read_note + get_weather) en une seule réponse sur la question 3.

---

## Limitations connues (Known Issues)

→ Les villes supportées par get_weather sont limitées à Paris, Lyon, Marseille et Villejuif (coordonnées codées en dur). Toute autre ville retombe sur Paris par défaut.
→ Claude peut ignorer l'outil get_weather et utiliser sa recherche web intégrée si le prompt n'est pas formulé explicitement. La description de l'outil mériterait d'être affinée.
→ Pas de gestion des accents dans les noms de fichiers (ex: réunion.txt au lieu de reunion.txt).

---

## Ce que j'ai appris

→ MCP inverse le paradigme du développement classique : au lieu d'orchestrer moi-même les appels API dans mon code, j'expose des capacités et c'est le LLM qui décide quand et comment les utiliser. C'est un changement conceptuel majeur pour une dev full stack habituée à tout contrôler.
→ La qualité des descriptions d'outils est critique : le LLM choisit ses outils en lisant leur description en langage naturel, comme un développeur lit une documentation. Une description floue = un outil ignoré.
→ MCP standardise ce que chaque équipe réinventait de son côté — c'est l'équivalent de ce que HTTP a fait pour le web : un protocole unique, des implémentations multiples et interopérables.
