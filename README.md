# Examino

**Examino v1.0** è uno strumento creato da **Samuele Gallicani** per la generazione e la gestione di esami personalizzati online.

Permette di creare test strutturati con supporto alla sintassi **LaTeX** per equazioni matematiche e include un **editor di testo** integrato. A fine test viene generato un **report PDF**.  
La correzione può avvenire manualmente o tramite **intelligenza artificiale (Gemini AI)**, a scelta dell'utente.

---

## 🧩 Tipi di domande supportati

- ✅ Vero o falso  
- ✅ Vero o falso motivato  
- ✅ Risposta breve  
- ✅ Risposta multipla  
- ✅ Paragrafo  
- ✅ Caricamento di file

---

## 🔧 Uso

### `/test-creator`  
Pagina per creare test personalizzati.

### `/test`  
Pagina dove si svolge la prova di verifica. Da qui è possibile accedere:
- all'**editor di testo**  
- all'**editor di equazioni LaTeX**

### `/control-panel`  
Pannello di controllo per gestire le **impostazioni del programma**, incluse le opzioni di correzione automatica con AI.

---

## Correzione degli esami

È possibile scegliere tra:
- Correzione **manuale**. Il test non verrà corretto automaticamente, e nella schermata dei risultati non sarà visibile il punteggio o l'esito.
- Correzione automatica tramite **Gemini AI**. Viene assegnato un punteggio in base alla risposta, e i risultati saranno immediatamente visibili. Funzione implementata per superare i limiti delle attuali puattaforme di test online, che prevedono una correzione rigida della risposta.

---

## 📝 Output

Al termine del test, viene generato un **report PDF** con le risposte e i risultati dell'esame.

---

## 📄 Licenza

Rilasciato con licenza **Copyleft** – il codice è libero di essere usato, modificato e distribuito, purché le versioni derivate restino anch'esse libere.

---

## 👤 Autore

Sviluppato da **Samuele Gallicani**
