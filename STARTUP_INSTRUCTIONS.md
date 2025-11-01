# SubTrack Application - Startup Instructions

## Overview
SubTrack is a subscription management application with a Python FastAPI backend and React Native Expo frontend.

## Prerequisites

### Backend Requirements
- Python 3.9 or higher
- pip (Python package manager)

### Frontend Requirements
- Node.js 18 or higher
- npm or yarn
- Expo Go app on your iPhone (download from App Store)

## Environment Setup

### 1. Configure Environment Variables

Edit `/backend/.env` file with your credentials:

```
SECRET_JWT_KEY=your-secret-jwt-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

TINK_CLIENT_ID=your_tink_client_id
TINK_CLIENT_SECRET=your_tink_client_secret
TINK_REDIRECT_URI=http://localhost:8080/callback

OPENAI_API_KEY=your_openai_api_key
```

**Note:** You need to obtain:
- A strong secret key for JWT (generate using `openssl rand -hex 32`)
- Tink API credentials from https://tink.com (for bank integrations)
- OpenAI API key from https://platform.openai.com (for AI-powered subscription detection)

## Starting the Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start the FastAPI server:
```bash
python app.py
```

The backend will start on `http://0.0.0.0:8080`

**Important:** The backend will automatically create a SQLite database file (`subtrack.db`) on first run.

## Starting the Frontend

1. Navigate to the SubTrackDK directory:
```bash
cd SubTrackDK
```

2. Install Node dependencies:
```bash
npm install
```

3. Start the Expo development server:
```bash
npm start
```

The Expo server will start on `http://localhost:8080`

## Testing on iPhone with Expo Go

### Option 1: QR Code (Easiest)

1. Make sure your iPhone and computer are on the same WiFi network
2. Download the Expo Go app from the App Store on your iPhone
3. After running `npm start`, a QR code will appear in the terminal
4. Open the Camera app on your iPhone and scan the QR code
5. The app will open in Expo Go

### Option 2: Manual URL Entry

1. After running `npm start`, note the URL shown (e.g., `exp://192.168.x.x:8080`)
2. Open Expo Go on your iPhone
3. Tap "Enter URL manually"
4. Enter the URL and tap "Connect"

## Important Notes

### Backend IP Address Configuration

The frontend needs to know your backend's IP address. If you're testing on a physical device (iPhone), you need to update the backend URL in the frontend code:

Edit `SubTrackDK/services/api.js`:
```javascript
const BACKEND_BASE_URL = 'http://YOUR_LOCAL_IP:8080/api';
```

Replace `YOUR_LOCAL_IP` with your computer's local network IP address (e.g., `192.168.1.100`).

To find your local IP:
- **macOS/Linux:** Run `ifconfig` and look for `inet` under your WiFi adapter
- **Windows:** Run `ipconfig` and look for `IPv4 Address`

### Database Storage

The application uses SQLite for data storage:
- Database file: `backend/subtrack.db`
- Automatically created on first run
- Contains users and subscriptions tables

### Troubleshooting

**Backend won't start:**
- Verify Python version: `python --version` (should be 3.9+)
- Check if port 8080 is already in use
- Ensure all dependencies are installed

**Frontend won't connect:**
- Verify both devices are on the same WiFi network
- Check firewall settings (allow port 8080)
- Update backend URL in `api.js` with correct IP

**Expo Go won't load:**
- Clear Expo Go cache in the app settings
- Restart the Expo development server
- Check that your iPhone and computer can ping each other

## Features

The application supports:
- User authentication (signup/login)
- Manual subscription management
- Bank integration via Tink for automatic detection
- PDF bank statement upload with AI analysis
- Subscription categorization and tracking
- Renewal date reminders
- Spending analytics

## Development Tips

- Keep both backend and frontend running simultaneously
- Changes to Python code require backend restart
- React Native changes will hot-reload automatically
- Check both backend and Expo terminal for errors
- Use `console.log` statements for debugging frontend issues
