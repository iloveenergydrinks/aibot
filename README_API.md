# Bot Stats API

## 🌐 **API Endpoints**

Your bot exposes a simple REST API to track stats in real-time.

---

### **Start the API Server:**

```bash
# Terminal 1: Run the bot
python3 twitter_autonomous.py

# Terminal 2: Run the API
python3 bot_api.py
```

The API runs on: `http://localhost:5000`

---

### **Endpoints:**

#### **1. GET /api/status** - Quick Status

**Response:**
```json
{
  "status": "online",
  "space_link": "https://twitter.com/i/spaces/...",
  "uptime_hours": 2.5,
  "uptime_seconds": 9000,
  "argument_count": 47,
  "last_response": "Nein! Democracy is...",
  "last_updated": "2025-10-30T23:45:00"
}
```

#### **2. GET /api/stats** - Detailed Stats

**Response:**
```json
{
  "status": "online",
  "space_link": "https://twitter.com/i/spaces/...",
  "start_time": "2025-10-30T21:15:00",
  "uptime_hours": 2.5,
  "total_arguments": 47,
  "arguments_per_hour": 18.8,
  "last_response": "Nein! Democracy is...",
  "character": "Adolf Hitler",
  "timestamp": "2025-10-30T23:45:00"
}
```

#### **3. GET /api/health** - Health Check

**Response:**
```json
{
  "status": "ok"
}
```

---

## 🔗 **Use from Your Website:**

### **JavaScript Example:**

```javascript
// Fetch bot status
fetch('http://your-server:5000/api/status')
  .then(r => r.json())
  .then(data => {
    console.log('Bot status:', data.status);
    console.log('Arguments:', data.argument_count);
    console.log('Uptime:', data.uptime_hours, 'hours');
  });
```

### **Display on Website:**

```html
<div class="bot-stats">
  <h3>🔴 Hitler Bot LIVE</h3>
  <p>Space: <a href="{space_link}">{space_link}</a></p>
  <p>Live for: {uptime_hours} hours</p>
  <p>Arguments delivered: {argument_count}</p>
  <p>Last said: "{last_response}"</p>
</div>
```

---

## 🚀 **Deploy API Publicly:**

### **Option 1: Expose Port (Development)**

```bash
# Run API on public port
python3 bot_api.py
```

Access from anywhere: `http://YOUR_MAC_IP:5000/api/status`

### **Option 2: Deploy to Cloud**

**Upload bot_api.py to:**
- Railway.app (free tier)
- Vercel (serverless)
- Heroku (free tier)

Then your website calls: `https://your-api.railway.app/api/status`

---

## 📊 **What Gets Tracked:**

Bot automatically updates:
- ✅ When it starts (status: "online")
- ✅ After each argument (increment count)
- ✅ Last response text
- ✅ When it stops (status: "offline")

The stats are stored in `bot_stats.json` and exposed via API!

---

## 🎯 **Usage:**

**Run both:**
```bash
# Terminal 1
python3 twitter_autonomous.py

# Terminal 2  
python3 bot_api.py
```

**Then call from your website:**
```bash
curl http://localhost:5000/api/status
```

Perfect for dashboards, status pages, monitoring! 📈

