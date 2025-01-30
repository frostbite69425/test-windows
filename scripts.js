// Surprise message functionality
const surpriseBtn = document.getElementById("surpriseBtn");
const surpriseMessage = document.getElementById("surpriseMessage");

surpriseBtn.addEventListener("click", function() {
    surpriseMessage.innerHTML = "You are my heart, my soul, and my forever. I am so grateful to have you. 💕";
    surpriseMessage.classList.remove("animate__fadeIn");
    surpriseMessage.classList.add("animate__fadeIn");
    surpriseMessage.style.display = "block";
    surpriseBtn.style.display = "none"; // Hide the button after clicking
});
