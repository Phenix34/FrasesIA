function startProgress() {
    const progressBar = document.getElementById("progress-bar");
    const progressContainer = document.getElementById("progress-container");
    const phrasesContainer = document.getElementById("phrases-container");

    // Hide the start button
    const startButton = document.querySelector("button");
    startButton.style.display = "none";

    // Show the progress bar
    progressContainer.style.display = "block";

    let width = 0;
    const phrases = [
        "Calculando tu destino...",
        "Sintonizando las energías...",
        "Misterios desvelándose...",
        "Consultando las estrellas...",
"Explorando los misterios del destino...",
"Calculando tu suerte cósmica...",
"Descifrando los secretos del día...",
"Sintonizando con la inteligencia cósmica...",
"Leyendo las señales del universo...",
"Analizando los datos astrales...",
"Conectando con tu destino predicho...",
"Interpretando el oráculo virtual..."
    ];
    let phraseIndex = 0;

    const interval = setInterval(() => {
        if (width >= 100) {
            clearInterval(interval);
            // Redirect to /futuro when progress is complete
            window.location.href = "/futuro";
            startButton.style.display = "block";
            width = 0;
            progressBar.style.width = width + "%";
    // Show the progress bar
    progressContainer.style.display = "none";
        } else {
            width++;
            progressBar.style.width = width + "%";
            phraseIndex = (phraseIndex + 1) % phrases.length;
            phrasesContainer.innerText = phrases[phraseIndex];
        }
    }, 77);
}