// OpenClaw Tab Attacher - Content Script
// Injected into attached tabs for communication and automation

console.log('🦞 OpenClaw Tab Attacher loaded');

// State
let isAttached = false;
let gatewayConnection = null;
let heartbeatInterval = null;

// Listen for messages from background script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log('Content script message:', message);
    
    switch (message.action) {
        case 'tabAttached':
            handleTabAttached(message);
            sendResponse({ success: true });
            break;
            
        case 'tabDetached':
            handleTabDetached(message);
            sendResponse({ success: true });
            break;
            
        case 'executeScript':
            executeScript(message.script)
                .then(result => sendResponse({ result }))
                .catch(error => sendResponse({ error: error.message }));
            return true;
            
        case 'getPageInfo':
            sendResponse({
                url: window.location.href,
                title: document.title,
                domain: window.location.hostname,
                timestamp: new Date().toISOString()
            });
            break;
            
        default:
            sendResponse({ error: `Unknown action: ${message.action}` });
    }
});

// Handle tab attachment
function handleTabAttached(message) {
    if (isAttached) {
        console.warn('Tab already attached');
        return;
    }
    
    isAttached = true;
    console.log('✅ Tab attached at', message.timestamp);
    
    // Update page title to show attachment
    const originalTitle = document.title;
    if (!document.title.includes('🦞')) {
        document.title = `🦞 ${document.title}`;
    }
    
    // Start heartbeat to background script
    heartbeatInterval = setInterval(() => {
        chrome.runtime.sendMessage({
            action: 'heartbeat',
            tabId: chrome.devtools.inspectedWindow.tabId,
            url: window.location.href,
            timestamp: new Date().toISOString()
        }).catch(error => {
            console.warn('Heartbeat failed:', error);
            // Tab may have been detached
            if (heartbeatInterval) {
                clearInterval(heartbeatInterval);
                heartbeatInterval = null;
            }
        });
    }, 30000);
    
    // Inject OpenClaw overlay
    injectOverlay();
    
    // Notify page of attachment
    window.dispatchEvent(new CustomEvent('openclaw:tabAttached', {
        detail: { timestamp: message.timestamp }
    }));
}

// Handle tab detachment
function handleTabDetached(message) {
    if (!isAttached) {
        console.warn('Tab not attached');
        return;
    }
    
    isAttached = false;
    console.log('🔗 Tab detached at', message.timestamp);
    
    // Restore original title
    if (document.title.startsWith('🦞 ')) {
        document.title = document.title.substring(2);
    }
    
    // Clear heartbeat
    if (heartbeatInterval) {
        clearInterval(heartbeatInterval);
        heartbeatInterval = null;
    }
    
    // Remove overlay
    removeOverlay();
    
    // Notify page of detachment
    window.dispatchEvent(new CustomEvent('openclaw:tabDetached', {
        detail: { timestamp: message.timestamp }
    }));
}

// Inject OpenClaw overlay
function injectOverlay() {
    // Create overlay element
    const overlay = document.createElement('div');
    overlay.id = 'openclaw-overlay';
    overlay.style.cssText = `
        position: fixed;
        top: 10px;
        right: 10px;
        background: rgba(15, 157, 88, 0.9);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        z-index: 999999;
        display: flex;
        align-items: center;
        gap: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        pointer-events: none;
    `;
    
    overlay.innerHTML = `
        <span>🦞</span>
        <span>OpenClaw Attached</span>
    `;
    
    document.body.appendChild(overlay);
    
    // Add CSS for animations
    const style = document.createElement('style');
    style.id = 'openclaw-styles';
    style.textContent = `
        @keyframes openclawPulse {
            0% { opacity: 0.7; }
            50% { opacity: 1; }
            100% { opacity: 0.7; }
        }
        
        #openclaw-overlay {
            animation: openclawPulse 2s infinite;
        }
        
        .openclaw-highlight {
            outline: 2px solid #0f9d58 !important;
            outline-offset: 2px;
            transition: outline 0.3s ease;
        }
    `;
    
    document.head.appendChild(style);
}

// Remove overlay
function removeOverlay() {
    const overlay = document.getElementById('openclaw-overlay');
    if (overlay) overlay.remove();
    
    const styles = document.getElementById('openclaw-styles');
    if (styles) styles.remove();
}

// Execute script in page context
async function executeScript(script) {
    try {
        // Create a function from the script
        const func = new Function(script);
        
        // Execute in page context
        const result = func();
        
        // If it's a promise, await it
        if (result && typeof result.then === 'function') {
            return await result;
        }
        
        return result;
    } catch (error) {
        console.error('Script execution error:', error);
        throw error;
    }
}

// Monitor page changes
let lastUrl = window.location.href;
const observer = new MutationObserver(() => {
    if (window.location.href !== lastUrl) {
        lastUrl = window.location.href;
        
        // Notify background of URL change
        if (isAttached) {
            chrome.runtime.sendMessage({
                action: 'urlChanged',
                tabId: chrome.devtools.inspectedWindow.tabId,
                url: window.location.href,
                timestamp: new Date().toISOString()
            }).catch(() => {
                // Background may not be listening
            });
        }
    }
});

observer.observe(document, { subtree: true, childList: true });

// Handle page unload
window.addEventListener('beforeunload', () => {
    if (isAttached) {
        // Try to notify background before page unloads
        chrome.runtime.sendMessage({
            action: 'pageUnloading',
            tabId: chrome.devtools.inspectedWindow.tabId,
            url: window.location.href,
            timestamp: new Date().toISOString()
        }).catch(() => {
            // Background may not be reachable during unload
        });
    }
});

// Export for debugging
if (typeof window !== 'undefined') {
    window.__openclawTabAttacher = {
        isAttached: () => isAttached,
        version: '1.0.0'
    };
}