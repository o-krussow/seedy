// Define the API URL
const apiUrl = 'http://localhost:5000/api';

let output_data = null;

// Make a GET request
fetch(apiUrl)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    //output_data = response.json();
    console.log(output_data); 
    return response.json();
  })
  .then(data => {
   // console.log(data);
    let a = 0;
  })
  .catch(error => {
    console.error('Error:', error);
  });

console.log(output_data);
