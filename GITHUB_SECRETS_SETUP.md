# GitHub Secrets Setup Guide

This guide explains how to configure GitHub Secrets for the AI News Bot to work with GitHub Actions.

## Current Status

✅ **The codebase already properly uses environment variables from GitHub Secrets!**

All Python code correctly uses `os.getenv()` to read environment variables, which automatically works with GitHub Actions secrets.

## What You Need to Do

### 1. Update the Workflow File

The file `.github/workflows/daily-news.yml` needs a small update to use the correct environment variables for Resend.com instead of the old SMTP configuration.

**Replace lines 36-41:**
```yaml
          # Email configuration (optional)
          SMTP_HOST: ${{ secrets.SMTP_HOST }}
          SMTP_PORT: ${{ secrets.SMTP_PORT }}
          SMTP_USER: ${{ secrets.SMTP_USER }}
          SMTP_PASSWORD: ${{ secrets.SMTP_PASSWORD }}
          EMAIL_FROM: ${{ secrets.EMAIL_FROM }}
```

**With:**
```yaml
          # Email configuration with Resend.com (optional)
          RESEND_API_KEY: ${{ secrets.RESEND_API_KEY }}
          EMAIL_FROM: ${{ secrets.EMAIL_FROM }}
```

### 2. Configure GitHub Secrets

Go to your repository: **Settings → Secrets and variables → Actions → New repository secret**

#### Required Secrets

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key | `sk-ant-...` |
| `NOTIFICATION_METHODS` | Notification methods to use | `email,webhook` or `email` or `webhook` |

#### Email Secrets (Optional - only if using email notifications)

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `RESEND_API_KEY` | Your Resend.com API key | `re_...` |
| `EMAIL_FROM` | Sender email (must be verified in Resend) | `news@yourdomain.com` |
| `EMAIL_TO` | Recipient email address | `you@example.com` |

#### Webhook Secrets (Optional - only if using webhook notifications)

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `WEBHOOK_URL` | Your webhook endpoint URL | `https://hooks.slack.com/...` |

### 3. Verify Setup

After configuring secrets:

1. Go to **Actions** tab in your repository
2. Select **Daily AI News Digest** workflow
3. Click **Run workflow** to manually trigger a test run
4. Check the workflow logs to verify it's working correctly

## How It Works

1. **Local Development**: Uses `.env` file (copy from `.env.example`)
2. **GitHub Actions**: Uses repository secrets configured above
3. **Code**: Uses `os.getenv()` which works with both methods automatically

## Migration from SMTP

If you previously had SMTP secrets configured, you can safely delete these old secrets:
- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASSWORD`

The bot now uses Resend.com for email delivery, which is simpler and more reliable.

## Troubleshooting

**"Missing required environment variable" errors:**
- Verify the secret name matches exactly (case-sensitive)
- Ensure you added the secret to **Actions** secrets, not Environment secrets

**Email not sending:**
- Verify `RESEND_API_KEY` is correct
- Ensure `EMAIL_FROM` is verified in your Resend dashboard
- Check you haven't exceeded Resend's free tier limits

**Webhook failing:**
- Test the webhook URL manually with a POST request
- Verify the endpoint accepts JSON data
- Check the webhook service logs

## Security Notes

- Never commit actual API keys or secrets to the repository
- Always use `.env` for local development (already in `.gitignore`)
- GitHub Secrets are encrypted and only exposed during workflow runs
- Rotate API keys periodically for security
