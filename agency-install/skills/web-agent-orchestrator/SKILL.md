---
name: web-agent-orchestrator
description: Use authenticated browser sessions (via Camoufox) to act as an agent on websites mentioned in chat, leveraging Fiesta Agents for orchestration. Use when you need to perform web-based tasks using existing session cookies (e.g., Gmail, social media, internal portals) and coordinate multiple specialized agents for complex web interactions.
version: 1.0.0
author: Fiesta
license: MIT
tags: [web, browser, automation, orchestration, fiesta-agents, camoufox]
---

# Web Agent Orchestrator

This skill enables you to use authenticated browser sessions (via Camoufox) to act as an AI agent on websites. It leverages your existing session cookies (e.g., from Gmail authentication) and orchestrates tasks using Fiesta Agents for complex workflows.

## 🎯 Usage

### Single Website Task

Tell the agent which website to interact with and what to do:

```
Use the web-agent-orchestrator to check my Gmail inbox for unread messages from the last 24 hours
```

The skill will load the Camoufox browser with your session cookies, navigate to the site, and perform the requested task.

### Orchestrated Multi-Site Workflow

For complex projects spanning multiple websites:

```
Use the web-agent-orchestrator to:
1. Check GitHub for open issues in the agency-agents repository
2. Post a summary to the agency Twitter account
3. Update the project status in the internal dashboard
```

The orchestrator breaks the project into tasks, assigns appropriate Fiesta Agents (e.g., github-issue-reader, twitter-poster, dashboard-updater), runs them sequentially, and delivers a unified result.

### Department Mode

Activate an entire department of web specialists:

```
Use the web-engineering department to audit and improve the agency's public-facing websites
```

## 🚀 How It Works

1. **Session Recovery**: The skill reads your existing browser session cookies (stored via `gog auth` and Camoufox) to authenticate to websites without re-login.
2. **Camoufox Integration**: Uses the Camoufox browser (configured as the default for OpenClaw) for all web interactions, ensuring privacy and anti-fingerprinting.
3. **Fiesta Agents Orchestration**: For multi-step tasks, the skill delegates to specialized Fiesta Agents:
   - `web-navigator` - Handles site navigation and element interaction
   - `form-filler` - Automates form submissions and data entry
   - `data-extractor` - Scrapes and structures information from pages
   - `content-poster` - Creates and publishes content (tweets, posts, comments)
   - `status-monitor` - Checks for updates, notifications, and system health
4. **Error Handling**: Built-in retry logic with exponential backoff for transient failures (network, rate limits).

## 📋 Supported Websites

The skill works with any website where you have an active session, including but not limited to:
- Gmail (mail.google.com)
- Google Workspace (drive.google.com, calendar.google.com)
- GitHub (github.com)
- Twitter/X (twitter.com, x.com)
- Reddit (reddit.com)
- Internal agency portals
- Any site where session cookies are preserved

## 🔧 Configuration

### Environment Variables

```bash
# Set default timeout for web interactions (seconds)
WEB_AGENT_ORCHESTRATOR_TIMEOUT=30

# Enable verbose logging for debugging
WEB_AGENT_ORCHESTRATOR_VERBOSE=true

# Set maximum retry attempts for failed requests
WEB_AGENT_ORCHESTRATOR_MAX_RETRIES=3
```

### Cookie Persistence

Session cookies are automatically managed by:
- `gog auth` for Google services
- Browser storage for other sites
- The skill reads from the Camoufox profile directory

## 📖 Examples

### Example 1: Check Gmail

```
Use the web-agent-orchestrator to:
  Open Gmail
  Search for unread messages from @agency-agents
  Return the count and subjects of the top 5 messages
```

### Example 2: Twitter Post with Image

```
Use the web-agent-orchestrator to:
  Log into Twitter/X
  Upload the attached image
  Compose a tweet: "Agency update: All systems operational. #ShannonEconomy"
  Schedule the tweet for peak engagement time
```

### Example 3: Multi-Site Orchestration

```
Use the web-agent-orchestrator orchestrator to:
  1. Fetch latest commit from deception-floor-commodity-factory repo
  2. Extract key changes from the commit message
  3. Post a summary to the agency Twitter account
  4. Log the activity to the internal Notion dashboard
  5. Send a confirmation email to the team lead
```

## 🛠️ Troubleshooting

### Common Issues

**Q: I'm being redirected to login pages despite having session cookies**
A: The session may have expired. Re-authenticate using:
```bash
gog auth add ironiclawdoctor@gmail.com --services gmail,calendar,drive
```
Then refresh your browser session.

**Q: The skill reports "element not found" on a website**
A: Websites change frequently. Try:
1. Increasing the timeout: `WEB_AGENT_ORCHESTRATOR_TIMEOUT=60`
2. Using more specific selectors in your task description
3. Checking if the site requires additional permissions

**Q: I get rate-limited errors (429)**
A: The skill automatically respects rate limits. You can:
1. Increase delay between actions: Add "wait 2 seconds between steps" to your task
2. Reduce frequency of requests
3. Wait for the rate limit window to reset

### Debugging

Enable verbose logging to see detailed browser interactions:
```bash
export WEB_AGENT_ORCHESTRATOR_VERBOSE=true
```

## 🔄 Integration with Other Skills

This skill works seamlessly with:
- `twitter-posts` - For automated Twitter/X publishing
- `gog` - For Google Workspace authentication and operations
- `github` - For GitHub issue and PR management
- `fiesta-agents` - For accessing specialized agents (frontend-developer, growth-hacker, etc.)

## 📈 Best Practices

1. **Be Specific**: Clearly define what you want the agent to do on the website (e.g., "click the 'Compose' button" vs "write an email").
2. **Chain Actions**: Break complex tasks into sequential steps for better reliability.
3. **Leverage Orchestration**: Use the orchestrator for multi-site workflows to ensure proper error handling and resource allocation.
4. **Monitor Sessions**: Periodically re-authenticate critical services (especially Gmail) to maintain access.
5. **Respect Rate Limits**: The skill includes built-in throttling, but be mindful of aggressive scraping or posting frequencies.

## 📞 Support

- 📧 Email: support@agency-agents.xyz
- 💬 Discord: Join the agency agents channel
- 📚 Documentation: Full guides in the references/ directory

## 📄 License

MIT License - Feel free to modify and extend this skill for your agency's needs.
