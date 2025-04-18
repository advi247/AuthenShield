document.addEventListener('DOMContentLoaded', function () {
    const button = document.getElementById('start-button');
    const resultsDiv = document.getElementById('results');
    const loader = document.getElementById('loader');

    button.addEventListener('click', function () {
        button.disabled = true;
        button.innerText = 'Detecting...';
        resultsDiv.innerText = 'Running detection... please wait.';
        loader.style.display = 'block';  // Show the loader while detection runs

        fetch('/run-detection')
            .then(response => response.json())
            .then(data => {
                const output = data.output.join('\n');
                resultsDiv.innerText = output;
                button.disabled = false;
                button.innerText = 'Start Detection';
                loader.style.display = 'none'; // Hide the loader once detection is complete
            })
            .catch(error => {
                resultsDiv.innerText = 'Error: ' + error;
                button.disabled = false;
                button.innerText = 'Start Detection';
                loader.style.display = 'none'; // Hide the loader in case of an error
            });
    });
});
