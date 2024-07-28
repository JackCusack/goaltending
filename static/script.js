document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('theme-toggle');
    const body = document.body;

    // Check for saved user preference, if any, on load of the website
    const currentTheme = localStorage.getItem('theme') || 'dark';
    body.classList.add(currentTheme + '-mode');

    // Event listener for the toggle button
    toggleButton.addEventListener('click', () => {
        if (body.classList.contains('dark-mode')) {
            body.classList.replace('dark-mode', 'light-mode');
            localStorage.setItem('theme', 'light');
            toggleButton.textContent = 'Switch to Dark Mode';
        } else {
            body.classList.replace('light-mode', 'dark-mode');
            localStorage.setItem('theme', 'dark');
            toggleButton.textContent = 'Switch to Light Mode'
        }
    });
});

document.getElementById('statForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const gamesPlayed = document.getElementById('gamesPlayed').value;
    const shutouts = document.getElementById('shutouts').value;
    const goalsagainstaverage = document.getElementById('goalsagainstaverage').value;
    const savepercentage = document.getElementById('savepercentage').value;

    // Simple validation
    if (gamesPlayed && shutouts && goalsagainstaverage && savepercentage) {
        // Perform some action, like sending data to the server
        alert('Stats submitted!');
    } else {
        alert('Please fill in all fields.');
    }
});