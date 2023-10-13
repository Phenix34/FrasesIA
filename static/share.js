// Get references to the buttons and the <h1> element
const likeButton = document.getElementById('like-button');
const dislikeButton = document.getElementById('dislike-button');
const shareButton = document.getElementById('share-button');
const predictionQuestion = document.getElementById('prediction-question');

// Function to toggle button visibility and change the text
function toggleButtons() {
    likeButton.style.display = 'none';
    dislikeButton.style.display = 'none';
    shareButton.style.display = 'block';
    predictionQuestion.textContent = '¡Prueba tu suerte de nuevo o la de tus amigos!';
}
shareButton.addEventListener('click', function() {
    // Redirect to the specified URL when the button is clicked
    window.location.href = '/';
});
// Add click event listeners to the like and dislike buttons
likeButton.addEventListener('click', toggleButtons);
dislikeButton.addEventListener('click', toggleButtons);
