# serveur_mcp.py
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types
import httpx
import os
import asyncio

# ── Initialisation du serveur ──────────────────────────
app = Server("poc-mcp-sarah")

# ── Chemin absolu du projet ────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Coordonnées des villes supportées ─────────────────
VILLES_COORDS = {
    "Paris":     {"latitude": 48.85, "longitude": 2.35},
    "Lyon":      {"latitude": 45.75, "longitude": 4.85},
    "Marseille": {"latitude": 43.30, "longitude": 5.37},
    "Villejuif": {"latitude": 48.79, "longitude": 2.36},
}

# ── Déclaration des outils exposés au LLM ─────────────
@app.list_tools()
async def lister_outils():
    return [
        types.Tool(
            name="read_note",
            description=(
                "Lit le contenu d'un fichier texte dans le dossier notes/. "
                "À utiliser quand l'utilisateur demande de lire, consulter "
                "ou résumer une note, un fichier ou un document local."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Nom du fichier avec extension, ex: projet.txt"
                    }
                },
                "required": ["filename"]
            }
        ),
        types.Tool(
            name="get_weather",
            description=(
                "Retourne la température actuelle en degrés Celsius pour une ville. "
                "À utiliser quand l'utilisateur pose une question sur la météo, "
                "la température, ou s'il fait beau quelque part."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Nom de la ville en français, ex: Paris"
                    }
                },
                "required": ["city"]
            }
        ),
        types.Tool(
            name="list_notes",
            description=(
                "Liste tous les fichiers disponibles dans le dossier notes/. "
                "À utiliser quand l'utilisateur demande quels documents, fichiers "
                "ou notes sont disponibles, ou avant de chercher un fichier précis."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]

# ── Exécution des outils ───────────────────────────────
@app.call_tool()
async def executer_outil(name: str, arguments: dict):

    if name == "read_note":
        filename = arguments.get("filename", "")
        filepath = os.path.join(BASE_DIR, "notes", filename)

        if not os.path.exists(filepath):
            return [types.TextContent(
                type="text",
                text=f"Erreur : le fichier '{filename}' n'existe pas dans le dossier notes/."
            )]

        with open(filepath, "r", encoding="utf-8") as fichier:
            contenu = fichier.read()

        return [types.TextContent(
            type="text",
            text=f"Contenu de {filename} :\n\n{contenu}"
        )]

    if name == "get_weather":
        city = arguments.get("city", "Paris")
        coords = VILLES_COORDS.get(city, VILLES_COORDS["Paris"])

        async with httpx.AsyncClient() as client:
            reponse = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude":        coords["latitude"],
                    "longitude":       coords["longitude"],
                    "current_weather": True
                },
                timeout=10.0
            )

        data = reponse.json()
        temperature = data["current_weather"]["temperature"]
        vitesse_vent = data["current_weather"]["windspeed"]

        return [types.TextContent(
            type="text",
            text=f"Météo à {city} : {temperature}°C, vent {vitesse_vent} km/h."
        )]

    if name == "list_notes":
        notes_path = os.path.join(BASE_DIR, "notes")
        fichiers = [
            f for f in os.listdir(notes_path)
            if f.endswith(".txt")
        ]

        if not fichiers:
            return [types.TextContent(
                type="text",
                text="Aucun fichier trouvé dans le dossier notes/."
            )]

        liste = "\n".join(f"- {f}" for f in sorted(fichiers))
        return [types.TextContent(
            type="text",
            text=f"Fichiers disponibles dans notes/ :\n\n{liste}"
        )]

    return [types.TextContent(type="text", text=f"Outil inconnu : {name}")]

# ── Point d'entrée ─────────────────────────────────────
async def main():
    async with stdio_server() as (flux_lecture, flux_ecriture):
        await app.run(flux_lecture, flux_ecriture, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())