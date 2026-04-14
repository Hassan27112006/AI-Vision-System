document.addEventListener('DOMContentLoaded', () => {
    const uploadInput = document.getElementById('media-upload');
    const displayImg = document.getElementById('display-image');
    const prompt = document.getElementById('upload-prompt');
    const loading = document.getElementById('loading');
    const totalCount = document.getElementById('total-count');
    const logContainer = document.getElementById('log-container');
    const breakdownContainer = document.getElementById('breakdown-container');

    uploadInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        loading.classList.remove('hidden');

        const formData = new FormData();
        formData.append('file', file);

        try {
            const uploadRes = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
            const uploadData = await uploadRes.json();

            const analyzeRes = await fetch('/api/analyze/object', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ filename: uploadData.filename })
            });
            const result = await analyzeRes.json();

            updateUI(result);

        } catch (error) {
            console.error(error);
        } finally {
            loading.classList.add('hidden');
        }
    });

    function updateUI(data) {
        displayImg.src = data.output_url;
        displayImg.classList.remove('hidden');
        prompt.classList.add('hidden');

        totalCount.innerText = data.total_count;

        // Breakdown UI
        breakdownContainer.innerHTML = '';
        Object.keys(data.breakdown).forEach(label => {
            const div = document.createElement('div');
            div.className = 'flex flex-col items-center bg-slate-800/50 p-4 rounded-2xl min-w-[100px] border border-cyan-500/20';
            div.innerHTML = `
                <span class="text-[10px] text-slate-500 uppercase font-bold mb-1">${label}</span>
                <span class="text-xl font-bold text-cyan-400">${data.breakdown[label]}</span>
            `;
            breakdownContainer.appendChild(div);
        });

        // Logs
        data.logs.forEach(log => addLog(log));
    }

    function addLog(msg) {
        const p = document.createElement('p');
        p.innerText = `[${new Date().toLocaleTimeString()}] ${msg}`;
        logContainer.prepend(p);
    }
});
