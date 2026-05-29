from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from playwright.async_api import async_playwright
import asyncio
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class DossierData(BaseModel):
    patient_nom: str
    patient_prenom: str
    patient_nss: str = ""
    mutuelle_nom: str
    mutuelle_numero_adherent: str = ""
    date_ordonnance: str = ""
    od_sphere: str = ""
    od_cylindre: str = ""
    od_axe: str = ""
    og_sphere: str = ""
    og_cylindre: str = ""
    og_axe: str = ""
    addition: str = ""
    type_verre: str = ""
    login: str = ""
    password: str = ""

@app.get("/")
def root():
    return {"status": "OPTIA Bot opérationnel"}

@app.post("/envoyer-almerys")
async def envoyer_almerys(data: DossierData):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()

            # Aller sur Almerys
            await page.goto("https://www.be-almerys.com")
            await page.wait_for_timeout(2000)

            # TODO mardi : ajouter les étapes 
            # de connexion et remplissage
            # après cartographie du portail

            await browser.close()

            return {
                "success": True,
                "message": "Bot Almerys lancé avec succès",
                "dossier": f"{data.patient_prenom} {data.patient_nom}"
            }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }

@app.get("/test-playwright")
async def test_playwright():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            await page.goto("https://www.google.com")
            title = await page.title()
            await browser.close()
            return {
                "success": True, 
                "message": f"Playwright fonctionne — page ouverte : {title}"
            }
    except Exception as e:
        return {"success": False, "message": str(e)}