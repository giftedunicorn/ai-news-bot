# AI News Bot

An automated system that generates and distributes daily AI news digests using Anthropic's Claude API.

## Features

- **AI-Powered News Generation**: Uses Anthropic's Claude Sonnet 4.5 (latest model, released Sept 2025) to generate comprehensive AI news digests
- **Beautiful Email Formatting**: Automatically converts AI content to stunning HTML emails - no markdown, just clean professional design
- **Customizable Prompts**: 9 pre-built templates (comprehensive, research, business, technical, etc.) or create your own
- **Multilingual Support**: Generate news in 13+ languages including English, Chinese, Spanish, French, Japanese, and more
- **Multiple Notification Channels**: Supports email (via Resend.com) and webhook notifications
- **Flexible Configuration**: Easy-to-customize topics and notification settings via YAML config
- **Automated Scheduling**: GitHub Actions workflow for daily automated execution
- **Robust Error Handling**: Comprehensive logging and retry logic
- **Email Client Compatible**: Works perfectly in Gmail, Outlook, Apple Mail, and mobile email apps
- **Modern Email Delivery**: Uses Resend.com for reliable, developer-friendly email delivery

## 🚀 Deployment Options

Choose your deployment method:

| Method | Configuration | When to Use |
|--------|--------------|-------------|
| **Local Development** | `.env` file | Testing locally on your computer |
| **GitHub Actions** | Repository Secrets | Automated daily runs (recommended) |

> 💡 **Tip**: Start with local development to test, then deploy to GitHub Actions for automation.
>
> 📋 **Setup Checklist**: Use [CONFIGURATION_CHECKLIST.md](CONFIGURATION_CHECKLIST.md) to ensure everything is configured correctly.

## Quick Start (Local Development)

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd ai-news-bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Settings (For Local Development)

For **local development**, copy the example file and fill in your credentials:

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

> **Note**: The `.env` file is only for **local development**. For GitHub Actions automation, you'll configure these as **GitHub Secrets** (see [GitHub Actions Setup](#github-actions-setup) below).

### 4. Customize News Prompt (Optional)

The bot uses an **optimized, concise prompt** (15 lines vs 50+ in typical systems) that generates high-quality news digests.

**Default Prompt** (in config.yaml):
```yaml
Summarize 10 recent AI news items (5 international + 5 domestic) covering: {topics}

Format:
International News:
1. [Headline]
[2-3 sentence summary]
Source: [Name]

Domestic News:
1. [Headline]
...

Rules: Recent news, no markdown, clear language
```

**Why it's concise:**
- ✅ Faster processing
- ✅ Lower cost
- ✅ Easier to maintain
- ✅ No redundancy

**Multi-Language Support:**

Prompts are in English (best for Claude), but output can be in **13+ languages**:
```bash
# In .env file
AI_RESPONSE_LANGUAGE=zh  # Chinese output
AI_RESPONSE_LANGUAGE=es  # Spanish output
AI_RESPONSE_LANGUAGE=ja  # Japanese output
# Supports: en, zh, es, fr, ja, de, ko, pt, ru, ar, hi, it, nl
```

**Pre-built Templates** (config.examples.yaml):
1. Comprehensive (default) - Balanced coverage
2. Research - Academic focus
3. Business - Industry & funding
4. Technical - Engineering depth
5. Startup - Early-stage companies
6. Policy - Regulations
7. Weekly - Top stories
8. Concise - Ultra-brief
9. Chinese - 中文示例

📖 **Full Guide**: See [PROMPT_GUIDE.md](PROMPT_GUIDE.md) for customization and multi-language details.

### 5. Run Locally

```bash
python main.py
```

## Configuration

### Configuration Variables

The bot requires the following configuration. How you set them depends on your deployment:

