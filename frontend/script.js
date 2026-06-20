// frontend/script.js
const button = document.getElementById('sendBtn');
const input = document.getElementById('longUrl');
const BACKEND_URL = 'https://effective-space-giggle-5gpr4xx5p7jx346q4-5000.app.github.dev/api/shorten';

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