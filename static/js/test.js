function openApp(url) {
    // Prendi i valori dei campi del form (modifica con i tuoi ID o nomi)
    const candidateName = encodeURIComponent(document.querySelector('input[name="candidateName"]').value);
    const candidateSurname = encodeURIComponent(document.querySelector('input[name="candidateSurname"]').value);

    // Costruisci URL con query string
    const fullUrl = `${url}?candidateName=${candidateName}&candidateSurname=${candidateSurname}`;

    window.open(fullUrl, '_blank', 'width=1000,height=700,resizable=yes');
}