- **Local Development**: Use `.env` file (see [Quick Start](#quick-start))
- **GitHub Actions**: Use GitHub Repository Secrets (see [GitHub Actions Setup](#github-actions-setup))

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | ✅ Required | Your Anthropic API key |
| `NOTIFICATION_METHODS` | ✅ Required | Comma-separated list: `email`, `webhook`, or `email,webhook` |
| `AI_RESPONSE_LANGUAGE` | Optional | Language code for AI responses (default: `en`). Supports: `zh`, `es`, `fr`, `ja`, `de`, `ko`, `pt`, `ru`, `ar`, `hi`, `it`, `nl` |
| `RESEND_API_KEY` | If using email | Your Resend.com API key |
| `EMAIL_FROM` | If using email | Sender email address (must be verified in Resend) |
| `EMAIL_TO` | If using email | Recipient email address |
| `WEBHOOK_URL` | If using webhook | Webhook endpoint URL |

### Configuration File (config.yaml)

The `config.yaml` file allows you to customize the news digest behavior:

**News Configuration**:
- **Topics**: Focus areas for news selection (optional, guides the AI)
- **Prompt Template**: The instruction template for Claude API
  - Default: Comprehensive 10-item digest (5 international + 5 domestic)
  - Fully customizable with your own prompts
  - See `config.examples.yaml` for 9 pre-built templates

**Logging Settings**: Control log verbosity and format

**Example Structure**:
```yaml
news:
  topics:
    - "Technical breakthroughs"
    - "Product launches"

  prompt_template: |
    Your custom prompt...
    Focus: {topics}

logging:
  level: INFO
  format: "%(asctime)s - %(levelname)s - %(message)s"
```

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

**How It Works:**
- Prompts are always in **English** (best for Claude understanding)
- Output can be in **13+ languages** (automatic translation)
- Set `AI_RESPONSE_LANGUAGE` in `.env` or GitHub Secrets

**Supported Languages:**

`en` (English) • `zh` (中文) • `es` (Español) • `fr` (Français) • `ja` (日本語) • `de` (Deutsch) • `ko` (한국어) • `pt` (Português) • `ru` (Русский) • `ar` (العربية) • `hi` (हिन्दी) • `it` (Italiano) • `nl` (Nederlands)

**Usage:**

```bash
# .env file
AI_RESPONSE_LANGUAGE=zh  # Full Chinese output

# GitHub Secret
# Add: AI_RESPONSE_LANGUAGE = zh
```

**Example Output (Chinese):**
```
国际新闻：

1. OpenAI发布GPT-5增强推理能力
OpenAI发布了GPT-5...
来源：OpenAI官方博客
```

The system automatically adds: "IMPORTANT: Please respond entirely in Chinese (中文)" to the prompt.

## GitHub Actions Setup

The project includes a GitHub Actions workflow that runs daily at midnight UTC (00:00).

> **Important**: GitHub Actions uses **Repository Secrets** for configuration (NOT environment variables). All settings must be added as secrets.
>
> 📖 **Detailed Setup Guide**: See [GITHUB_SETUP.md](GITHUB_SETUP.md) for step-by-step instructions with screenshots and troubleshooting.

### Step 1: Add GitHub Repository Secrets

Navigate to your GitHub repository:

```
Repository → Settings → Secrets and variables → Actions → Repository secrets → New repository secret
```

Add the following secrets one by one:

#### ✅ Required Secrets

| Secret Name | Example Value | Description |
|-------------|---------------|-------------|
| `ANTHROPIC_API_KEY` | `sk-ant-api03-xxx...` | Your Anthropic API key |
| `NOTIFICATION_METHODS` | `email,webhook` | Notification channels (comma-separated) |

#### 📧 Email Secrets (if using email notifications)

| Secret Name | Example Value | Description |
|-------------|---------------|-------------|
| `RESEND_API_KEY` | `re_123abc...` | Your Resend.com API key |
| `EMAIL_FROM` | `news@yourdomain.com` | Sender email (must be verified in Resend) |
| `EMAIL_TO` | `you@example.com` | Recipient email address |

#### 🔗 Webhook Secrets (if using webhook notifications)

| Secret Name | Example Value | Description |
|-------------|---------------|-------------|
| `WEBHOOK_URL` | `https://hooks.slack.com/...` | Your webhook endpoint URL |

#### 🌍 Optional Secrets

| Secret Name | Example Value | Description |
|-------------|---------------|-------------|
| `AI_RESPONSE_LANGUAGE` | `zh` or `es` or `ja` | Language code (defaults to `en` if not set) |

### Step 2: Enable GitHub Actions

Ensure GitHub Actions are enabled in your repository settings:

```
Repository → Settings → Actions → General → Allow all actions and reusable workflows
```

### Step 3: Manual Trigger (Test Your Setup)

Once secrets are configured, test your setup:

```
Repository → Actions tab → Daily AI News Digest → Run workflow button
```

This will run the workflow immediately so you can verify everything is working.

### Step 4: Customize Schedule (Optional)

The workflow runs daily at midnight UTC by default. To change the schedule, edit `.github/workflows/daily-news.yml`:

```yaml
schedule:
  - cron: '0 0 * * *'  # Midnight UTC daily (current)
  - cron: '0 9 * * *'  # 9:00 AM UTC daily
  - cron: '0 */6 * * *'  # Every 6 hours
```

Use [crontab.guru](https://crontab.guru/) to create custom schedules.

## Project Structure

```
ai-news-bot/
├── .github/
│   └── workflows/
│       └── daily-news.yml           # GitHub Actions workflow
├── src/
│   ├── __init__.py
│   ├── config.py                    # Configuration management
│   ├── logger.py                    # Logging utilities
│   ├── news_generator.py            # Anthropic API integration
│   └── notifiers/
│       ├── __init__.py
│       ├── email_notifier.py        # Email notification
│       └── webhook_notifier.py      # Webhook notification
├── docs/
│   └── CONFIGURATION_GUIDE.md       # Detailed configuration guide
├── main.py                          # Main application entry point
├── config.yaml                      # Active configuration file
├── config.examples.yaml             # 9 pre-built prompt templates ⭐
├── requirements.txt                 # Python dependencies
├── .env.example                     # Example environment variables
├── GITHUB_SETUP.md                  # GitHub Actions setup guide
├── CONFIGURATION_CHECKLIST.md       # Setup checklist
├── test_setup.py                    # Configuration verification script
├── example_usage.py                 # Usage examples
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

## Email Format

### Beautiful, Email-Friendly Design

The bot generates **email-optimized content** that looks stunning across all email clients:

**Features:**
- ✅ No markdown formatting (clean, professional appearance)
- ✅ Automatic HTML conversion with beautiful styling
- ✅ Numbered news cards with visual badges
- ✅ Color-coded sections and headers
- ✅ Mobile-responsive layout
- ✅ Works in Gmail, Outlook, Apple Mail, and all mobile apps

**What recipients see:**
- Clean white container with professional styling
- Blue section headers with subtle borders
- Numbered news items in styled cards
- Italicized source citations
- Comfortable reading experience on any device

**Preview your emails:**
```bash
python test_email_format.py
open email_preview.html
```

📖 **Detailed Guide**: See [EMAIL_FORMAT_GUIDE.md](EMAIL_FORMAT_GUIDE.md) for customization options and troubleshooting.

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
