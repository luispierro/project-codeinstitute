/* jshint esversion: 6 */
document.getElementById("upload-form").addEventListener("submit", function (event) {
    submitCSV.call(this, event); // Pass the event explicitly and bind 'this' to the form
});

document.getElementById("file-input").addEventListener("change", function () {
    const file = this.files[0];
    if (file && file.type !== "text/csv" && !file.name.endsWith(".csv")) {
        alert("Please upload a valid CSV file.");
        this.value = ""; // Clear the input
    }
});

function submitCSV(event){
    event.preventDefault(); // Prevent the default form submission

    const formData = new FormData(this);
    const spinner = document.getElementById("spinner");
    const insightsContainer = document.querySelector(".insights");

    // Show the spinner
    spinner.style.display = "block";
    insightsContainer.style.display = "none"; // Hide the insights temporarily

    // Send the form data to the server
    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Error processing data");
        }
        return response.text();
    })
    .then(data => {
        // Replace the insights section with the server response
        insightsContainer.innerHTML = data;
    })
    .catch(error => {
        console.error("Error:", error);
        alert("There was an error processing your data.");
    })
    .finally(() => {
        // Hide the spinner
        spinner.style.display = "none";
        insightsContainer.style.display = "block";
    });
}