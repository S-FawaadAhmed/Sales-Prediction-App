const API_BASE_URL = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", () => {
    checkBackendHealth();

    document.getElementById("regression-form").addEventListener("submit", handleRegressionSubmit);
    document.getElementById("classification-form").addEventListener("submit", handleClassificationSubmit);

    document.getElementById("reg-reset").addEventListener("click", () => {
        document.getElementById("regression-form").reset();
        document.getElementById("reg-result").classList.add("hidden");
    });

    document.getElementById("clf-reset").addEventListener("click", () => {
        document.getElementById("classification-form").reset();
        document.getElementById("clf-result").classList.add("hidden");
    });
});

async function checkBackendHealth() {
    const badge = document.getElementById("api-status-badge");
    try {
        const res = await fetch(`${API_BASE_URL}/health`);
        const data = await res.json();
        if (data.status === "healthy") {
            badge.className = "badge badge-online";
            badge.innerText = "Backend Connected & Models Loaded";
        } else {
            badge.className = "badge badge-loading";
            badge.innerText = "Backend Degraded";
        }
    } catch (err) {
        badge.className = "badge badge-offline";
        badge.innerText = "Backend Offline";
    }
}

async function handleRegressionSubmit(e) {
    e.preventDefault();
    const payload = {
        Quantity: parseInt(document.getElementById("reg-quantity").value),
        Unit_Price_INR: parseFloat(document.getElementById("reg-price").value),
        Discount: parseFloat(document.getElementById("reg-discount").value),
        Category: document.getElementById("reg-category").value,
        Subcategory: document.getElementById("reg-subcategory").value,
        Region: document.getElementById("reg-region").value,
        Segment: document.getElementById("reg-segment").value,
        Channel: document.getElementById("reg-channel").value,
        Payment_Method: document.getElementById("reg-payment").value,
        Order_Month: parseInt(document.getElementById("reg-month").value),
        Order_DayOfWeek: parseInt(document.getElementById("reg-day").value)
    };

    try {
        const res = await fetch(`${API_BASE_URL}/predict/regression`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (res.ok) {
            document.getElementById("reg-output").innerText = `₹ ${data.predicted_profit_inr.toLocaleString("en-IN")}`;
            document.getElementById("reg-result").classList.remove("hidden");
        } else {
            alert(`API Error: ${data.detail}`);
        }
    } catch (err) {
        alert("Failed to connect to regression endpoint.");
    }
}

async function handleClassificationSubmit(e) {
    e.preventDefault();
    const payload = {
        Quantity: parseInt(document.getElementById("clf-quantity").value),
        Unit_Price_INR: parseFloat(document.getElementById("clf-price").value),
        Discount: parseFloat(document.getElementById("clf-discount").value),
        Category: document.getElementById("clf-category").value,
        Subcategory: document.getElementById("clf-subcategory").value,
        Region: document.getElementById("clf-region").value,
        Segment: document.getElementById("clf-segment").value,
        Channel: document.getElementById("clf-channel").value,
        Payment_Method: document.getElementById("clf-payment").value,
        Order_Month: parseInt(document.getElementById("clf-month").value),
        Order_DayOfWeek: parseInt(document.getElementById("clf-day").value)
    };

    try {
        const res = await fetch(`${API_BASE_URL}/predict/classification`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (res.ok) {
            const outputDiv = document.getElementById("clf-output");
            outputDiv.innerText = data.predicted_returned === "Yes" ? "RETURN RISK: HIGH" : "RETURN RISK: LOW";
            outputDiv.style.color = data.predicted_returned === "Yes" ? "#dc2626" : "#16a34a";
            
            document.getElementById("clf-prob").innerText = `Estimated Return Probability: ${(data.return_probability * 100).toFixed(1)}%`;
            document.getElementById("clf-result").classList.remove("hidden");
        } else {
            alert(`API Error: ${data.detail}`);
        }
    } catch (err) {
        alert("Failed to connect to classification endpoint.");
    }
}