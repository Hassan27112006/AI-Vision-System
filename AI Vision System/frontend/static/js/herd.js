document.addEventListener('DOMContentLoaded', () => {
    const uploadInput = document.getElementById('media-upload');
    const displayImg = document.getElementById('display-image');
    const prompt = document.getElementById('upload-prompt');
    const loading = document.getElementById('loading');
    const herdCount = document.getElementById('herd-count');
    const herdStatus = document.getElementById('herd-status');
    const logContainer = document.getElementById('log-container');
    const confidenceBar = document.getElementById('confidence-bar');
    const confidenceText = document.getElementById('confidence-text');

    uploadInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        // Show loading
        loading.classList.remove('hidden');

        // 1. Upload
        const formData = new FormData();
        formData.append('file', file);

        try {
            const uploadRes = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
            const uploadData = await uploadRes.json();

            // 2. Analyze
            const analyzeRes = await fetch('/api/analyze/herd', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ filename: uploadData.filename })
            });
            const result = await analyzeRes.json();

            // 3. Update UI
            updateUI(result);

        } catch (error) {
            console.error(error);
            addLog('[ERROR] ' + error.message);
        } finally {
            loading.classList.add('hidden');
        }
    });

    function updateUI(data) {
        // Display result image
        displayImg.src = data.output_url;
        displayImg.classList.remove('hidden');
        prompt.classList.add('hidden');

        // Update counts
        herdCount.innerText = data.count;
        herdStatus.innerText = data.is_herd ? 'HERD DETECTED! ALERT SENT.' : 'Individual animals detected.';
        herdStatus.className = data.is_herd ? 'text-sm mt-4 text-amber-500 font-bold animate-pulse' : 'text-sm mt-4 text-slate-500';

        // Update confidence (mock avg)
        const avgConf = data.detections.length > 0
            ? (data.detections.reduce((a, b) => a + b.confidence, 0) / data.detections.length) * 100
            : 0;
        confidenceBar.style.width = `${avgConf}%`;
        confidenceText.innerText = `Confidence: ${avgConf.toFixed(2)}%`;

        // Update map
        if (window.updateMapAlerts && data.alerts) {
            window.updateMapAlerts(data.alerts);
        }

        // Add logs
        data.logs.forEach(log => addLog(`[AI] ${log}`));
    }

    function addLog(msg) {
        const p = document.createElement('p');
        p.innerText = `[${new Date().toLocaleTimeString()}] ${msg}`;
        logContainer.prepend(p);
    }
});
