function sendReport() {
    const lat = document.getElementById("lat").value;
    const lon = document.getElementById("lon").value;
    const condition = document.getElementById("condition").value;

    if (lat === "" || lon === "") {
        alert("Please enter latitude and longitude");
        return;
    }

    const report = {
        id: Date.now(),
        lat: parseFloat(lat),
        lon: parseFloat(lon),
        condition: condition,
        time_delay: 1
    };

    fetch("http://127.0.0.1:5000/route", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(report)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("output").textContent =
            JSON.stringify(data, null, 2);
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Could not connect to backend");
    });
}
