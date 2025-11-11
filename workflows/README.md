# N8N Workflows

This directory contains all n8n workflow definitions exported as JSON files.

## Workflow Files

### trending_news_automation.json

**Purpose:** Fetch and process trending news articles

**Trigger:** Schedule (configurable)

**Data Sources:**
- NewsAPI (https://newsapi.org) - Free and paid tiers

**Workflow Nodes:**

1. **Schedule Trigger** - Runs on a schedule (default: every 6 hours)
2. **Fetch Trending News** - HTTP request to NewsAPI
3. **Check Success** - Validates API response
4. **Check If Articles Found** - Ensures articles exist
5. **Loop Through Articles** - Iterates over each article
6. **Transform Article Data** - Normalizes article structure
7. **Filter Tech News** - Optional filtering by category
8. **Process Articles** - Custom JavaScript processing
9. **Append to Google Sheets** - Optional Google Sheets integration
10. **Send to Slack** - Optional Slack notifications
11. **Send to Webhook** - Optional webhook delivery

**Data Transformation:**

Input from NewsAPI:
```json
{
  "title": "Article Title",
  "description": "Article description",
  "url": "https://example.com",
  "urlToImage": "https://example.com/image.jpg",
  "source": { "name": "Source Name" },
  "publishedAt": "2024-01-01T00:00:00Z",
  "author": "Author Name",
  "content": "Full article content"
}
```

Output after transformation:
```json
{
  "title": "Article Title",
  "description": "Article description",
  "url": "https://example.com",
  "imageUrl": "https://example.com/image.jpg",
  "source": "Source Name",
  "publishedAt": "2024-01-01T00:00:00Z",
  "author": "Author Name",
  "content": "Full article content",
  "processedAt": "2024-01-01T12:00:00Z",
  "sentiment": "detailed"
}
```

## How to Import Workflows

### Method 1: Via n8n UI
1. Open n8n
2. Go to **Workflows** tab
3. Click **New**
4. Click **Import from File**
5. Select the JSON file
6. Configure credentials
7. Activate the workflow

### Method 2: Via n8n API
```bash
curl -X POST http://localhost:5678/api/v1/workflows/import \
  -H "Content-Type: application/json" \
  -d @workflows/trending_news_automation.json
```

## Customization Guide

### Change Schedule Frequency

Edit the "Schedule Trigger" node:
- `unit`: "hours", "days", "weeks", "minutes"
- `interval`: number (e.g., 6 for every 6 hours)

### Change News Country

Edit the "Fetch Trending News" node query parameters:
```json
{
  "name": "country",
  "value": "us"  // Change to: gb, de, fr, etc.
}
```

### Add Category Filter

Modify the query parameters to include `category`:
```json
{
  "name": "category",
  "value": "technology"  // Options: business, entertainment, health, science, sports, technology
}
```

### Add Slack Integration

1. Enable the "Send to Slack" node
2. Connect your Slack workspace
3. Select or create a channel
4. Customize the message template

### Add Google Sheets Integration

1. Enable the "Append to Google Sheets" node
2. Authenticate with Google
3. Select your spreadsheet
4. Configure the columns mapping

## Monitoring and Debugging

### View Execution Logs
- Click on a workflow → **Executions**
- View detailed logs for each execution
- Check error messages and stack traces

### Test a Node
- Click on a node
- Click **Test step**
- View sample output

### Debug Custom Code
Add `console.log()` statements in code nodes:
```javascript
console.log("Processing article:", $json.title);
return $json;
```

## Best Practices

1. **Error Handling:** Always add error branches for API calls
2. **Rate Limiting:** Respect API rate limits (NewsAPI: 100/day free tier)
3. **Data Validation:** Check data structure before processing
4. **Logging:** Add descriptive node names for easier debugging
5. **Credentials:** Store API keys securely in n8n credentials
6. **Testing:** Test workflows before activating
7. **Monitoring:** Regularly review execution logs for failures

## Troubleshooting

### Workflow Not Executing

**Symptom:** Schedule trigger not running

**Solution:**
1. Verify workflow is **Active** (toggle switch)
2. Check n8n instance is running
3. Check server logs for errors
4. Verify the schedule time is correct

### API Connection Issues

**Symptom:** 401 or 403 errors

**Solution:**
1. Verify API key is valid
2. Check API key hasn't exceeded rate limits
3. Ensure API key has correct permissions
4. Test API directly: `curl -H "Authorization: Bearer KEY" https://api.newsapi.org/...`

### No Data Returned

**Symptom:** Workflow runs but returns empty results

**Solution:**
1. Check API response in **Fetch Trending News** node
2. Verify query parameters are correct
3. Check data with sample request at https://newsapi.org/docs
4. Ensure country/category parameters are valid

## Advanced Usage

### Custom Processing

Edit the "Process Articles" code node to add custom logic:

```javascript
return items.map(item => ({
  ...item.json,
  // Add custom fields
  keywords: item.json.title.split(' ').filter(w => w.length > 4),
  readingTime: Math.ceil((item.json.content?.length || 0) / 200),

  // Add custom transformations
  headline: item.json.title.toUpperCase(),
}));
```

### Conditional Outputs

Use the "Filter Tech News" node pattern to route articles:
- Set different conditions
- Route to different output nodes
- Create category-specific workflows

### Webhooks and External Systems

Send article data to external systems:
```javascript
{
  "method": "POST",
  "url": "https://your-api.com/articles",
  "body": {
    "article": $json,
    "timestamp": new Date().toISOString()
  }
}
```

## Related Documentation

- [n8n Official Docs](https://docs.n8n.io)
- [NewsAPI Documentation](https://newsapi.org/docs)
- [n8n HTTP Request Node](https://docs.n8n.io/nodes/n8n-nodes-base.httpRequest/)
- [n8n Schedule Trigger](https://docs.n8n.io/nodes/n8n-nodes-base.scheduleTrigger/)
