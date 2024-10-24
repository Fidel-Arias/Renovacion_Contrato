document.getElementById("contratoForm").addEventListener('submit', (event) => {
    event.preventDefault();

    let formData = new FormData(document.getElementById("contratoForm"));

    let data = {}
    formData.forEach((value, key) => {
        data[key] = value;
    })
    console.log(data);

    fetch('http://127.0.0.1:8000/generar-contrato', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then((response) => response.blob())
    .then((blob) => {
        //Generar link de descarga
        let url = window.URL.createObjectURL(blob);
        let a = document.createElement('a');
        a.href = url;
        a.download = 'Contrato.pdf';
        document.body.appendChild(a);
        a.click();
        a.remove();
    })
    .catch((error) => {
         console.error('Error:', error);
     });
})