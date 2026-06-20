// frontend/script.js
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

const BACKEND_URL = 'https://effective-space-giggle-5gpr4xx5p7jx346q4-5000.app.github.dev/api/shorten';

button.addEventListener('click', async () => {
    button.textContent = "Generating...";
    button.disabled = true;
    
    try {
        const response = await fetch(BACKEND_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                long_url: input.value,
                length: slider.value
            })
        });
        
        const data = await response.json();

        if (response.ok) {
            resultPanel.style.display = 'block';
            
            const baseAddress = BACKEND_URL.replace('/api/shorten', ''); 
            shortLinkDisplay.textContent = `${baseAddress}/${data.short_code}`;
        }
        else {
            alert("Backend Error: " + data.error);
        }
    } 
    catch (error) {
        console.error("Connection failed:", error);
        alert("Could not connect to backend server.");
    }
    finally {
        button.textContent = "Generate Short Link";
        button.disabled = false;
    }
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