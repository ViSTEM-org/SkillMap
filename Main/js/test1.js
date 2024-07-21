const url = "http://localhost:8000/generate_study_plan";

// Data to be sent in the POST request
const data = {
    topics: ["Flutter Fundamentals", "Flutter for app development"],
    main_topic: "Flutter for Beginners"
};

// Function to send the POST request
async function sendPostRequest() {
    try {
        // Send POST request
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        // Check if the request was successful
        if (response.ok) {
            // Parse the JSON response
            const studyPlan = await response.json();
            
            // Access the study_plan object directly
            const plan = studyPlan.study_plan;
            
            console.log("Study Plan:");
            console.log(plan);
            document.getElementById("API-info").innerHTML = plan;
        } else {
            console.error(`Error: ${response.status}`);
            console.error(await response.text());
        }
    
    } catch (error) {
        console.error(`An error occurred: ${error}`);
    }
}

// Run the function
sendPostRequest();
