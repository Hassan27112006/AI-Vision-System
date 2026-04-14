document.addEventListener('DOMContentLoaded', () => {
    const uploadInput = document.getElementById('media-upload');
    const displayImg = document.getElementById('display-image');
    const prompt = document.getElementById('upload-prompt');
    const loading = document.getElementById('loading');
    const personalityReport = document.getElementById('personality-report');

    const bars = {
        eyeDist: document.getElementById('eye-dist-bar'),
        eyeText: document.getElementById('eye-dist-text'),
        jawWidth: document.getElementById('jaw-width-bar'),
        jawText: document.getElementById('jaw-width-text'),
        noseHeight: document.getElementById('nose-height-bar'),
        noseText: document.getElementById('nose-height-text'),
        faceRatio: document.getElementById('face-ratio-bar'),
        faceText: document.getElementById('face-ratio-text'),
    };

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

            const analyzeRes = await fetch('/api/analyze/face', {
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
        if (data.num_faces === 0) {
            personalityReport.innerHTML = '<div class="text-center py-8 text-rose-500 font-bold">No faces detected in this profile.</div>';
            resetBars();
            return;
        }

        const face = data.faces[0]; // Profile first face only for simplicity
        displayImg.src = data.output_url;
        displayImg.classList.remove('hidden');
        prompt.classList.add('hidden');

        // Update Personality
        personalityReport.innerHTML = `
            <div class="space-y-4 animate-fade-in">
                <div class="flex items-center gap-4">
                    <div class="h-12 w-12 bg-rose-500 rounded-full flex items-center justify-center text-xl font-bold">MBTI</div>
                    <div>
                        <h4 class="text-lg font-bold text-rose-400 capitalize">${face.personality_type}</h4>
                        <p class="text-xs text-slate-500">Based on unique facial biometric mapping.</p>
                    </div>
                </div>
                <p class="text-sm text-slate-300 leading-relaxed italic border-l-2 border-rose-500/30 pl-4 py-2 bg-slate-800/20 rounded-r-xl">
                    "This profile demonstrates high spatial intelligence and a balanced emotional ratio."
                </p>
            </div>
        `;

        // Update Biometrics (Normalize for visualization 0-100)
        updateBar('eyeDist', face.measurements.eye_distance, 150);
        updateBar('jawWidth', face.measurements.jaw_width, 400);
        updateBar('noseHeight', face.measurements.nose_height, 300);
        updateBar('faceRatio', face.measurements.face_ratio * 100, 100);
    }

    function updateBar(key, val, max) {
        const pct = Math.min((val / max) * 100, 100);
        bars[key + 'Bar'].style.width = `${pct}%`;
        bars[key + 'Text'].innerText = `${val.toFixed(2)} ${key === 'faceRatio' ? '%' : 'px'}`;
    }

    function resetBars() {
        Object.keys(bars).forEach(k => {
            if (k.includes('Bar')) bars[k].style.width = '0%';
            if (k.includes('Text')) bars[k].innerText = '0';
        });
    }
});
