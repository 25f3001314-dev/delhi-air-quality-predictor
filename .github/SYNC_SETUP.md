# 🔄 GitHub to Hugging Face Auto-Sync Setup

This repository is configured to automatically sync to Hugging Face Space: https://huggingface.co/spaces/25f3001314/Bachao

## Setup Instructions

### 1. Add Hugging Face Token to GitHub Secrets

**Already Done ✅** - But if you need to update it:

1. Go to repository Settings → Secrets and variables → Actions
2. Add a new secret:
   - Name: `HF_TOKEN`
   - Value: Your Hugging Face write token from https://huggingface.co/settings/tokens

### 2. How It Works

- Every push to the `main` branch triggers the workflow
- The workflow automatically pushes all changes to Hugging Face Space
- Your Space rebuilds and deploys automatically

### 3. Manual Trigger

You can also manually trigger the sync:
- Go to Actions tab
- Select "Sync to Hugging Face Space" workflow
- Click "Run workflow"

### 4. Viewing Your Deployed App

Once synced, your app will be live at:
**https://huggingface.co/spaces/25f3001314/Bachao**

## Troubleshooting

- **Sync fails?** Check that `HF_TOKEN` secret is set correctly
- **App not building?** Check Space logs at https://huggingface.co/spaces/25f3001314/Bachao/logs
- **Need to update token?** Generate new token at https://huggingface.co/settings/tokens
