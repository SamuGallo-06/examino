function format(command) {
    document.execCommand(command, false, null);
}

function clearContent() {
    document.getElementById("editor").innerHTML = "";
}

function downloadText() {
    const content = document.getElementById("editor").innerText;
    const blob = new Blob([content], { type: "text/plain" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "risposta.txt";
    a.click();
}

function formatFontFamily(font) {
    document.execCommand('fontName', false, font);
}

function formatFontSize(size) {
    document.execCommand("fontSize", false, size);
}

async function downloadPDF() {
  const content = document.getElementById("editor").innerText;
  const filename = document.getElementById("filename").value || "documento";

  const formData = new FormData();
  formData.append("latex", content);

  const response = await fetch("/generate-pdf", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    alert("Errore durante la generazione del PDF");
    return;
  }

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = filename.endsWith(".pdf") ? filename : `${filename}.pdf`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
}