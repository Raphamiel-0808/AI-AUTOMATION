# API Reference

## NewsAPI Reference

### Base URL
```
https://newsapi.org/v2
```

### Top Headlines Endpoint

The main endpoint used in the trending news automation.

**Endpoint:**
```
GET /top-headlines
```

**Authentication:**
```
Query Parameter: apiKey=[YOUR_API_KEY]
```

**Parameters:**

| Parameter | Type | Required | Options |
|-----------|------|----------|---------|
| `country` | string | Yes* | 2-letter country code (see list below) |
| `category` | string | No | See category list below |
| `q` | string | No | Search keyword/phrase |
| `pageSize` | integer | No | 1-100 (default: 20) |
| `page` | integer | No | Starting page (for pagination) |
| `sortBy` | string | No | `publishedAt`, `popularity`, `relevancy` |

*Either `country` or `category` is required, or use `q` with API key

### Response Format

**Success Response (200):**
```json
{
  "status": "ok",
  "totalResults": 1234,
  "articles": [
    {
      "source": {
        "id": "bbc-news",
        "name": "BBC News"
      },
      "author": "John Smith",
      "title": "Article Title Here",
      "description": "Article description...",
      "url": "https://example.com/article",
      "urlToImage": "https://example.com/image.jpg",
      "publishedAt": "2024-01-15T14:30:00Z",
      "content": "Full article content..."
    }
  ]
}
```

**Error Response:**
```json
{
  "status": "error",
  "code": "apiKeyInvalid",
  "message": "Your API key is invalid or incorrect."
}
```

### Supported Countries

| Code | Country |
|------|---------|
| ae | United Arab Emirates |
| ar | Argentina |
| at | Austria |
| au | Australia |
| be | Belgium |
| bg | Bulgaria |
| br | Brazil |
| by | Belarus |
| ca | Canada |
| ch | Switzerland |
| cn | China |
| co | Colombia |
| cu | Cuba |
| cz | Czech Republic |
| de | Germany |
| eg | Egypt |
| fr | France |
| gb | United Kingdom |
| gr | Greece |
| hk | Hong Kong |
| hu | Hungary |
| id | Indonesia |
| ie | Ireland |
| il | Israel |
| in | India |
| it | Italy |
| jp | Japan |
| kr | South Korea |
| lt | Lithuania |
| lv | Latvia |
| ma | Morocco |
| mx | Mexico |
| my | Malaysia |
| ng | Nigeria |
| nl | Netherlands |
| no | Norway |
| nz | New Zealand |
| ph | Philippines |
| pl | Poland |
| pt | Portugal |
| ro | Romania |
| rs | Serbia |
| ru | Russia |
| sa | Saudi Arabia |
| se | Sweden |
| sg | Singapore |
| si | Slovenia |
| sk | Slovakia |
| th | Thailand |
| tr | Turkey |
| tw | Taiwan |
| ua | Ukraine |
| us | United States |
| ve | Venezuela |
| za | South Africa |

### Supported Categories

- `business`
- `entertainment`
- `general`
- `health`
- `science`
- `sports`
- `technology`

### Rate Limiting

**Free Tier:**
- 100 requests per day
- 1 request per second

**Paid Plans:**
- Requests per day based on plan
- Higher rate limits

**Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1642252800
```

### Example Requests

**Get US Top Headlines:**
```
GET https://newsapi.org/v2/top-headlines?country=us&pageSize=20&apiKey=YOUR_API_KEY
```

**Get Technology News from Multiple Countries:**
```
GET https://newsapi.org/v2/top-headlines?category=technology&pageSize=20&apiKey=YOUR_API_KEY
```

**Get News with Pagination:**
```
GET https://newsapi.org/v2/top-headlines?country=us&page=2&pageSize=20&apiKey=YOUR_API_KEY
```

### Response Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `source.id` | string | Identifier for the news source |
| `source.name` | string | Display name of the news source |
| `author` | string | Author of the article |
| `title` | string | Headline of the article |
| `description` | string | Short summary/excerpt |
| `url` | string | Link to the article |
| `urlToImage` | string | Link to the article's image |
| `publishedAt` | datetime | Publication timestamp (ISO 8601) |
| `content` | string | Full article text (may be truncated) |

## N8N Node Reference

### HTTP Request Node Configuration

**For NewsAPI in the automation:**

```json
{
  "url": "https://newsapi.org/v2/top-headlines",
  "method": "GET",
  "authentication": "queryAuth",
  "queryAuth": {
    "key": "apiKey",
    "value": "YOUR_API_KEY"
  },
  "queryParameters": {
    "country": "us",
    "pageSize": "20",
    "sortBy": "publishedAt"
  }
}
```

### Schedule Trigger Configuration

```json
{
  "triggerName": "Schedule Trigger",
  "unit": "hours",
  "interval": 6
}
```

**Available Units:**
- `minutes`
- `hours`
- `days`
- `weeks`

### Set Node (Data Transformation)

```json
{
  "mode": "expression",
  "expression": "={\n  \"title\": $json.title,\n  \"source\": $json.source.name,\n  \"url\": $json.url\n}"
}
```

### Split in Batches (Loop)

```json
{
  "mode": "simple",
  "loopOver": "articles"
}
```

### If Node (Conditional)

```json
{
  "mode": "runOnceForAllItems",
  "expression": "={{ $json.articles.length > 0 }}"
}
```

### Code Node (JavaScript)

```json
{
  "functionCode": "return items.map(item => ({\n  ...item.json,\n  processedAt: new Date().toISOString()\n}));"
}
```

## Data Flow in the Workflow

```
Schedule Trigger
    ↓
