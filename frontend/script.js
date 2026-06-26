(function wakeUpBackend() {
    const BACKEND_PING_URL = 'https://api.n06.me/api/redirect/ping';
    console.log("Initializing silent background wake-up call to Render...");
    fetch(BACKEND_PING_URL).catch(() => {
    });
})();

const customCodeInput = document.getElementById('customCode');
const button = document.getElementById('sendBtn');
const input = document.getElementById('longUrl');
const slider = document.getElementById('lengthSlider');
const lengthVal = document.getElementById('lengthVal');
const resultPanel = document.getElementById('resultPanel');
const shortLinkDisplay = document.getElementById('shortLinkDisplay');
const copyBtn = document.getElementById('copyBtn');

slider.addEventListener('input', () => {
    lengthVal.textContent = slider.value;
});

const BACKEND_URL = 'https://secure-url-shortener-b6nj.onrender.com/api/shorten';

button.addEventListener('click', async () => {
    button.textContent = "Generating...";
    button.disabled = true;
    const sanitizedCustomCode = customCodeInput.value 
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9-_]/g, '-') 
    .replace(/-+/g, '-');
    
    const maxRetries = 3;
    let attempt = 0;
    let success = false;

    while (attempt < maxRetries && !success) {
        try {
            attempt++;
            const response = await fetch(BACKEND_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    long_url: input.value,
                    length: slider.value,
                    custom_code: sanitizedCustomCode
                })
            });
            
            const responseData = await response.json();

            if (response.ok) {
                success = true;
                resultPanel.style.display = 'block';
                shortLinkDisplay.textContent = `https://${responseData.short_code}.n06.me`;
            } else {
                const errorMsg = responseData.message || responseData.error || "The server rejected the request.";
                alert("Backend Error: " + errorMsg);
                success = true; 
            }
        } 
        catch (error) {
            console.warn(`Attempt ${attempt} failed.`);
            if (attempt < maxRetries) {
                await new Promise(resolve => setTimeout(resolve, 3000)); // Quietly wait 3 seconds
            }
        }
    }

    if (!success) {
        alert("Server connection timeout. Please try again in a few moments.");
    }

    button.textContent = "Generate Short Link";
    button.disabled = false;
});

copyBtn.addEventListener('click', () => {
    navigator.clipboard.writeText(shortLinkDisplay.textContent);
    
    const originalText = copyBtn.textContent;
    copyBtn.textContent = "Copied! ✅";
    copyBtn.style.backgroundColor = "#1e7e34";
    
    setTimeout(() => {
        copyBtn.textContent = originalText;
        copyBtn.style.backgroundColor = "#28a745";
    }, 2000);
});