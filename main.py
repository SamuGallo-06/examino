import json
import os
from flask import Flask, render_template, request, abort, send_file
import markdown
from weasyprint import HTML
import test_utils
import configparser
from ascii_arts import *
import time

print(LOGO, flush=True)
print("[INFO]: Inizializzazione...", flush=True)
time.sleep(0.5)
app = Flask(__name__)

print("[INFO]: Creazione file di log...", flush=True)
time.sleep(0.5)
with open("examino.log", "w") as logFile:
    logFile.truncate(0)
logFile = open("examino.log", "a")
print("[INFO]: Creazione file di log completata", flush=True)
time.sleep(0.5)

print("[INFO]: Lettura file di configurazione...", flush=True)
time.sleep(0.5)
cfg = configparser.ConfigParser()

#Create settings.ini if it doesn't exist
if not os.path.exists("settings.ini"):
    with open("settings.ini", "x"):
        pass

#Read config File with ConfigParser
cfg.read("settings.ini")
    
if not cfg.has_section("EXAMINO"):
    print("[INFO]: Creazione file di configurazione...", flush=True)
    time.sleep(0.5)
    try:
        with open("settings.ini", "w") as settingsFile:
            cfg.add_section("EXAMINO")
            cfg.set("EXAMINO", "percorso_esami", "exams")
            cfg.set("EXAMINO", "percorso_archivio", "archivio_esami")
            cfg.set("EXAMINO", "percorso_upload", "uploads")
            cfg.write(settingsFile)
    except Exception as e:
        print("[ERRORE]: Creazione file di configurazione non riuscita", flush=True)
        time.sleep(0.5)
        exit(1)
    else:
        print("[INFO]: Configurazione creata con successo", flush=True)
        time.sleep(0.5)
        
print("[INFO]: Caricamento configurazione...", flush=True)
time.sleep(0.5)
EXAMS_FOLDER = cfg.get("EXAMINO", "percorso_esami")
EXAMS_ARCHIVE = cfg.get("EXAMINO", "percorso_archivio")
UPLOAD_FOLDER = cfg.get("EXAMINO", "percorso_upload")
print(f"[INFO]: Percorso Esami: {EXAMS_FOLDER}", flush=True)
print(f"[INFO]: Percorso Archivio: {EXAMS_ARCHIVE}", flush=True)
print(f"[INFO]: Percorso Upload: {UPLOAD_FOLDER}", flush=True)
print("[INFO]: Creazione directory...", flush=True)
time.sleep(0.5)

try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(EXAMS_FOLDER, exist_ok=True)
    os.makedirs(EXAMS_ARCHIVE, exist_ok=True)
except Exception as e:
    print("[ERRORE]: Creazione directory non riuscita", flush=True)
    time.sleep(0.5)
    exit(1)
else:   
    print("[INFO]: Creazione directory completata", flush=True)
    time.sleep(0.5)

