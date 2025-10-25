# AI News Bot

An automated system that generates and distributes daily AI news digests using Anthropic's Claude API.

## Features

- **AI-Powered News Generation**: Uses Anthropic's Claude API to generate comprehensive AI news digests
- **Multiple Notification Channels**: Supports email and webhook notifications
- **Flexible Configuration**: Easy-to-customize topics and notification settings via YAML config
- **Automated Scheduling**: GitHub Actions workflow for daily automated execution
- **Robust Error Handling**: Comprehensive logging and retry logic
- **Professional Email Templates**: HTML-formatted emails with clean design

## Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd ai-news-bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your actual values:

```env
# Required: Anthropic API Key
ANTHROPIC_API_KEY=your_api_key_here

# Optional: Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAIL_FROM=your_email@gmail.com
EMAIL_TO=recipient@example.com

# Optional: Webhook Configuration
WEBHOOK_URL=https://your-webhook-url.com/endpoint

# Notification Methods (comma-separated)
NOTIFICATION_METHODS=email,webhook
```

### 4. Customize News Topics (Optional)

Edit `config.yaml` to customize the news topics and prompt template:

```yaml
news:
  topics:
    - "Your custom topic 1"
    - "Your custom topic 2"
```

### 5. Run Locally

```bash
python main.py
```

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Your Anthropic API key |
| `NOTIFICATION_METHODS` | Yes | Comma-separated list: `email,webhook` |
| `SMTP_HOST` | For email | SMTP server host |
| `SMTP_PORT` | For email | SMTP server port |
| `SMTP_USER` | For email | SMTP username |
| `SMTP_PASSWORD` | For email | SMTP password |
| `EMAIL_FROM` | For email | Sender email address |
| `EMAIL_TO` | For email | Recipient email address |
| `WEBHOOK_URL` | For webhook | Webhook endpoint URL |

### Configuration File (config.yaml)

The `config.yaml` file allows you to customize:

- **News Topics**: List of topics to cover in the digest
- **Prompt Template**: Custom prompt for Claude API
- **Logging Settings**: Log level and format

## GitHub Actions Setup

The project includes a GitHub Actions workflow that runs daily at 9:00 AM UTC.

### Setup Steps:

1. **Add Repository Secrets**

   Go to your GitHub repository → Settings → Secrets and variables → Actions → New repository secret

   Add the following secrets:
   - `ANTHROPIC_API_KEY` (required)
   - `NOTIFICATION_METHODS` (required, e.g., `email,webhook`)
   - Email-related secrets (if using email)
   - `WEBHOOK_URL` (if using webhook)

2. **Enable GitHub Actions**

   Ensure GitHub Actions are enabled in your repository settings.

3. **Manual Trigger**

   You can manually trigger the workflow from the Actions tab → Daily AI News Digest → Run workflow

4. **Customize Schedule**

   Edit `.github/workflows/daily-news.yml` to change the schedule:

   ```yaml
   schedule:
     - cron: '0 9 * * *'  # 9:00 AM UTC daily
   ```

## Project Structure

```
ai-news-bot/
├── .github/
│   └── workflows/
│       └── daily-news.yml       # GitHub Actions workflow
├── src/
│   ├── __init__.py
│   ├── config.py                # Configuration management
│   ├── logger.py                # Logging utilities
│   ├── news_generator.py        # Anthropic API integration
│   └── notifiers/
│       ├── __init__.py
│       ├── email_notifier.py    # Email notification
│       └── webhook_notifier.py  # Webhook notification
├── main.py                      # Main application entry point
├── config.yaml                  # Configuration file
├── requirements.txt             # Python dependencies
├── .env.example                 # Example environment variables
├── .gitignore
└── README.md
```

## Usage Examples

### Email Only

```env
NOTIFICATION_METHODS=email
```

### Webhook Only

```env
NOTIFICATION_METHODS=webhook
```

### Both Email and Webhook

```env
NOTIFICATION_METHODS=email,webhook
```

## Email Setup Guide

### Gmail Setup

1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password:
   - Go to Google Account → Security → 2-Step Verification → App passwords
   - Generate a new app password for "Mail"
3. Use the app password as `SMTP_PASSWORD`

### Other Email Providers

Update `SMTP_HOST` and `SMTP_PORT` according to your provider:

- **Outlook**: `smtp.office365.com:587`
- **Yahoo**: `smtp.mail.yahoo.com:587`
- **SendGrid**: `smtp.sendgrid.net:587`

## Webhook Integration

The webhook sends a JSON payload:

```json
{
  "title": "AI News Digest - 2025-10-25",
  "content": "... news digest content ...",
  "timestamp": "2025-10-25T09:00:00",
  "source": "AI News Bot"
}
```

Compatible with:
- Slack (use Incoming Webhooks)
- Discord (use Webhook URLs)
- Microsoft Teams
- Custom webhook endpoints

## Error Handling

- **Automatic Retries**: The news generator retries up to 3 times on failure
- **Graceful Degradation**: If one notification method fails, others still execute
- **Comprehensive Logging**: All operations are logged with timestamps and context
- **GitHub Actions Artifacts**: Error logs are uploaded for debugging

## Troubleshooting

### "Config file not found" Error

Ensure `config.yaml` exists in the project root.

### Email Not Sending

- Check SMTP credentials are correct
- Verify app password (not regular password) for Gmail
- Check firewall/network settings

### Webhook Failing

- Verify webhook URL is accessible
- Check webhook endpoint accepts JSON POST requests
- Review webhook service logs

### API Errors

- Verify `ANTHROPIC_API_KEY` is valid
- Check API quota/rate limits
- Review Anthropic API status

## Development

### Running Tests (when available)

```bash
pytest
```

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the bot
python main.py
```

## License

MIT License - See LICENSE file for details

## Support

For issues and feature requests, please use the GitHub issue tracker.

## Credits

Powered by [Anthropic Claude](https://www.anthropic.com)
