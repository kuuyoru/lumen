# Firebase Setup Instructions for L.U.M.E.N. AI

## 1. Create Firebase Project
1. Go to https://console.firebase.google.com/
2. Click "Create a project" (or select existing)
3. Enable Firestore Database:
   - Go to Firestore Database → Create database
   - Choose "Start in test mode" for development

## 2. Get API Credentials
1. Go to Project Settings (gear icon)
2. Scroll to "Your apps" section
3. Click "Add app" → Web app (</>) icon
4. Register app with any name
5. Copy the config values:
   - `apiKey`
   - `projectId`

## 3. Configure memory.py
Edit the Firebase configuration in `memory.py`:

```python
FIREBASE_PROJECT_ID = "your-actual-project-id"  # From Firebase console
FIREBASE_API_KEY = "your-actual-api-key"       # From Firebase console
```

## 4. Test Connection
Run the assistant and check if memory syncs to Firebase console.

## Resource Usage (Optimized)
- **RAM**: < 50MB additional
- **Storage**: < 10MB local cache
- **CPU**: Minimal (only during AI calls and sync)
- **Network**: Light HTTP requests only when needed

## Free Limits Reminder
- 1GB storage
- 50K reads/day, 20K writes/day
- 10GB egress/month

The system automatically consolidates memories to stay within limits.