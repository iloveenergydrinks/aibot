/**
 * Lord Fishnu Sermon Manager - Client-side JavaScript
 */

// Socket.IO connection
const socket = io();

// State
let currentStatus = null;
let selectedTheme = null;

// ============================================================================
// SOCKET HANDLERS
// ============================================================================

socket.on('connect', () => {
    console.log('🌐 Connected to sermon server');
    updateConnectionStatus(true);
    loadInitialData();
});

socket.on('disconnect', () => {
    console.log('❌ Disconnected from sermon server');
    updateConnectionStatus(false);
});

socket.on('status_update', (status) => {
    updateStatus(status);
});

socket.on('sermon_started', (status) => {
    addLog('🙏 Sermon started!', 'success');
    updateStatus(status);
});

socket.on('sermon_stopped', () => {
    addLog('🛑 Sermon stopped', 'warning');
    resetStatus();
});

socket.on('segment_changed', (status) => {
    addLog(`📿 Segment: ${status.segment_name}`, 'info');
    updateStatus(status);
});

socket.on('sermon_paused', (status) => {
    addLog('⏸️ Sermon paused', 'warning');
    updateStatus(status);
});

socket.on('sermon_resumed', (status) => {
    addLog('▶️ Sermon resumed', 'success');
    updateStatus(status);
});

// ============================================================================
// UI UPDATES
// ============================================================================

function updateConnectionStatus(connected) {
    const dot = document.getElementById('statusDot');
    const text = document.getElementById('statusText');
    
    if (connected) {
        dot.className = 'w-3 h-3 rounded-full bg-green-500 live-indicator';
        text.textContent = 'Connected';
    } else {
        dot.className = 'w-3 h-3 rounded-full bg-red-500';
        text.textContent = 'Disconnected';
    }
}

function updateStatus(status) {
    currentStatus = status;
    
    // Update main status display
    document.getElementById('currentSegment').textContent = status.segment_name || 'Idle';
    document.getElementById('progress').textContent = `${status.segment_index || 0}/${status.total_segments || 9}`;
    document.getElementById('elapsed').textContent = formatTime(status.sermon_elapsed_seconds || 0);
    
    // Update theme
    const theme = status.daily_theme;
    if (theme) {
        document.getElementById('currentTheme').textContent = theme.theme || 'None';
    }
    
    // Update progress bar
    const progressPercent = status.total_segments ? 
        (status.segment_index / status.total_segments) * 100 : 0;
    document.getElementById('progressBar').style.width = `${progressPercent}%`;
    
    // Update button states
    updateButtons(status.active, status.paused);
    
    // Update segments grid
    updateSegmentsGrid(status);
}

function resetStatus() {
    currentStatus = null;
    document.getElementById('currentSegment').textContent = 'Idle';
    document.getElementById('progress').textContent = '0/9';
    document.getElementById('elapsed').textContent = '00:00';
    document.getElementById('currentTheme').textContent = 'None';
    document.getElementById('progressBar').style.width = '0%';
    updateButtons(false, false);
    loadSegments(); // Reset segments grid
}

function updateButtons(active, paused) {
    const btnStart = document.getElementById('btnStart');
    const btnAdvance = document.getElementById('btnAdvance');
    const btnPause = document.getElementById('btnPause');
    const btnStop = document.getElementById('btnStop');
    
    btnStart.disabled = active;
    btnAdvance.disabled = !active || paused;
    btnPause.disabled = !active || paused;
    btnStop.disabled = !active;
    
    // Update pause button text
    if (paused) {
        btnPause.innerHTML = '<span>▶</span> Resume';
        btnPause.disabled = false;
        btnPause.onclick = resumeSermon;
    } else {
        btnPause.innerHTML = '<span>⏸</span> Pause';
        btnPause.onclick = pauseSermon;
    }
}

function updateSegmentsGrid(status) {
    const grid = document.getElementById('segmentsGrid');
    const currentIndex = status.segment_index || 0;
    
    // Get segments from existing grid items
    const items = grid.querySelectorAll('.segment-item');
    items.forEach((item, index) => {
        const badge = item.querySelector('.segment-badge');
        badge.classList.remove('completed', 'current', 'pending');
        
        if (index + 1 < currentIndex) {
            badge.classList.add('completed');
            badge.querySelector('.status-icon').textContent = '✓';
        } else if (index + 1 === currentIndex) {
            badge.classList.add('current');
            badge.querySelector('.status-icon').textContent = '►';
        } else {
            badge.classList.add('pending');
            badge.querySelector('.status-icon').textContent = (index + 1).toString();
        }
    });
}

function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

