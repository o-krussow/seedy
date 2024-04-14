const apiUrl = 'http://localhost:5000/api';
const outputElement = document.getElementById('output');

fetch(apiUrl)
    .then(response => {
	if (!response.ok)){
	    throw new Error('Network response was not ok');
	}
	return response.json();
    })
    .then(data => {
	outputElement.textContent = JSON.stringify(data, null, 2);
    })
    .catch(error => {
	console.error('Error:', error);
    });
