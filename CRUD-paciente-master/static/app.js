document.getElementById('create-form').addEventListener('submit', async function (e) {
    e.preventDefault();
    const id = document.getElementById('create-id').value;
    const name = document.getElementById('create-name').value;
    const age = document.getElementById('create-age').value;
    const disease = document.getElementById('create-disease').value;
    
    const response = await fetch('/patients/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id, name, age, disease }),
    });

    if (response.ok) {
        alert('Paciente creado con éxito');
        fetchPatients();
    } else {
        alert('Error al crear el paciente');
    }
});

document.getElementById('fetch-patients').addEventListener('click', fetchPatients);

async function fetchPatients() {
    const response = await fetch('/patients/');
    const patients = await response.json();
    const patientsList = document.getElementById('patients-list');
    patientsList.innerHTML = '';
    patients.forEach(patient => {
        const li = document.createElement('li');
        li.textContent = `ID: ${patient.id}, Nombre: ${patient.name}, Edad: ${patient.age}, Enfermedad: ${patient.disease}`;
        patientsList.appendChild(li);
    });
}