function addLog(message, type = 'info') {
    const container = document.getElementById('logContainer');
    const timestamp = new Date().toLocaleTimeString();
    
    const colors = {
        info: 'text-blue-400',
        success: 'text-green-400',
        warning: 'text-yellow-400',
        error: 'text-red-400'
    };
    
    const p = document.createElement('p');
    p.className = colors[type] || 'text-gray-400';
    p.innerHTML = `<span class="text-gray-500">[${timestamp}]</span> ${message}`;
    
    // Remove "waiting" message if present
    const waiting = container.querySelector('.text-gray-500');
    if (waiting && waiting.textContent.includes('Waiting')) {
        waiting.remove();
    }
    
    container.appendChild(p);
    container.scrollTop = container.scrollHeight;
}

// ============================================================================
// SERMON CONTROLS
// ============================================================================

async function startSermon() {
    try {
        const response = await fetch('/api/sermon/start');
        const data = await response.json();
        if (!data.success && !data.error) addLog(`Failed to start`, 'error');
    } catch (error) {
        addLog(`Error: ${error.message}`, 'error');
    }
}

async function stopSermon() {
    try {
        const response = await fetch('/api/sermon/stop');
        const data = await response.json();
        if (!data.success && !data.error) addLog(`Failed to stop`, 'error');
    } catch (error) {
        addLog(`Error: ${error.message}`, 'error');
    }
}

async function pauseSermon() {
    try {
        const response = await fetch('/api/sermon/pause');
        const data = await response.json();
        if (!data.success) addLog(`Failed to pause`, 'error');
    } catch (error) {
        addLog(`Error: ${error.message}`, 'error');
    }
}

async function resumeSermon() {
    try {
        const response = await fetch('/api/sermon/resume');
        const data = await response.json();
        if (!data.success) addLog(`Failed to resume`, 'error');
    } catch (error) {
        addLog(`Error: ${error.message}`, 'error');
    }
}

async function advanceSermon() {
    try {
        const response = await fetch('/api/sermon/advance');
        const data = await response.json();
        if (!data.success) addLog(`Failed to advance`, 'error');
    } catch (error) {
        addLog(`Error: ${error.message}`, 'error');
    }
}

async function skipToSegment(segmentId) {
    try {
        const response = await fetch(`/api/sermon/skip/${segmentId}`);
        const data = await response.json();
        if (data.success) {
            addLog(`Skipped to ${segmentId}`, 'info');
        } else {
            addLog(`Failed to skip`, 'error');
        }
    } catch (error) {
        addLog(`Error: ${error.message}`, 'error');
    }
}

// ============================================================================
// DATA LOADING
// ============================================================================

async function loadInitialData() {
    await Promise.all([
        loadSegments(),
        loadThemes(),
        loadAudioStatus()
    ]);
    addLog('Dashboard loaded', 'success');
}

async function loadSegments() {
    try {
        const response = await fetch('/api/segments');
        const data = await response.json();
        
        const grid = document.getElementById('segmentsGrid');
        grid.innerHTML = '';
        
        data.segments.forEach((segment, index) => {
            const div = document.createElement('div');
            div.className = 'segment-item';
            div.innerHTML = `
                <div class="segment-badge pending rounded-lg p-3 cursor-pointer hover:opacity-80 transition"
                     onclick="skipToSegment('${segment.id}')">
                    <div class="flex items-center gap-3">
                        <span class="status-icon w-6 h-6 flex items-center justify-center rounded-full bg-black/30 text-sm">
                            ${index + 1}
                        </span>
                        <div class="flex-1 min-w-0">
                            <p class="font-medium truncate">${segment.name}</p>
                            <p class="text-xs text-gray-400">${segment.duration_minutes} min • ${segment.type}</p>
                        </div>
                    </div>
                </div>
            `;
            grid.appendChild(div);
        });
    } catch (error) {
        console.error('Failed to load segments:', error);
    }
}

async function loadThemes() {
    try {
        const response = await fetch('/api/themes');
        const data = await response.json();
        
        const list = document.getElementById('themesList');
        list.innerHTML = '';
        
        data.themes.forEach((theme, index) => {
            const div = document.createElement('div');
            const isDaily = data.daily_theme && data.daily_theme.number === theme.number;
            div.className = `p-3 rounded-lg cursor-pointer transition ${
                isDaily ? 'bg-yellow-600/20 border border-yellow-600/40' : 'bg-black/30 hover:bg-black/50'
            }`;
            div.onclick = () => selectTheme(theme.number);
            div.innerHTML = `
                <div class="flex items-start gap-2">
                    <span class="text-yellow-500 font-bold">${theme.number}.</span>
                    <div>
                        <p class="text-sm font-medium">${theme.commandment}</p>
                        <p class="text-xs text-gray-500 mt-1">${theme.theme}</p>
                        ${isDaily ? '<span class="text-xs text-yellow-500">📅 Today\'s Theme</span>' : ''}
                    </div>
                </div>
            `;
            list.appendChild(div);
        });
    } catch (error) {
        console.error('Failed to load themes:', error);
    }
}

