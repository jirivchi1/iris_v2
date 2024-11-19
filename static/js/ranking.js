// Display responses for selected question
function displayResponses(questionId) {
    const container = document.getElementById("responseCards");
    container.innerHTML = ""; // Clear previous results

    // Filter responses for the selected question
    const filteredData = data.filter(item => item.question_id === questionId);

    if (filteredData.length === 0) {
        container.innerHTML = "<p class='text-center'>No responses found for this question.</p>";
        return;
    }

    // Sort the data temporarily for ranking display (future ranking logic can replace this)
    const sortedData = filteredData.slice(0, 3);

    // Create a card for each response
    sortedData.forEach((entry, index) => {
        const card = document.createElement("div");
        card.className = "card col-md-4 mx-2 position-relative";

        // Add ranking number for the first three cards
        const rankingNumber = index < 3 ? `<div class="ranking-number">${index + 1}</div>` : "";

        card.innerHTML = `
            ${rankingNumber}
            <div class="card-body">
                <h5 class="card-title">User: ${entry.user_name}</h5>
                <p class="card-text"><strong>Prompt:</strong> ${entry.prompt}</p>
                <p class="card-text"><strong>AI Response:</strong> ${entry.ai_response}</p>
            </div>
        `;

        container.appendChild(card);
    });
}
