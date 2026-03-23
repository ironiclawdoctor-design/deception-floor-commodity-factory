// OpenClaw Browser Extension - Background Service Worker
// Agency-only browser automation and session management

console.log('🦞 OpenClaw Browser Extension loaded');

// Configuration
const OPENCLAW_GATEWAY = 'http://localhost:18792'; // Default CDP proxy port
const LOGIN_SERVER = 'http://localhost:8080';
const EXTENSION_VERSION = '1.0.0';

// State
let attachedTabs = new Set();
let gatewayConnected = false;

// Initialize
chrome.runtime.onInstalled.addListener((details) => {
  console.log(`OpenClaw extension ${details.reason} (v${EXTENSION_VERSION})`);
  
  if (details.reason === 'install') {
    // First install - setup
    chrome.storage.local.set({
      installed: new Date().toISOString(),
      version: EXTENSION_VERSION,
      settings: {
        autoAttach: false,
        captureCookies: true,
        logLevel: 'info'
      }
    });
    
    // Open welcome page
    chrome.tabs.create({ url: `${LOGIN_SERVER}/` });
  }
});

// Handle tab updates
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    // Auto-attach to Google Cloud Console if enabled
    if (tab.url.includes('console.cloud.google.com')) {
      chrome.storage.local.get(['settings'], (result) => {
        if (result.settings?.autoAttach) {
          attachTab(tabId);
        }
      });
    }
  }
});

// Message handling
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('Extension message:', message);
  
  switch (message.action) {
    case 'attachTab':
      attachTab(message.tabId || sender.tab?.id);
      sendResponse({ success: true });
      break;
      
    case 'detachTab':
      detachTab(message.tabId);
      sendResponse({ success: true });
      break;
      
    case 'getCookies':
      getTabCookies(message.tabId || sender.tab?.id, message.domains)
        .then(cookies => sendResponse({ cookies }))
        .catch(error => sendResponse({ error: error.message }));
      return true; // Async response
      
    case 'exportCookies':
      exportCookiesToServer(message.cookies, message.tabId)
        .then(result => sendResponse(result))
        .catch(error => sendResponse({ error: error.message }));
      return true;
      
    case 'checkGateway':
      checkGatewayConnection()
        .then(connected => sendResponse({ connected }))
        .catch(error => sendResponse({ error: error.message }));
      return true;
      
    default:
      sendResponse({ error: `Unknown action: ${message.action}` });
  }
});

// Tab attachment
async function attachTab(tabId) {
  try {
    // Inject content script
    await chrome.scripting.executeScript({
      target: { tabId },
      files: ['content/tab-attacher.js']
    });
    
    attachedTabs.add(tabId);
    
    // Update badge
    chrome.action.setBadgeText({ tabId, text: '🔗' });
    chrome.action.setBadgeBackgroundColor({ tabId, color: '#0f9d58' });
    
    console.log(`✅ Tab ${tabId} attached`);
    
    // Notify content script
    chrome.tabs.sendMessage(tabId, { 
      action: 'tabAttached',
      timestamp: new Date().toISOString()
    });
    
    return true;
  } catch (error) {
    console.error(`❌ Failed to attach tab ${tabId}:`, error);
    return false;
  }
}

// Tab detachment
async function detachTab(tabId) {
  attachedTabs.delete(tabId);
  chrome.action.setBadgeText({ tabId, text: '' });
  
  try {
    chrome.tabs.sendMessage(tabId, { 
      action: 'tabDetached',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    // Tab may have been closed
  }
  
  console.log(`🔗 Tab ${tabId} detached`);
}

// Get cookies for tab domains
async function getTabCookies(tabId, specificDomains = null) {
  try {
    const tab = await chrome.tabs.get(tabId);
    if (!tab?.url) throw new Error('Tab URL not available');
    
    const url = new URL(tab.url);
    const domains = specificDomains || [
      url.hostname,
      `.${url.hostname}`,
      'google.com',
      '.google.com',
      'accounts.google.com'
    ];
    
    const cookies = [];
    
    for (const domain of domains) {
      try {
        const domainCookies = await chrome.cookies.getAll({ domain });
        cookies.push(...domainCookies.map(c => ({
          name: c.name,
          value: c.value,
          domain: c.domain,
          path: c.path,
          secure: c.secure,
          httpOnly: c.httpOnly,
          sameSite: c.sameSite,
          expirationDate: c.expirationDate
        })));
      } catch (error) {
        console.warn(`Could not get cookies for domain ${domain}:`, error);
      }
    }
    
    return cookies;
  } catch (error) {
    console.error('Error getting cookies:', error);
    throw error;
  }
}

// Export cookies to login server
async function exportCookiesToServer(cookies, tabId) {
  try {
    const response = await fetch(`${LOGIN_SERVER}/upload-cookies`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(cookies)
    });
    
    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }
    
    const result = await response.json();
    
    // Log successful export
    chrome.storage.local.get(['cookieExports'], (data) => {
      const exports = data.cookieExports || [];
      exports.push({
        timestamp: new Date().toISOString(),
        tabId,
        count: cookies.length,
        success: true
      });
      chrome.storage.local.set({ cookieExports: exports });
    });
    
    return result;
  } catch (error) {
    console.error('Cookie export failed:', error);
    
    // Log failure
    chrome.storage.local.get(['cookieExports'], (data) => {
      const exports = data.cookieExports || [];
      exports.push({
        timestamp: new Date().toISOString(),
        tabId,
        error: error.message,
        success: false
      });
      chrome.storage.local.set({ cookieExports: exports });
    });
    
    throw error;
  }
}

// Check OpenClaw gateway connection
async function checkGatewayConnection() {
  try {
    const response = await fetch(`${OPENCLAW_GATEWAY}/json/version`, {
      method: 'GET',
      mode: 'no-cors' // CDP endpoints may not have CORS headers
    }).catch(() => null);
    
    // Even if fetch fails, try WebSocket
    const ws = new WebSocket(`${OPENCLAW_GATEWAY.replace('http', 'ws')}/devtools`);
    
    return new Promise((resolve) => {
      ws.onopen = () => {
        ws.close();
        gatewayConnected = true;
        resolve(true);
      };
      
      ws.onerror = () => {
        gatewayConnected = false;
        resolve(false);
      };
      
      setTimeout(() => {
        gatewayConnected = false;
        resolve(false);
      }, 1000);
    });
  } catch (error) {
    gatewayConnected = false;
    return false;
  }
}

// Periodic gateway check
setInterval(() => {
  checkGatewayConnection().then(connected => {
    if (connected !== gatewayConnected) {
      gatewayConnected = connected;
      console.log(`Gateway ${connected ? 'connected' : 'disconnected'}`);
    }
  });
}, 30000);

// Export for testing
if (typeof module !== 'undefined') {
  module.exports = {
    attachTab,
    detachTab,
    getTabCookies,
    exportCookiesToServer,
    checkGatewayConnection
  };
}