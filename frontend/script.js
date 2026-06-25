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

const BACKEND_URL = 'https://api.n06.me/api/shorten';

button.addEventListener('click', async () => {
    button.textContent = "Waking up secure server (takes up to 1 min)...";
    button.disabled = true;
    
    const maxRetries = 3;
    let attempt = 0;
    let success = false;
    let responseData = null;

    while (attempt < maxRetries && !success) {
        try {
            attempt++;
            if (attempt > 1) {
                button.textContent = `Retrying connection (Attempt ${attempt}/${maxRetries})...`;
            }

            const response = await fetch(BACKEND_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    long_url: input.value,
                    length: slider.value,
                    custom_code: customCodeInput.value
                })
            });
            
            responseData = await response.json();

            if (response.ok) {
                success = true;
                resultPanel.style.display = 'block';
                
                const productionDomain = "n06.me";
                shortLinkDisplay.textContent = `https://${responseData.short_code}.${productionDomain}`;
            } else {
                const errorMsg = responseData.message || responseData.error || "An unknown error occurred.";
                alert("Backend Error: " + errorMsg);
                success = true;
            }
        } 
        catch (error) {
            console.warn(`Connection attempt ${attempt} failed. Server might still be waking up.`, error);
            if (attempt < maxRetries) {
                await new Promise(resolve => setTimeout(resolve, 4000));
            }
        }
    }

    if (!success) {
        alert("Could not connect to backend server. The server is taking too long to wake up. Please refresh and try again in 30 seconds.");
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