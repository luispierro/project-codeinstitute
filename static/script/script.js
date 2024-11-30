/* jshint esversion: 6 */

const overlayBackground = document.getElementById('overlay-background');
const aboutUsMessage = document.getElementById('aboutus-message');
const howWorksMessage = document.getElementById('howworks-message');
const errorMessage = document.getElementById("error-message"); // New: For displaying error messages

document.getElementById("upload-form").addEventListener("submit", function (event) {
    submitCSV.call(this, event); // Pass the event explicitly and bind 'this' to the form
});

document.getElementById("file-input").addEventListener("change", function () {
    const file = this.files[0];
    if (file && file.type !== "text/csv" && !file.name.endsWith(".csv")) {
        errorMessage.textContent = "Please upload a valid CSV file.";
        this.value = ""; // Clear the input
    }
});

function submitCSV(event) {
    event.preventDefault(); // Prevent the default form submission

    const formData = new FormData(this);
    const spinner = document.getElementById("spinner");
    const insightsContainer = document.querySelector(".insights");
    

    // Clear previous error message
    errorMessage.textContent = "";

    // Show the spinner
    spinner.style.display = "block";
    insightsContainer.style.display = "none"; // Hide the insights temporarily

    // Send the form data to the server
    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => {
        if (response.ok) {
            const contentType = response.headers.get("Content-Type");
            if (contentType && contentType.includes("application/json")) {
                // If JSON is returned, it's likely an error
                return response.json();
            } else {
                // If HTML is returned, process it as text (success case)
                return response.text();
            }
        } else {
            throw new Error("Error processing data");
        }
    })
    .then(data => {
        if (typeof data === "object" && data.error) {
            // Handle error returned as JSON
            errorMessage.textContent = data.error; // Display the error message
        } else {
            // Handle success case with returned HTML
            insightsContainer.innerHTML = data;
        }
    })
    .catch(error => {
        console.error("Error:", error);
        errorMessage.textContent = "There was an error processing your data.";
    })
    .finally(() => {
        // Hide the spinner
        spinner.style.display = "none";
        insightsContainer.style.display = "block";
    });
}

function navOpen(element){
    // function to display option selected on nav
    element.style.display = 'block';
    overlayBackground.style.display = 'block';
    element.scrollTop = 0;
}
function navClose(element){
    // function to close option selected on nav
    element.style.display = 'none';
    overlayBackground.style.display = 'none';
}

//Click listener for the about us button
document.getElementById("about-button").addEventListener("click", () => navOpen(aboutUsMessage));
document.getElementById("close-about").addEventListener("click", () => navClose(aboutUsMessage));
//Click listener for the how it works button
document.getElementById("how-button").addEventListener("click", () => navOpen(howWorksMessage));
document.getElementById("close-how").addEventListener("click", () => navClose(howWorksMessage));