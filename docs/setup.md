# Detailed Setup Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [NewsAPI Setup](#newsapi-setup)
3. [n8n Installation](#n8n-installation)
4. [Workflow Import](#workflow-import)
5. [Configuration](#configuration)
6. [Testing](#testing)
7. [Activation](#activation)

## Prerequisites

Before starting, ensure you have:

- A computer or server with internet access
- n8n installed (or n8n Cloud account)
- A NewsAPI account (free tier available)
- Optional: Google account (for Sheets integration)
- Optional: Slack workspace (for Slack integration)

## NewsAPI Setup

### Step 1: Create NewsAPI Account

1. Visit https://newsapi.org/register
2. Enter your email address
3. Create a password
4. Click "Register"
5. Verify your email by clicking the link in the confirmation email

### Step 2: Get Your API Key

1. Log in to https://newsapi.org
2. Go to the **Dashboard**
3. Copy your **API Key** (it starts with a long string of characters)
4. Keep this key safe - you'll need it for n8n

### Step 3: Check Your Plan

1. Free tier includes:
   - 100 requests per day
   - Top headlines endpoint
   - Limited sorting options
2. Paid plans include:
   - Unlimited requests
   - Everything News endpoint
   - Advanced filtering

## n8n Installation

### Option A: n8n Self-Hosted (Docker)

#### Prerequisites
- Docker installed on your machine

#### Installation Steps

1. Create a directory for n8n:
```bash
mkdir n8n
cd n8n
```

2. Start n8n with Docker:
```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -e NODE_ENV=production \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

3. Access n8n:
   - Open http://localhost:5678 in your browser
   - Set up your account

4. Keep the container running (don't close the terminal)

#### Optional: Use Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  n8n:
    image: n8nio/n8n
    container_name: n8n
    ports:
      - "5678:5678"
    environment:
      - NODE_ENV=production
    volumes:
      - ~/.n8n:/home/node/.n8n
    restart: unless-stopped
```

Run:
```bash
docker-compose up -d
```

### Option B: n8n Cloud

1. Visit https://n8n.cloud
2. Click "Sign Up"
3. Create your account
4. Start using immediately (no installation needed)

### Option C: n8n npm Installation

```bash
# Install Node.js 16+ first

npm install -g n8n

n8n start
```

## Workflow Import

### Step 1: Access n8n

1. Open http://localhost:5678 (self-hosted) or your n8n Cloud URL
2. Log in with your credentials

### Step 2: Import the Workflow

1. Click **Workflows** in the sidebar
2. Click the **Plus icon** or **New** button
3. Click **Import from File**
4. Navigate to `workflows/trending_news_automation.json`
5. Select it and click **Open**
6. Click **Import**

### Step 3: View Your Workflow

The workflow should now appear in your workflows list. Click on it to open and edit.

## Configuration

### Step 1: Set Up NewsAPI Credentials

1. In the workflow, find the **Fetch Trending News** node (looks like an HTTP request)
2. Click on it to open the configuration panel
3. Under **Credentials**, look for the authentication section
4. Click **Create New Credential** or **Connect**
5. Choose **News API** or **Generic Credential Type**
6. Enter your API key from Step 2 above
7. Click **Test** to verify the connection
8. You should see a success message

### Step 2: Configure the Schedule

1. Find the **Schedule Trigger** node at the beginning of the workflow
2. Click on it
3. Set the frequency:
   - **Unit**: "hours"
   - **Interval**: "6" (for every 6 hours)
4. Or choose your preferred schedule:
   - Hourly: Unit = "hours", Interval = "1"
   - Daily: Unit = "days", Interval = "1"
   - Weekly: Unit = "weeks", Interval = "1"

### Step 3: Customize News Parameters (Optional)

1. Click on the **Fetch Trending News** node
2. Scroll to the **Query Parameters** section
3. Modify as needed:
   - **country**: Change to your country code (us, gb, de, etc.)
   - **pageSize**: Number of articles (1-100)
   - **sortBy**: Sort order (publishedAt, popularity)
   - **category**: Add if desired (business, technology, etc.)

### Step 4: Set Up Optional Outputs

#### Google Sheets Integration

1. Find the **Append to Google Sheets** node
2. Click the **toggle switch** to enable it
3. In the credentials section, click **Create New Credential**
4. Authenticate with your Google account
5. Select the spreadsheet and sheet name
6. Configure the columns mapping

#### Slack Integration

1. Find the **Send to Slack** node
2. Click the **toggle switch** to enable it
3. In the credentials section, create a new Slack credential
4. Authenticate with your Slack workspace
5. Select the channel (e.g., #trending-news)
6. You can customize the message format in the **text** field

#### Webhook Integration

1. Find the **Send to Webhook** node
2. Click the **toggle switch** to enable it
3. Replace the URL with your webhook endpoint
4. Test the webhook to ensure it's working

## Testing

### Test Individual Nodes

1. Click on any node in the workflow
2. Click **Test step** or **Test node**
3. You should see the output below
4. Check for errors or unexpected data

### Test the Entire Workflow

1. Click the **Test Workflow** button (or press Ctrl+Enter)
2. The workflow will execute once
3. Check the **Execution** tab for:
   - Success or error status
   - Number of articles processed
   - Output data

### Expected Output

You should see:
- Articles retrieved from NewsAPI
- Transformed data with standardized fields
- Messages in Slack (if enabled)
- Rows added to Google Sheets (if enabled)

### Troubleshoot Issues

**Issue**: "401 Unauthorized" or "Invalid API Key"
- Verify your NewsAPI key is correct
- Ensure it hasn't exceeded rate limits (100/day free tier)
- Generate a new key if necessary

**Issue**: "No articles found"
- Check the country code is valid
- Verify NewsAPI has data for that country
- Try a different country code temporarily

**Issue**: "Credentials not found"
- Ensure you've created the credential
- Click on the node and check the credentials section
- Re-enter your API key if needed

## Activation

### Step 1: Save the Workflow

Click **Save** (Ctrl+S) to save any changes you've made.

### Step 2: Activate the Workflow

1. Look for the **Activate** button (toggle switch) at the top-right
2. Click it to turn it **On** (it should turn blue/green)
3. You'll see a confirmation message

### Step 3: Verify Activation

1. The workflow is now active and will run on the schedule
2. Go to the **Executions** tab to see when it runs
3. Check the logs for successful executions

### Step 4: Monitor Executions

1. Click on the **Executions** tab
2. You'll see a list of all past and scheduled executions
3. Click on any execution to see details:
   - Start time
   - End time
   - Duration
   - Number of articles
   - Success or error status

## Common Configuration Variations

### Daily News Digest at 9 AM

1. Schedule Trigger:
   - Unit: "hours"
   - Interval: "24"
   - Run at: 9 AM (set in n8n schedule)

### Hourly Updates

1. Schedule Trigger:
   - Unit: "hours"
   - Interval: "1"

### Tech News Only

1. Modify **Filter Tech News** node:
   - Change the condition to filter for technology category
   - Only articles matching the filter go to outputs

### Multiple Countries

1. Create separate workflows for each country
2. Or modify the workflow to loop through multiple country codes
3. Each iteration creates separate articles

## Next Steps

- Review `docs/api-reference.md` for detailed API information
- Check `docs/troubleshooting.md` for common issues
- Explore `workflows/README.md` for advanced customization
- Visit https://docs.n8n.io for comprehensive n8n documentation

## Support Resources

- **n8n Documentation**: https://docs.n8n.io
- **n8n Community Forum**: https://community.n8n.io
- **NewsAPI Documentation**: https://newsapi.org/docs
- **This Repository**: Check the main README.md and docs folder
