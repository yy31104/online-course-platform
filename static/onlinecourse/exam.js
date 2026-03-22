(function () {
    var examForm = document.getElementById("examForm");
    if (!examForm) {
        return;
    }

    var checkboxes = examForm.querySelectorAll(".exam-choice");
    var submitButton = document.getElementById("examSubmitButton");
    var progressText = document.getElementById("examProgressText");
    var progressBar = document.getElementById("examProgressBar");

    function updateProgress() {
        var answeredMap = {};
        var totalQuestions = 0;

        checkboxes.forEach(function (checkbox) {
            var questionId = checkbox.getAttribute("data-question-id");
            if (!(questionId in answeredMap)) {
                answeredMap[questionId] = false;
                totalQuestions += 1;
            }
            if (checkbox.checked) {
                answeredMap[questionId] = true;
            }
        });

        var answeredCount = Object.values(answeredMap).filter(Boolean).length;
        var percent = totalQuestions ? Math.round((answeredCount / totalQuestions) * 100) : 0;

        progressText.textContent = "Answered " + answeredCount + " / " + totalQuestions + " questions";
        progressBar.style.width = percent + "%";
        progressBar.textContent = percent + "%";
    }

    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener("change", updateProgress);
    });

    examForm.addEventListener("submit", function (event) {
        var hasCheckedChoice = Array.from(checkboxes).some(function (checkbox) {
            return checkbox.checked;
        });

        if (!hasCheckedChoice) {
            event.preventDefault();
            window.alert("Please select at least one choice before submitting.");
            return;
        }

        submitButton.disabled = true;
        submitButton.textContent = "Submitting...";
    });

    updateProgress();
})();
