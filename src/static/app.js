document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  let activities = [];

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      activities = await response.json();
      displayActivities();
      populateActivitySelect();
    } catch (error) {
      console.error("Error loading activities:", error);
    }
  }

  function displayActivities() {
    activitiesList.innerHTML = "";

    for (const [name, details] of Object.entries(activities)) {
      const card = document.createElement("div");
      card.className = "activity-card";

      const participantCount = details.participants.length;
      const spotsLeft = details.max_participants - participantCount;

      card.innerHTML = `
        <h4>${name}</h4>
        <p><strong>Description:</strong> ${details.description}</p>
        <p><strong>Schedule:</strong> ${details.schedule}</p>
        <p><strong>Spots Available:</strong> ${spotsLeft}/${details.max_participants}</p>
        <div class="participants-section">
          <h5>Current Participants (${participantCount}):</h5>
          <ul class="participants-list">
            ${details.participants.map((email) => `<li>${email}</li>`).join("")}
          </ul>
        </div>
      `;
      activitiesList.appendChild(card);
    }
  }

  function populateActivitySelect() {
    activitySelect.innerHTML = ""; // Clear existing options
    for (const activityName of Object.keys(activities)) {
      const option = document.createElement("option");
      option.value = activityName;
      option.textContent = activityName;
      activitySelect.appendChild(option);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );
      const data = await response.json();

      if (response.ok) {
        messageDiv.className = "message success";
        messageDiv.textContent = data.message;
        messageDiv.classList.remove("hidden");
        signupForm.reset();
        fetchActivities(); // Refresh activities list
      } else {
        messageDiv.className = "message error";
        messageDiv.textContent = data.detail;
        messageDiv.classList.remove("hidden");
      }
    } catch (error) {
      messageDiv.className = "message error";
      messageDiv.textContent = "An error occurred. Please try again.";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
