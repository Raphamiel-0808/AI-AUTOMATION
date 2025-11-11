# Troubleshooting Guide

## Common Issues and Solutions

### 1. API Key Issues

#### Problem: "401 Unauthorized" or "Invalid API Key"

**Symptoms:**
- Workflow fails with 401 error
- Error message: "API key invalid or incorrect"
- No articles are returned

**Solutions:**

1. **Verify API Key:**
   - Log into https://newsapi.org
   - Go to Dashboard
   - Copy your API key exactly (including all characters)
   - Ensure there are no spaces before/after

2. **Check Credential Storage:**
   - In n8n, click on the **Fetch Trending News** node
   - Click **Credentials** section
   - Verify the API key matches what you copied

3. **Regenerate API Key:**
   - If issues persist, regenerate your API key at NewsAPI
   - Update the credential in n8n

4. **Test Directly:**
   - Use curl to test:
   ```bash
   curl "https://newsapi.org/v2/top-headlines?country=us&apiKey=YOUR_API_KEY"
   ```
   - If this works, the issue is in n8n configuration

#### Problem: "403 Forbidden"

**Symptoms:**
- Error message: "Forbidden"
- You have a valid API key

**Solutions:**
- Your API key doesn't have permission for the endpoint
- Ensure your NewsAPI plan supports the top-headlines endpoint
- Try with a different country or category

### 2. Rate Limiting

#### Problem: "429 Too Many Requests"

**Symptoms:**
- Workflow fails after running frequently
- Error message: "Rate limit exceeded"
- Requests were working, then stopped

**Solutions:**

1. **Check Your Plan:**
   - Free tier: 100 requests per day
   - Paid plans: More requests available
   - Visit https://newsapi.org/pricing

2. **Reduce Request Frequency:**
   - Change schedule interval:
     ```
     Current: Every 1 hour (24 req/day)
     Try: Every 6 hours (4 req/day)
     ```
   - Click **Schedule Trigger** node
   - Change interval from 1 to 6

3. **Monitor Rate Limits:**
   - Watch response headers:
     ```
     X-RateLimit-Remaining: 50
     X-RateLimit-Reset: 1642252800
     ```
   - Implement backoff strategy in code node

4. **Add Error Handling:**
   ```javascript
   if (error.statusCode === 429) {
     // Wait before retrying
     throw new Error("Rate limited, will retry later");
   }
   ```

### 3. No Articles Returned

#### Problem: "Empty Articles Array"

**Symptoms:**
- Workflow runs successfully but returns 0 articles
- No data to process
- Loop section is skipped

**Solutions:**

1. **Verify Country Code:**
   - Ensure country code is valid (2 letters)
   - Check list in `docs/api-reference.md`
   ```json
   "country": "us"  // ✓ Correct
   "country": "usa" // ✗ Wrong (3 letters)
   ```

2. **Test with Different Parameters:**
   - Try a different country:
     ```
     "country": "gb"  // UK news
     ```
   - Or use a category:
     ```
     "category": "technology"
     ```

3. **Check Data Availability:**
   - Some countries may not have news data
   - Try "us" or "gb" as a test
   - Visit https://newsapi.org/docs and test manually

4. **Verify Page Size:**
   - Ensure pageSize is between 1-100
   - Default is 20 (usually safe)

### 4. Workflow Not Running

#### Problem: "Scheduled Workflow Never Executes"

**Symptoms:**
- Schedule trigger is set up
- But workflow doesn't run at scheduled times
- Executions tab shows nothing new

**Solutions:**

1. **Check if Workflow is Active:**
   - Look for the **Activate** toggle at top-right
   - It should be **ON** (blue/green)
   - Click it to turn on if off

2. **Verify n8n is Running:**
   - Check if n8n service is active
   - For Docker:
     ```bash
     docker ps | grep n8n
     # Should show a running container
     ```
   - For npm:
     ```bash
     ps aux | grep n8n
     ```

3. **Check n8n Logs:**
   - Look for errors in n8n startup logs
   - If using Docker:
     ```bash
     docker logs n8n
     ```
   - Check for "workflow scheduled" messages

