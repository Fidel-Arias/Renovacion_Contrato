document.getElementById("contratoForm").addEventListener('submit', (event) => {
    event.preventDefault();

    let formData = new FormData(document.getElementById("contratoForm"));

    // let data = {}
    const salario = document.getElementById("salario").value;
    // formData.forEach((value, key) => {
    //     data[key] = value;
    // })
    console.log('Salario', salario);

    fetch('http://127.0.0.1:8000/contract/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(salario)
    })
    .then((response) => response.json())
    .catch((error) => {
         console.error('Error:', error);
     });
})