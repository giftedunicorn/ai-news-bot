# AI News Bot

An automated system that generates and distributes daily AI news digests using Anthropic's Claude API.

## Features

- **AI-Powered News Generation**: Uses Anthropic's Claude Sonnet 4.5 (latest model, released Sept 2025) to generate comprehensive AI news digests
- **Multilingual Support**: Generate news in 13+ languages including English, Chinese, Spanish, French, Japanese, and more
- **Multiple Notification Channels**: Supports email (via Resend.com) and webhook notifications
- **Flexible Configuration**: Easy-to-customize topics and notification settings via YAML config
- **Automated Scheduling**: GitHub Actions workflow for daily automated execution
- **Robust Error Handling**: Comprehensive logging and retry logic
- **Professional Email Templates**: HTML-formatted emails with clean design
- **Modern Email Delivery**: Uses Resend.com for reliable, developer-friendly email delivery

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

# Optional: Email Configuration with Resend.com
RESEND_API_KEY=re_your_api_key_here
EMAIL_FROM=your_email@yourdomain.com
EMAIL_TO=recipient@example.com

# Optional: Webhook Configuration
WEBHOOK_URL=https://your-webhook-url.com/endpoint

# Notification Methods (comma-separated)
NOTIFICATION_METHODS=email,webhook

# Language Settings (optional, defaults to 'en')
AI_RESPONSE_LANGUAGE=en
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
| `AI_RESPONSE_LANGUAGE` | Optional | Language code for AI responses (default: `en`). Supports: `zh`, `es`, `fr`, `ja`, `de`, `ko`, `pt`, `ru`, `ar`, `hi`, `it`, `nl` |
| `RESEND_API_KEY` | For email | Your Resend.com API key |
| `EMAIL_FROM` | For email | Sender email address (must be verified in Resend) |
| `EMAIL_TO` | For email | Recipient email address |
| `WEBHOOK_URL` | For webhook | Webhook endpoint URL |

### Configuration File (config.yaml)

The `config.yaml` file allows you to customize:

- **News Topics**: List of topics to cover in the digest
- **Prompt Template**: Custom prompt for Claude API
- **Logging Settings**: Log level and format

### AI Model Configuration

The bot uses **Claude Sonnet 4.5** (`claude-sonnet-4-5-20250929`) by default - Anthropic's latest and most capable model for general use.

**To use a different model**, modify `src/news_generator.py:39`:

```python
# Available models (as of October 2025):
model: str = "claude-sonnet-4-5-20250929"  # Latest Sonnet (default) - Best for most tasks
# model: str = "claude-haiku-4-5-20251001"  # Latest Haiku - Fastest, most cost-effective
# model: str = "claude-opus-4-1-20250805"   # Latest Opus - Most powerful (higher cost)

# Or use aliases (automatically use latest version):
# model: str = "claude-sonnet-4-5"  # Alias for latest Sonnet
# model: str = "claude-haiku-4-5"   # Alias for latest Haiku
# model: str = "claude-opus-4-1"    # Alias for latest Opus
```

**Pricing (per million tokens):**
- Claude Sonnet 4.5: $3 input / $15 output
- Claude Haiku 4.5: $1 input / $5 output
- Claude Opus 4.1: Higher cost, maximum capability

Or pass the model parameter when calling:
```python
news_gen.generate_news_digest(
    topics=topics,
    prompt_template=template,
    model="claude-sonnet-4-5-20250929"
)
```

### Language Configuration

The bot supports **multilingual AI responses**. Set the `AI_RESPONSE_LANGUAGE` environment variable to generate news in your preferred language.

**Supported Languages:**

| Code | Language | Native Name |
|------|----------|-------------|
| `en` | English | English (default) |
| `zh` | Chinese | 中文 |
| `es` | Spanish | Español |
| `fr` | French | Français |
| `ja` | Japanese | 日本語 |
| `de` | German | Deutsch |
| `ko` | Korean | 한국어 |
| `pt` | Portuguese | Português |
| `ru` | Russian | Русский |
| `ar` | Arabic | العربية |
| `hi` | Hindi | हिन्दी |
| `it` | Italian | Italiano |
| `nl` | Dutch | Nederlands |

**Example Usage:**

```bash
# In .env file
AI_RESPONSE_LANGUAGE=zh  # For Chinese
AI_RESPONSE_LANGUAGE=es  # For Spanish
AI_RESPONSE_LANGUAGE=ja  # For Japanese
```

Or programmatically:
```python
news_gen.generate_news_digest(
    topics=topics,
    prompt_template=template,
    language="zh"  # Chinese
)
```

The AI will generate the entire news digest in the specified language, including headlines, descriptions, and analysis.

## GitHub Actions Setup

The project includes a GitHub Actions workflow that runs daily at 9:00 AM UTC.

### Setup Steps:

1. **Add Repository Secrets**

   Go to your GitHub repository → Settings → Secrets and variables → Actions → New repository secret

   Add the following secrets:
   - `ANTHROPIC_API_KEY` (required)
   - `NOTIFICATION_METHODS` (required, e.g., `email,webhook`)
   - `AI_RESPONSE_LANGUAGE` (optional, e.g., `zh`, `es`, `ja` - defaults to `en`)
   - `RESEND_API_KEY` (if using email)
   - `EMAIL_FROM` (if using email)
   - `EMAIL_TO` (if using email)
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

## Email Setup Guide with Resend.com

### Setting Up Resend

1. **Sign up for Resend**
   - Go to [resend.com](https://resend.com) and create an account
   - Resend offers a generous free tier (100 emails/day, 3,000 emails/month)

2. **Get Your API Key**
   - Navigate to API Keys in your Resend dashboard
   - Create a new API key
   - Copy the API key (starts with `re_`) and set it as `RESEND_API_KEY`

3. **Verify Your Domain** (Recommended for production)
   - Go to Domains in your Resend dashboard
   - Add and verify your domain by adding DNS records
   - Once verified, you can send from any address at your domain

4. **For Testing** (No domain verification needed)
   - You can use `onboarding@resend.dev` as the `EMAIL_FROM` address
   - This is only for testing and has sending limits
   - For production use, verify your own domain

### Why Resend?

- **Simple API**: Easy-to-use REST API, much simpler than SMTP
- **Better Deliverability**: Higher inbox placement rates
- **No SMTP Configuration**: No need to manage SMTP credentials
- **Modern**: Built for developers with excellent documentation
- **Analytics**: Track email delivery and engagement

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

- Verify `RESEND_API_KEY` is correct and active
- Ensure `EMAIL_FROM` is verified in Resend (or use `onboarding@resend.dev` for testing)
- Check Resend dashboard for delivery logs and errors
- Verify you haven't exceeded Resend's sending limits

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