4. **Verify System Time:**
   - n8n schedules depend on correct system time
   - Ensure your server/computer has correct time
   - Resync time if needed:
     ```bash
     ntpdate -s time.nist.gov  # Linux
     ```

5. **Test Manual Execution:**
   - Click **Test Workflow** button to test immediately
   - If manual test fails, fix the issue before worrying about scheduling

### 5. Slack Integration Issues

#### Problem: "Messages Not Appearing in Slack"

**Symptoms:**
- Workflow runs successfully
- But messages don't appear in Slack
- No error message shown

**Solutions:**

1. **Enable Slack Node:**
   - Click **Send to Slack** node
   - Ensure the **toggle switch** is ON (not disabled)

2. **Verify Credentials:**
   - Click the **Send to Slack** node
   - Check credentials are configured
   - Test the connection

3. **Check Channel Name:**
   - Verify channel name is correct:
     ```
     #trending-news    // ✓ Correct
     trending-news     // May work or fail (depends on Slack)
     #general          // Built-in channels are OK
     ```

4. **Check Bot Permissions:**
   - Ensure bot has permission to post to channel
   - In Slack, go to channel settings
   - Check bot is a member of the channel
   - Check bot has message posting permissions

5. **Test Message Format:**
   - In the node, check the message text
   - Ensure it's not empty
   - Slack formatting should be:
     ```
     **Bold text** = _italic_
     <URL|Link Text>
     ```

### 6. Google Sheets Integration Issues

#### Problem: "Data Not Appearing in Google Sheets"

**Symptoms:**
- Workflow runs without errors
- But data doesn't appear in Sheets
- Sheets tab is enabled

**Solutions:**

1. **Enable Sheets Node:**
   - Click **Append to Google Sheets** node
   - Toggle should be ON

2. **Verify Google Authentication:**
   - Click the node
   - Check credentials are connected
   - If not, click **Connect** and authorize with Google

3. **Check Spreadsheet & Sheet:**
   - Verify spreadsheet ID is correct
   - Verify sheet name exists and is spelled correctly
   - Ensure bot has edit permission to sheet
   - Share sheet with the service account email if needed

4. **Verify Column Mapping:**
   - Check columns configuration:
     ```json
     {
       "header": "Title",
       "key": "title"
     }
     ```
   - `header` = Column name in Sheet
   - `key` = Field name from article data

5. **Check Data Structure:**
   - Ensure data matches expected columns
   - Missing fields will create empty cells
   - That's OK, but verify data is being processed

6. **Test Sheet Access:**
   - Manually add a row to the sheet
   - Edit workflow with test data
   - Click "Test step" to verify connection

### 7. Data Transformation Issues

#### Problem: "Incorrect or Missing Data in Output"

**Symptoms:**
- Articles are fetched but data is wrong
- Fields are empty or have wrong values
- Data structure is incorrect

**Solutions:**

1. **Check Transform Node:**
   - Click **Transform Article Data** node
   - Review the expression:
     ```javascript
     =={
       "title": $json.article.title,
       "source": $json.article.source.name
     }
     ```

2. **Verify JSON Path:**
   - Article data might be at different level
   - Check actual data structure:
     - Is it `$json.title` or `$json.article.title`?
   - Click "Test step" to see actual structure

3. **Handle Missing Fields:**
   - Some fields might be null/undefined
   - Add fallback values:
     ```javascript
     "author": $json.author || "Unknown"
     ```

4. **Check Code Node:**
   - Click **Process Articles** node
   - Review JavaScript logic
   - Add console.log for debugging:
     ```javascript
     console.log("Processing:", $json.title);
     return items;
     ```

### 8. Webhook Delivery Issues

#### Problem: "Webhook Not Receiving Data"

**Symptoms:**
- Workflow runs without error
- But webhook endpoint doesn't receive data
- Webhook node shows success but nothing arrives

**Solutions:**

1. **Verify Webhook URL:**
   - Ensure URL is correct and accessible
   - Test URL in browser or with curl:
     ```bash
     curl -X POST https://your-webhook.com/endpoint \
       -H "Content-Type: application/json" \
       -d '{"test": "data"}'
     ```