Fetch Trending News (NewsAPI)
    ↓
Check Success (Validate 200 status)
    ↓
Check If Articles Found (Validate articles exist)
    ↓
Loop Through Articles (Iterate each article)
    ↓
Transform Article Data (Normalize fields)
    ↓
Filter Tech News (Optional filtering)
    ↓
Process Articles (Custom JavaScript)
    ↓
Output Nodes:
├─ Google Sheets
├─ Slack
└─ Webhook
```

## Webhook Integration Example

If you're sending data to your own webhook:

**Webhook Payload:**
```json
{
  "title": "Breaking News Article",
  "description": "Article summary...",
  "url": "https://example.com",
  "imageUrl": "https://example.com/img.jpg",
  "source": "News Source",
  "publishedAt": "2024-01-15T14:30:00Z",
  "processedAt": "2024-01-15T14:35:00Z"
}
```

**Webhook Headers:**
```
Content-Type: application/json
User-Agent: n8n-automation/1.0
```

## Common HTTP Status Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid parameters |
| 401 | Unauthorized | Invalid/missing API key |
| 403 | Forbidden | API key not allowed for endpoint |
| 429 | Rate Limited | Too many requests, wait before retrying |
| 500 | Server Error | NewsAPI server issue, retry later |

## Error Codes from NewsAPI

| Code | Message | Solution |
|------|---------|----------|
| apiKeyMissing | Your API key is missing | Add apiKey parameter |
| apiKeyInvalid | Your API key is invalid | Check your API key |
| apiKeyDisabled | Your API key has been disabled | Contact NewsAPI support |
| parameterInvalid | Your request parameters are invalid | Check parameter values |
| parametersNotAccepted | You've included a parameter that is not permitted | Remove invalid parameters |
| tooManyRequests | You have been rate limited | Wait and retry |
| requestsUnavailable | Your account is not allowed to use this endpoint | Check your plan |
| serverError | Server error, please try again | Retry the request |

## Environment Variables

For development, you can use environment variables:

```bash
export NEWS_API_KEY="your_api_key_here"
export SLACK_BOT_TOKEN="xoxb-your-token"
export WEBHOOK_URL="https://your-webhook.com"
```

In n8n, reference them:
```
{{ $env.NEWS_API_KEY }}
{{ $env.SLACK_BOT_TOKEN }}
{{ $env.WEBHOOK_URL }}
```

## Performance Notes

- **API Response Time**: Usually 200-500ms
- **Data Processing**: 1-5ms per article (depending on complexity)
- **Total Workflow Time**: Typically 5-10 seconds for 20 articles
- **Storage**: Each article requires ~5-10KB when stored

## Rate Limit Strategy

To avoid hitting rate limits with free tier (100 requests/day):

**Recommended Schedule:**
- Every 6 hours = 4 requests/day ✓ (Safe)
- Every 4 hours = 6 requests/day ✓ (Safe)
- Every 2 hours = 12 requests/day ✓ (Safe)
- Every hour = 24 requests/day ✓ (Safe)
- Every 30 minutes = 48 requests/day ✓ (Safe)

**Avoid:**
- Every 5 minutes = 288 requests/day ✗ (Exceeds limit)
- Every 10 minutes = 144 requests/day ✗ (Exceeds limit)

## References

- [NewsAPI Official Documentation](https://newsapi.org/docs)
- [NewsAPI Pricing](https://newsapi.org/pricing)
- [n8n HTTP Request Node Docs](https://docs.n8n.io/nodes/n8n-nodes-base.httpRequest/)
