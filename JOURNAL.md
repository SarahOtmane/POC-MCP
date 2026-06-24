# Journal de bord — POC MCP

## Pourquoi ce projet ?

Explorer le Model Context Protocol (MCP) d'Anthropic, un protocole standard qui permet à un LLM de se connecter à des outils externes de façon découplée et réutilisable.

Contexte : développeuse full stack sans expérience LLM, apprentissage from scratch du paradigme "exposer des outils plutôt qu'orchestrer".

---

## Session 1 — Setup (date : 24\06\2026)

**Durée : 1h**

Ce que j'ai fait :

- [x] Init Git + .gitignore
- [x] Création virtualenv Python
- [x] pip install mcp httpx
- [x] Premier serveur vide qui démarre

Problèmes rencontrés :
→ aucun

Solution trouvée :
→

---

## Session 2 — Outil read_note (date : 24\06\2026)

**Durée : 2h**

Ce que j'ai fait :

- [x] Codé read_note(filename)
- [x] Testé avec fichier existant
- [x] Testé avec fichier inexistant

Problèmes rencontrés :
→ il ne trouve pas projet.txt parce que le serveur cherche le fichier dans notes/ relatif à l'endroit où il est lancé, pas dans le dossier poc-mcp.

Solution trouvée :
→ Remplacer filepath = os.path.join("notes", filename) par :
BASE_DIR = os.path.dirname(os.path.abspath(**file**))
filepath = os.path.join(BASE_DIR, "notes", filename)

---

## Session 3 — Outil get_weather (date : \_\_\_)

**Durée : 2h**

Ce que j'ai fait :

- [ ] Codé get_weather(city)
- [ ] Testé l'appel API open-meteo
- [ ] Vérification des données retournées

Problèmes rencontrés :
→

Solution trouvée :
→

---

## Session 4 — Intégration Claude Desktop (date : \_\_\_)

**Durée : 1h**

Ce que j'ai fait :

- [ ] Configuré claude_desktop_config.json
- [ ] Relancé Claude Desktop
- [ ] Vérifié que les outils apparaissent

Problèmes rencontrés :
→

---

## Session 5 — Tests et démo (date : \_\_\_)

**Durée : 3h**

Questions testées :

1. "Lis ma note projet.txt et résume-la"
   → Résultat :

2. "Quel temps fait-il à Paris ?"
   → Résultat :

3. "Lis ma note reunion.txt et dis-moi
   s'il fait beau à Paris aujourd'hui"
   → Résultat :

KPI 1 validé ? oui / non
KPI 2 validé ? oui / non

---

## Limitations connues (Known Issues)

→ (liste ici les bugs non résolus)

## Ce que j'ai appris

→ (tes vraies conclusions, en 3 phrases)