2. **Check Firewall/Network:**
   - Ensure n8n can reach your webhook
   - If n8n is in Docker, check network settings
   - Webhooks must be publicly accessible

3. **Verify HTTP Method:**
   - Ensure webhook is using POST
   - Check your endpoint expects POST
   - Some endpoints require GET

4. **Check Response Status:**
   - Webhook endpoint must return 200-299 status
   - If returning error, n8n might retry or fail
   - Add error handling in your endpoint

5. **Enable Node:**
   - Toggle **Send to Webhook** node to ON

6. **Review Payload:**
   - Click the node and check the body
   - Ensure data is being sent
   - Test with webhook.site temporarily:
     ```
     https://webhook.site/your-unique-id
     ```

### 9. Performance Issues

#### Problem: "Workflow Runs Very Slowly"

**Symptoms:**
- Workflow takes more than 30 seconds
- Articles take long time to process
- System seems unresponsive

**Solutions:**

1. **Reduce Page Size:**
   - Change `pageSize` from 20 to 10:
     ```json
     "pageSize": "10"
     ```
   - Less data = faster processing

2. **Simplify Processing:**
   - Remove unnecessary filtering
   - Disable Google Sheets integration temporarily
   - Remove custom code node

3. **Check System Resources:**
   - For Docker:
     ```bash
     docker stats n8n
     # Check CPU and memory usage
     ```
   - Increase container limits if needed

4. **Optimize Code Node:**
   - Avoid complex nested loops
   - Use efficient JavaScript:
     ```javascript
     // Good
     return items.map(item => ({...item.json}));

     // Avoid
     for (let i = 0; i < items.length; i++) {
       // Complex nested loops
     }
     ```

### 10. Credential Issues

#### Problem: "Credentials Not Found" or "Credential Missing"

**Symptoms:**
- Error: "Credential not found"
- Error: "Credential is undefined"
- Node can't authenticate

**Solutions:**

1. **Recreate Credential:**
   - Click on the node
   - Remove existing credential
   - Click **Create New Credential**
   - Re-enter the API key/token

2. **Check Credential Scope:**
   - n8n credentials are sometimes workspace-specific
   - Ensure you're in the right workspace

3. **Verify Credential Type:**
   - Ensure credential type matches node
   - NewsAPI = Generic/News API type
   - Slack = Slack credential type

4. **Restart n8n:**
   - Sometimes credential cache gets corrupted
   - Restart n8n service
   - For Docker:
     ```bash
     docker restart n8n
     ```

## Getting Help

### Debug Checklist

Before seeking help, verify:
- [ ] API key is valid
- [ ] Workflow is active
- [ ] Schedule trigger is configured
- [ ] At least one test execution succeeded
- [ ] Check error message carefully
- [ ] Review logs in Executions tab
- [ ] Try disabling optional nodes (Slack, Sheets, Webhook)
- [ ] Test with default configuration

### Resources

- **n8n Community:** https://community.n8n.io
- **NewsAPI Support:** https://newsapi.org/support
- **This Repository Issues:** Create an issue with details
- **n8n Docs:** https://docs.n8n.io

### Information to Provide When Getting Help

1. Error message (exact text)
2. Workflow name and nodes involved
3. What you were trying to do
4. Steps you've already tried
5. Screenshots of configuration if helpful
6. n8n version
7. Operating system

## Prevention Tips

1. **Always Test First:**
   - Test individual nodes before activating
   - Use "Test step" frequently

2. **Start Simple:**
   - Begin with just NewsAPI node
   - Add features one at a time
   - Test after each addition

3. **Monitor Regularly:**
   - Check executions tab weekly
   - Look for failed runs
   - Address issues immediately

4. **Keep Documentation:**
   - Document your customizations
   - Keep notes on changes made
   - Makes troubleshooting easier

5. **Backup Configuration:**
   - Export workflow regularly
   - Keep credentials noted somewhere safe (encrypted)
   - Can quickly restore if needed
