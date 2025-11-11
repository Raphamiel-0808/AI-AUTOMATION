# AI-AUTOMATION

A collection of n8n workflow automations for retrieving and processing trending news from various sources.

## Overview

This repository contains production-ready n8n workflows for automating news retrieval, filtering, and distribution tasks.

## Available Workflows

### 1. Trending News Automation (`workflows/trending_news_automation.json`)

Automatically fetch and process trending news articles from NewsAPI.

**Features:**
- Scheduled execution (every 6 hours by default)
- Fetch top headlines from NewsAPI
- Data transformation and enrichment
- Optional filtering (e.g., tech news only)
- Multiple output options:
  - Google Sheets integration
  - Slack notifications
  - Webhook delivery
  - Custom code processing

**Flow:**
1. Schedule trigger → 2. Fetch news from API → 3. Validate data → 4. Loop and transform articles → 5. Optional filtering → 6. Send to outputs

## Prerequisites

- n8n installed and running (self-hosted or cloud)
- NewsAPI account and API key (free tier available at https://newsapi.org)
- Optional: Google Sheets API credentials (for sheet integration)
- Optional: Slack workspace and bot token (for Slack integration)

## Setup Instructions

### 1. Get NewsAPI Key

1. Visit https://newsapi.org/register
2. Sign up for a free account
3. Copy your API key from the dashboard

### 2. Import Workflow into n8n

1. Open your n8n instance
2. Go to **Workflows** → **New**
3. Click **Import from File**
4. Select `workflows/trending_news_automation.json`
5. Click **Import**

### 3. Configure Credentials

1. In the workflow, click **Fetch Trending News** node
2. Click **Connect** or create new credentials
3. Choose **News API** or **Generic Credential Type**
4. Paste your NewsAPI key
5. Test the connection

### 4. (Optional) Enable Output Nodes

To send news to Slack or Google Sheets:

1. **For Slack:**
   - Click the **Send to Slack** node
   - Enable the node (toggle switch)
   - Connect your Slack workspace
   - Set the channel (e.g., #trending-news)

2. **For Google Sheets:**
   - Click the **Append to Google Sheets** node
   - Enable the node
   - Authenticate with Google
   - Select your spreadsheet and sheet

3. **For Webhooks:**
   - Click the **Send to Webhook** node
   - Replace the webhook URL with your endpoint
   - Enable if needed

### 5. Customize the Workflow

- **Change Schedule:** Edit the **Schedule Trigger** node interval
- **Change Country:** Modify the `country` parameter in **Fetch Trending News**
- **Change Page Size:** Adjust `pageSize` (1-100, default 20)
- **Add Filters:** Modify the **Filter Tech News** node conditions
- **Add More Processing:** Edit the **Process Articles** code node

## Project Structure

```
AI-AUTOMATION/
├── README.md                          # This file
├── .gitignore                         # Git ignore rules
├── workflows/
│   ├── trending_news_automation.json  # Main trending news workflow
│   └── README.md                      # Workflow documentation
├── docs/
│   ├── setup.md                       # Detailed setup guide
│   ├── api-reference.md               # API reference
│   └── troubleshooting.md             # Common issues and fixes
└── examples/
    └── output-samples.json            # Example workflow outputs
```

## Configuration Options

### NewsAPI Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| `country` | 2-letter code (us, gb, etc.) | Country to fetch news from |
| `pageSize` | 1-100 | Number of articles per request |
| `sortBy` | publishedAt, popularity | Sort order |
| `category` | business, tech, health, etc. | Optional category filter |

### Schedule Options

- **Every hour:** Set unit to "hours", interval to 1
- **Every 6 hours:** Set unit to "hours", interval to 6
- **Daily:** Set unit to "days", interval to 1
- **Weekly:** Set unit to "weeks", interval to 1

## API Limits

- **NewsAPI Free Tier:** 100 requests per day
- **Recommended Schedule:** Every 6 hours (4 requests/day)

## Troubleshooting

### API Key Error
- Verify your API key is correct and active
- Check that your free tier subscription is valid
- Ensure the API key has not exceeded daily limits

### No Articles Returned
- Check the `country` parameter is valid
- Verify the API is responding with data
- Check network connectivity

### Webhook Delivery Issues
- Verify the webhook URL is correct and accessible
- Check that your webhook endpoint is publicly accessible
- Test with webhook.site for debugging

## Environment Variables (Optional)

Create a `.env` file for development:

```
NEWS_API_KEY=your_api_key_here
SLACK_BOT_TOKEN=xoxb-xxxxx
GOOGLE_SHEETS_ID=your_sheet_id
```

## Examples

See `examples/output-samples.json` for sample workflow outputs and data structures.

## Support

For issues with:
- **n8n:** Check n8n documentation at https://docs.n8n.io
- **NewsAPI:** Visit https://newsapi.org/docs
- **This repo:** Check the `docs/` folder or create an issue

## License

This project is provided as-is for automation purposes.
