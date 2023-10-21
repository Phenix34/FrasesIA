let partnerAnswer = null; // Variable to store the partner answer

    // Add event listeners to radio buttons to capture the answer
    document.getElementById("partner-yes").addEventListener("change", function() {
        partnerAnswer = "yes";
        enableEmpezarButton();
    });

    document.getElementById("partner-no").addEventListener("change", function() {
        partnerAnswer = "no";
        enableEmpezarButton();
    });
const partnerForm = document.getElementById("partner-form");
            const empezarButton = document.getElementById("custom-button");

            partnerForm.addEventListener("change", function() {
                const partnerYes = document.getElementById("partner-yes");
                const partnerNo = document.getElementById("partner-no");

                if (partnerYes.checked || partnerNo.checked) {
                    empezarButton.removeAttribute("disabled");
                } else {
                    empezarButton.setAttribute("disabled", "true");
                }
            });

function startProgress() {
    const partnerAnswer = getPartnerAnswer();
    const progressBar = document.getElementById("progress-bar");
    const progressContainer = document.getElementById("progress-container");
    const phrasesContainer = document.getElementById("phrases-container");
    const partnerForm = document.getElementById("partner-form");
    // Hide the start button
    const startButton = document.querySelector("button");
    startButton.style.display = "none";
    partnerForm.style.display = "none";
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
            window.location.href = `/futuro?partnerAnswer=${partnerAnswer}`;
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
    }, 40);
}
function getPartnerAnswer() {
    const partnerYes = document.getElementById("partner-yes");
    const partnerNo = document.getElementById("partner-no");

    if (partnerYes.checked) {
        return "yes";
    } else if (partnerNo.checked) {
        return "no";
    } else {
        return null;
    }
}
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('custom-button').addEventListener('click', function () {
        const partnerAnswer = document.querySelector('input[name="partnerAnswer"]:checked').value;
        // Send selectedPartnerValue to the server or store it where needed
    });
});