print("[INFO]: Inizializzazione route...", flush=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/test', methods=['POST'])
def access_test():
    nome = request.form.get('nome')
    cognome = request.form.get('cognome')
    codice_test = request.form.get('codice_test')
    
    filepath = os.path.join(EXAMS_FOLDER, f'{codice_test}.json')
    if not os.path.exists(filepath):
        return "Test non trovato", 404

    with open(filepath, 'r', encoding='utf-8') as f:
        exam_data = json.load(f)
        question_texts = []
        question_types = []
        question_formats = []
        
        for q in exam_data["questions"]:
            question_texts.append(q.get("question"))
            question_types.append(q.get("type"))
            question_formats.append(q.get("format"))
            
    
    combined_questions = list(zip(question_texts, question_types, question_formats))

    return render_template(
        'test.html',
        examTitle=exam_data["title"],
        nome=nome,
        cognome=cognome,
        questions=combined_questions,
        codice_test=codice_test
    )
    
@app.route("/submit", methods=["POST"])
def submit():
    # Recupero dati dal form
    test_name = request.form.get("test_name")
    codice_test = request.form.get("codice_test")
    candidateName = request.form.get("candidateName")
    candidateSurname = request.form.get("candidateSurname")

    filepath = os.path.join(EXAMS_FOLDER, f"{codice_test}.json")
    if not os.path.exists(filepath):
        return "Test non trovato", 404

    # Caricamento dati del test
    with open(filepath, 'r', encoding='utf-8') as f:
        exam_data = json.load(f)

    questions = exam_data["questions"]
    votoMax = int(exam_data["max_score"])
    sogliaSufficenza = int(exam_data["sufficiency_mark"])
    autocorrect = bool(exam_data["autocorrect"])

    # Setup directory archivio e AI
    currentExamDir = test_utils.CreaTestInArchivio(candidateName, candidateSurname, codice_test)
    test_utils.setup()

    # Inizializzazione report
    allegati_dir = os.path.join(currentExamDir, "allegati")
    os.makedirs(allegati_dir, exist_ok=True)
    report_path = os.path.join(currentExamDir, "report.md")
    with open(report_path, "w", encoding="utf-8") as report:
        report.write(f"Candidato: {candidateSurname} {candidateName}<br>\n")
        report.write(f"Codice test: {codice_test}<br>\n")
        report.write(f"Percorso test: {currentExamDir}<br>\n")
        report.write(f"# {test_name}<br>\n\n")

        score = 0
        results = []
        totalScore = 0

        for idx, q in enumerate(questions, start=1):
            key = f"q{idx}"
            report.write(f"### {idx}. {q['question']}<br>\n")
            report.write(f"Tipo di domanda: {q['type'].replace('_', ' ').capitalize()}<br>\n")

            user_answer = None
            correct = False
            response = ""

            if q["type"] == "file-upload":
                uploaded_file = request.files.get(key)
                if uploaded_file and uploaded_file.filename:
                    file_path = os.path.join(allegati_dir, uploaded_file.filename)
                    uploaded_file.save(file_path)
                    uploaded_file.close()
                    report.write(f"File caricato: {uploaded_file.filename}<br>\n")
                    if autocorrect:
                        response = test_utils.correggi_file(domanda=q["question"], filePath=file_path, maxScore=q["value"])
                    responseObj = json.loads(response)
                    correct = responseObj["valutazione"] == "RISPOSTA_CORRETTA"
                    comment = responseObj["commento"]
                    currentQuestionScore = int(responseObj["punteggio"])
                else:
                    correct=False
                    comment="Nessun file caricato"
            else:
                user_answer = request.form.get(key, "none")
                motivation = request.form.get(f"{key}_motivation", "")

                report.write(f"Risposta: {user_answer}<br>\n")
                if motivation:
                    report.write(f"Motivazione: {motivation}<br>\n")

                if autocorrect and user_answer != "none":
                    try:
                        if q["type"] == "true_false_justify":
                            response = test_utils.correggi_vero_falso_motivato(q["question"], user_answer, motivation, maxScore=q["value"])
                        else:
                            response = test_utils.correggi_risposta(q["question"], user_answer, maxScore=q["value"])
                        responseObj = json.loads(response)
                        correct = responseObj["valutazione"] == "RISPOSTA_CORRETTA"
                        comment = responseObj["commento"]
                        currentQuestionScore = int(responseObj["punteggio"])
                    except Exception as e:
                        abort(500, f"[Errore correzione AI] {e}")

            # Assegnazione punteggio
            if autocorrect:
                if correct:
                    report.write(f"Risposta corretta<br>\n")
                    report.write(f"Punteggio: {currentQuestionScore}/{q['value']}<br>\n")
                    score += currentQuestionScore
                else:
                    report.write(f"Risposta errata<br>\n")
                    report.write(f"Punteggio: 0/{q['value']}<br>\n")
                    
                report.write(f"Commento: {comment}")
                
            totalScore += q["value"]

            results.append({
                "question": q["question"],
                "user_answer": user_answer or uploaded_file.filename if q["type"] == "file-upload" else "N/D",
                "correct": correct if autocorrect else "Non valutata",
                "comment": comment,
                "score": currentQuestionScore,
                "maxScore": q["value"]
            })

        voto = test_utils.calcola_voto(score, totalScore, votoMax)

    # Generazione PDF
    with open(report_path, "r", encoding="utf-8") as md_file:
        html_content = markdown.markdown(md_file.read())
        HTML(string=html_content).write_pdf(os.path.join(currentExamDir, "report.pdf"))

    return render_template(
        "results.html",
        results=results,
        score=score,
        total=totalScore,
        voto=voto,
        votoMax=votoMax,
        examTitle=test_name,
        sogliaSufficenza=sogliaSufficenza,
        candidateName=candidateName,
        candidateSurname=candidateSurname,
        autocorrect=autocorrect
    )

@app.route('/text-editor', methods=["GET"])
def text_editor():    
    return render_template(
        "text-editor.html",
    )

@app.route('/math-editor', methods=["GET"])
def math_editor():
    return render_template(
        "math-editor.html",
    )
    
@app.route("/math-editor/generate-pdf", methods=["POST"])
def generate_pdf():
    latex_code = request.form.get("latex")
    filename = request.form.get("filename")
    
    if filename == "":
        filename = "formula"
    
    pdf_path = os.path.join("uploads", f"{filename}.tex")
    with open(pdf_path, "w") as file:
        file.truncate(0)
        file.write(latex_code)

    return send_file(pdf_path, as_attachment=True, download_name=f"{filename}.pdf")

@app.route("/control-panel", methods=["GET", "POST"])
def ControlPanel():
    return render_template(
        "control-panel.html",
        restart=False
    )
    
@app.route("/control-panel/save", methods=["POST"])
def SaveSettings():
    print("[INFO]: Ricarica della configurazione in corso...", flush=True)
    percorso_esami = str(request.form.get("percorso-esami")).strip()
    percorso_archivio = str(request.form.get("percorso-archivio")).strip()
    
    if not cfg.has_section("EXAMINO"):
        cfg.add_section("EXAMINO")
    
    with open("settings.ini", "w") as settingsFile:
        cfg.set("EXAMINO", "percorso_esami", percorso_esami)
        cfg.set("EXAMINO", "percorso_archivio", percorso_archivio)
        cfg.set("EXAMINO", "percorso_upload", "uploads")
        cfg.write(settingsFile)
        
    test_utils.setup()
    
    print("[INFO]: Ricarica della configurazione completata", flush=True)
    return render_template(
        "control-panel.html",
        restart=True
    )
    
@app.route("/test-creator", methods=["GET", "POST"])
def TestCreator():
    return render_template(
        "test-creator.html",
        success=False
    )
    
@app.route("/test-creator/save", methods=["POST"])
def SaveTest():
    
    test_name = request.form.get("nome_test")
    test_code = request.form.get("codice_test")
    total_score = int(request.form.get("punteggio_totale"))
    max_score = int(request.form.get("voto_massimo"))
    sufficient_mark = int(request.form.get("soglia_sufficenza"))
    autocorrect = bool(request.form.get("test_autocorrect") == "True")
    
    try:
        examData = {
            "title": test_name,
            "total_score": total_score,
            "max_score": max_score,
            "sufficiency_mark": sufficient_mark,
            "autocorrect": autocorrect,
        }
        
        questionsData = {}
        for key in request.form:
            if "_" in key and key not in ["title", "total_score", "max_score", "sufficiency_mark", "autocorrect"]:
                field, index = key.rsplit("_", 1)
                if index not in questionsData:
                    questionsData[index] = {}
                questionsData[index][field] = request.form[key]

        # Costruisci l'array di questionsData
        questionList = []
        for idx in sorted((k for k in questionsData if k.isdigit()), key=int):
            item = questionsData[idx]

            questionList.append({
                "type": item.get("type", ""),
                "format": item.get("format", ""),
                "accept": item.get("accept", ""),
                "question": item.get("domanda", ""),
                "value": int(item.get("valore", 0))
            })

        # Aggiungi le domande all'oggetto finale
        examData["questions"] = questionList
        
        examSavePath = os.path.join(EXAMS_FOLDER, f"{test_code}.json")
        
        with open(examSavePath, "w", encoding="utf-8") as examFile:
            json.dump(examData, examFile, ensure_ascii=False, indent=2)
    
    except Exception as error:
        print(f"[ERRORE]: Si è verificato un errore nella creazione dell'esame. Seguono i dettagli dell'errore:\n        {error}", flush=True)
        abort(500, f"[ERRORE]: Si è verificato un errore nella creazione dell'esame. Seguono i dettagli dell'errore:\n{error}")
    
    return render_template(
        "test-creator.html",
        success=True,
    )

time.sleep(0.5)    
print("[INFO]: Avvio dell'applicazione in corso...", flush=True)
time.sleep(0.5)

if __name__ == "__main__":
    app.run()