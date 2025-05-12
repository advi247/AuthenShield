let keystrokes = [];

document.addEventListener('DOMContentLoaded', function () {
    const button = document.getElementById('start-button');
    const resultsDiv = document.getElementById('results');
    const loader = document.getElementById('loader');

    let lastKeyTime = null;

    document.addEventListener('keydown', (e) => {
        const now = Date.now();
        const delay = lastKeyTime ? now - lastKeyTime : 0;

        keystrokes.push({
            key: e.key,
            code: e.code,
            timestamp: now,
            delay: delay
        });

        lastKeyTime = now;

        if (keystrokes.length >= 20) {
            fetch('/log-keystrokes', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ log: keystrokes })
            })
            .then(res => res.json())
            .then(data => console.log(data.status))
            .catch(err => console.error('Keystroke log error:', err));

            keystrokes = [];
        }
    });

    button.addEventListener('click', function () {
        button.disabled = true;
        button.innerText = 'Detecting...';
        resultsDiv.innerText = 'Running detection... please wait.';
        loader.style.display = 'block';

        fetch('/run-detection')
            .then(response => response.json())
            .then(data => {
                const output = data.output.join('\n');
                resultsDiv.innerText = output;
                button.disabled = false;
                button.innerText = 'Start Detection';
                loader.style.display = 'none';
            })
            .catch(error => {
                resultsDiv.innerText = 'Error: ' + error;
                button.disabled = false;
                button.innerText = 'Start Detection';
                loader.style.display = 'none';
            });
    });
});
