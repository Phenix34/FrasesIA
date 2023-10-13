 // Check if the progress bar has been shown
 const progressBarShown = sessionStorage.getItem("progressBarShown");

 if (!progressBarShown) {
     startProgress();

     // Set a flag to indicate that the progress bar has been shown
     sessionStorage.setItem("progressBarShown", "true");
 } else {
     // Redirect to /futuro if the progress bar has already been shown
     window.location.href = "/futuro";
 }