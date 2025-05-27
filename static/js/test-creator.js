let counter = 0;

function addInputGroup() {
      counter++;
      const container = document.getElementById('inputContainer');
      const group = document.createElement('div');
      group.className = 'question';
      group.innerHTML = `
        <h3>Domanda ${counter}</h3>
        <label>Domanda: <br/>
        <textarea>name="domanda_${counter}" required></textarea></label><br>
        <label>Tipo Domanda: 
        <select name="type_${counter}">
            <option value="true_false">Vero o falso</option>
            <option value="true_false_justify">Vero o falso Motivato</option>
            <option value="short_answer">Risposta breve</option>
            <option value="paragraph">Paragrafo</option>
            <option value="file-upload">Caricamento di file</option>
        </select>
        </label><br>
        <label>Valore: <input type="number" name="valore_${counter}" required></label><br>
        <label>Formato file: <input type="text" name="accept_${counter}"></label><br>
        <button type="button" onclick="this.parentElement.remove(); counter--">❌ Rimuovi</button>
      `;
      container.appendChild(group);
    }