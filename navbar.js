document.addEventListener("DOMContentLoaded", function() {
    var selectElement = document.getElementById("project-select");
    selectElement.addEventListener("change", function() {
        var selectedValue = selectElement.value;
        if (selectedValue === "uni-projects") {
            window.location.href = "https://diegobarmor.github.io/";
        } else if (selectedValue === "personal-projects") {
            window.location.href = "https://diegobarmor.github.io/";
        }
    });
});
