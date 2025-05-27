const editor = document.getElementById("editor");
const preview = document.getElementById("preview");

editor.addEventListener("input", () => {
    const latex = editor.innerText;
    preview.innerText = latex;
    MathJax.typesetPromise([preview]);
});

function clearContent() {
    document.getElementById("editor").innerHTML = "";
}

function insertText(latex) {
    const editor = document.getElementById("editor");
    editor.focus();
    const selection = window.getSelection();
    
    if (!selection.rangeCount) return;

    const range = selection.getRangeAt(0);
    const textNode = document.createTextNode(latex);
    range.deleteContents(); // sostituisce eventuale selezione
    range.insertNode(textNode);

    // Sposta il cursore dopo il testo inserito
    range.setStartAfter(textNode);
    range.setEndAfter(textNode);
    selection.removeAllRanges();
    selection.addRange(range);
    updatePreview();
}

function updatePreview() {
    const latex = document.getElementById("editor").innerText;
    const preview = document.getElementById("preview");
    try {
        preview.innerHTML = katex.renderToString(latex, {
            throwOnError: false,
            displayMode: true
        });
    } catch (err) {
        preview.innerHTML = "<span style='color:red'>Errore nella formula</span>";
    }
}

function downloadPDF() {
    const filename = document.getElementById("filename").value;
    const latexFormula = document.getElementById("editor").innerText;
    const encoded = encodeURIComponent(latex);
    window.open("https://latexonline.cc/compile?text=" + encoded + "&download=true");
}