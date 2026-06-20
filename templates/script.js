// frontend/script.js
const button = document.getElementById('sendBtn');
const input = document.getElementById('longUrl');

const BACKEND_URL = 'https://jubilant-umbrella-x5xq979rwq49f6rp4-5000.app.github.dev/';

button.addEventListener('click', async () => {
    console.log("Sending request to backend...");
    try {
        const response = await fetch(BACKEND_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ long_url: input.value })
        });
        const data = await response.json();
        console.log("🎉 Response received from Flask:", data);
    } catch (error) {
        console.error("❌ Connection failed:", error);
    }
});