function selectTheme(number) {
    selectedTheme = selectedTheme === number ? null : number;
    
    // Update UI
    const items = document.getElementById('themesList').children;
    Array.from(items).forEach((item, index) => {
        if (index + 1 === selectedTheme) {
            item.classList.add('ring-2', 'ring-yellow-500');
        } else {
            item.classList.remove('ring-2', 'ring-yellow-500');
        }
    });
    
    if (selectedTheme) {
        addLog(`Selected theme #${selectedTheme} for next sermon`, 'info');
    }
}

async function loadAudioStatus() {
    try {
        const response = await fetch('/api/audio');
        const data = await response.json();
        
        const list = document.getElementById('audioList');
        list.innerHTML = '';
        
        const audioLabels = {
            'intro_song': 'Intro Song',
            'flute_titanic': 'Flute Titanic',
            'outro_song': 'Outro Song'
        };
        
        for (const [key, info] of Object.entries(data.audio_files)) {
            const div = document.createElement('div');
            div.className = 'flex items-center justify-between p-3 rounded-lg bg-black/30';
            div.innerHTML = `
                <div class="flex items-center gap-2">
                    <span class="${info.exists ? 'text-green-500' : 'text-red-500'}">${info.exists ? '✅' : '❌'}</span>
                    <div>
                        <p class="font-medium">${audioLabels[key] || key}</p>
                        <p class="text-xs text-gray-500">${info.exists ? `${info.size_mb} MB` : 'Not uploaded'}</p>
                    </div>
                </div>
                <div class="flex gap-2">
                    ${info.exists ? `
                        <button onclick="playAudio('${key}')" class="px-3 py-1 text-sm bg-gray-700 hover:bg-gray-600 rounded transition">
                            ▶ Play
                        </button>
                    ` : ''}
                    <label class="px-3 py-1 text-sm bg-yellow-600 hover:bg-yellow-700 rounded cursor-pointer transition">
                        📁 Upload
                        <input type="file" accept="audio/*" class="hidden" onchange="uploadAudio('${key}', this.files[0])">
                    </label>
                </div>
            `;
            list.appendChild(div);
        }
    } catch (error) {
        console.error('Failed to load audio status:', error);
    }
}

async function uploadAudio(key, file) {
    if (!file) return;
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        addLog(`Uploading ${key}...`, 'info');
        const response = await fetch(`/api/audio/upload/${key}`, {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        
        if (data.success) {
            addLog(`Uploaded ${key} successfully!`, 'success');
            loadAudioStatus();
        } else {
            addLog(`Upload failed: ${data.error}`, 'error');
        }
    } catch (error) {
        addLog(`Upload error: ${error.message}`, 'error');
    }
}

function playAudio(key) {
    const audio = new Audio(`/api/audio/preview/${key}`);
    audio.play();
    addLog(`Playing ${key}...`, 'info');
}

// ============================================================================
// CONTENT PREVIEW
// ============================================================================

async function previewScroll() {
    try {
        const scrollNum = (new Date().getDay() % 10) + 1;
        const response = await fetch(`/api/content/scroll/${scrollNum}`);
        const data = await response.json();
        
        showPreview(`📖 Scroll #${data.scroll_number}: ${data.title}`, data.content);
    } catch (error) {
        addLog(`Preview error: ${error.message}`, 'error');
    }
}

async function previewCannon() {
    try {
        const response = await fetch('/api/content/cannon');
        const data = await response.json();
        
        showPreview(
            `📚 ${data.book} - ${data.chapter}`,
            `<p class="text-sm text-gray-400 mb-4">by ${data.author}</p>${data.content}`
        );
    } catch (error) {
        addLog(`Preview error: ${error.message}`, 'error');
    }
}

async function previewBrothtism() {
    try {
        const response = await fetch('/api/content/brothtism');
        const data = await response.json();
        
        showPreview('🙏 The Brothtism', `<pre class="whitespace-pre-wrap">${data.text}</pre>`);
    } catch (error) {
        addLog(`Preview error: ${error.message}`, 'error');
    }
}

function showPreview(title, content) {
    document.getElementById('previewTitle').textContent = title;
    document.getElementById('previewContent').innerHTML = `<div class="text-gray-300 leading-relaxed">${content}</div>`;
    document.getElementById('previewModal').classList.remove('hidden');
}

function closePreview() {
    document.getElementById('previewModal').classList.add('hidden');
}

// Close modal on escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closePreview();
});

// Close modal on background click
document.getElementById('previewModal').addEventListener('click', (e) => {
    if (e.target.id === 'previewModal') closePreview();
});

