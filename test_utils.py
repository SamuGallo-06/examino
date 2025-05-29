import re
import google.generativeai as gemini
import datetime, os

EXAMS_ARCHIVE = "archivio_esami"

def calcola_voto(punteggio, totale, votoMax):
    voto = (punteggio / totale) * votoMax
    return round(voto)
    
def setup():
    with open("gemini_apikey", "r") as apiKeyFile:
        apiKey = apiKeyFile.read()
    
    gemini.configure(api_key=apiKey)
    
def correggi_risposta(domanda = "", risposta="", maxScore=1):
    aiPrompt = f"""Domanda: "{domanda}";
Risposta: "{risposta}". 
Questa domanda è un vero o falso o una risposta aperta.
Punteggio massimo per questa domanda: {maxScore}

Correggi la risposta dello studente:
Rispondi solo in formato JSON con questa struttura:

{{
    "valutazione": "RISPOSTA_CORRETTA" o "RISPOSTA_ERRATA",
    "commento": "spiega molto brevemente il motivo",
    ""punteggio": "Assegna un punteggio alla risposta che non sia superiore al punteggio massimo"
}}

Rispondi solo con il contenuto JSON, senza includere ```json o altri simboli di formattazione Markdown.
"""
    geminiModel = gemini.GenerativeModel("gemini-2.0-flash-lite")
    response = geminiModel.generate_content(aiPrompt)
    print("_______________________________________________")
    print("Prompt: " + aiPrompt)
    print("Risposta: " + response.text)
    print("_______________________________________________")
    return ProcessResponse(response.text)

def correggi_file(domanda, filePath, maxScore):
    with open(filePath, "r") as file:
        fileContent = file.read()
        
    tipoFile = DetectFileType(filePath)
    
    aiPrompt = f"""Domanda: "{domanda}"
Questa domanda prevedeva il caricamento di un file. 
Contenuto del file caricato:
```{tipoFile}
{fileContent}
```
\n\n 
Valuta se il contenuto risponde correttamente alla domanda.
Punteggio massimo per questa domanda: {maxScore}
Rispondi solo in formato JSON con questa struttura:

{{
    "valutazione": "RISPOSTA_CORRETTA" o "RISPOSTA_ERRATA",
    "commento": "spiega molto brevemente il motivo o suggerisci miglioramenti",
    "punteggio": "Assegna un punteggio alla risposta che non sia superiore al punteggio massimo"
}}

Rispondi solo con il contenuto JSON, senza includere ```json o altri simboli di formattazione Markdown.
"""
    
    geminiModel = gemini.GenerativeModel("gemini-2.0-flash-lite")
    response = geminiModel.generate_content(aiPrompt)
    print("_______________________________________________")
    print("Prompt: " + aiPrompt)
    print("Risposta: " + response.text)
    print("_______________________________________________")
    return ProcessResponse(response.text)
    

def correggi_vero_falso_motivato(domanda = "", risposta=None, motivazione="", maxScore=1):
    aiPrompt = f"""Domanda: "{domanda}";
Risposta: "{risposta}". 
Questa domanda è un vero o falso motivando la risposta, 
L'utente ha motivato la sua risposta con: "{motivazione}".
Punteggio massimo per questa domanda: {maxScore}

Correggi la risposta dello studente:
Rispondi solo in formato JSON con questa struttura:

{{
    "valutazione": "RISPOSTA_CORRETTA" o "RISPOSTA_ERRATA",
    "commento": "spiega molto brevemente il motivo o suggerisci miglioramenti",
    "punteggio": "Assegna un punteggio alla risposta che non sia superiore al punteggio massimo"
}}

Rispondi solo con il contenuto JSON, senza includere ```json o altri simboli di formattazione Markdown.
"""

    geminiModel = gemini.GenerativeModel("gemini-2.0-flash-lite")
    response = geminiModel.generate_content(aiPrompt)
    print("_______________________________________________")
    print("Prompt: " + aiPrompt)
    print("Risposta: " + response.text)
    print("_______________________________________________")
    return ProcessResponse(response.text)

def CreaTestInArchivio(nome, cognome, codice_test):
    now = datetime.datetime.now()
    date = now.strftime("%d-%m-%Y")	
    currentExamDir = os.path.join(EXAMS_ARCHIVE, f"{cognome}_{nome}_{date}", codice_test)
    os.makedirs(currentExamDir, exist_ok=True)
    
    return currentExamDir

def DetectFileType(filePath):
    estensione = os.path.splitext(filePath)[1].lower()  # ".PY" → ".py"
    
    mapping = {
        ".py": "python",
        ".c": "c",
        ".cpp": "cpp",
        ".js": "javascript",
        ".ts": "typescript",
        ".html": "html",
        ".css": "css",
        ".tex": "latex",
        ".java": "java",
        ".rb": "ruby",
        ".go": "go",
        ".php": "php"
    }
    
    return mapping.get(estensione, "text")  #plain text se non trova l'estensione o non è tra quelle supportate

def ProcessResponse(response_text):
    # Cerca blocco di codice JSON tipo ```json ... ```
    match = re.search(r"```json\s*(\{.*?\})\s*```", response_text, re.DOTALL)
    if match:
        json_text = match.group(1)
    else:
        json_text = response_text.strip()  # fallback se non trova il blocco
        
    return json_text