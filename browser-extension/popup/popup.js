// OpenClaw Browser Extension - Popup Script

document.addEventListener('DOMContentLoaded', async () => {
    console.log('🦞 OpenClaw popup loaded');
    
    // Elements
    const gatewayStatus = document.getElementById('gateway-status');
    const serverStatus = document.getElementById('server-status');
    const attachedCount = document.getElementById('attached-count');
    const currentTabInfo = document.getElementById('current-tab-info');
    const tabUrl = document.getElementById('tab-url');
    const tabStatus = document.getElementById('tab-status');
    const attachBtn = document.getElementById('attach-btn');
    const detachBtn = document.getElementById('detach-btn');
    const captureCookiesBtn = document.getElementById('capture-cookies-btn');
    const openLoginBtn = document.getElementById('open-login-btn');
    const refreshBtn = document.getElementById('refresh-btn');
    const autoAttach = document.getElementById('auto-attach');
    const autoCapture = document.getElementById('auto-capture');
    const extensionVersion = document.getElementById('extension-version');
    
    // State
    let currentTab = null;
    let isAttached = false;
    let settings = {};
    
    // Initialize
    await loadSettings();
    await updateCurrentTab();
    await checkGateway();
    await checkLoginServer();
    updateAttachedCount();
    
    // Event Listeners
    attachBtn.addEventListener('click', attachCurrentTab);
    detachBtn.addEventListener('click', detachCurrentTab);
    captureCookiesBtn.addEventListener('click', captureCookies);
    openLoginBtn.addEventListener('click', openLoginPortal);
    refreshBtn.addEventListener('click', refreshAll);
    autoAttach.addEventListener('change', saveSettings);
    autoCapture.addEventListener('change', saveSettings);
    
    // Load settings
    async function loadSettings() {
        try {
            const result = await chrome.storage.local.get(['settings', 'version']);
            settings = result.settings || {
                autoAttach: false,
                captureCookies: true,
                logLevel: 'info'
            };
            
            autoAttach.checked = settings.autoAttach;
            autoCapture.checked = settings.captureCookies;
            
            if (result.version) {
                extensionVersion.textContent = `v${result.version}`;
            }
        } catch (error) {
            console.error('Error loading settings:', error);
        }
    }
    
    // Save settings
    async function saveSettings() {
        try {
            settings.autoAttach = autoAttach.checked;
            settings.captureCookies = autoCapture.checked;
            
            await chrome.storage.local.set({ settings });
            console.log('Settings saved:', settings);
        } catch (error) {
            console.error('Error saving settings:', error);
        }
    }
    
    // Get current tab
    async function updateCurrentTab() {
        try {
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
            currentTab = tab;
            
            if (tab) {
                currentTabInfo.classList.remove('hidden');
                tabUrl.textContent = tab.url || 'No URL';
                
                // Check if tab is attached
                const result = await chrome.runtime.sendMessage({ 
                    action: 'checkTabAttachment',
                    tabId: tab.id 
                }).catch(() => ({ attached: false }));
                
                isAttached = result.attached || false;
                updateAttachmentUI();
            } else {
                currentTabInfo.classList.add('hidden');
            }
        } catch (error) {
            console.error('Error getting current tab:', error);
        }
    }
    
    // Update attachment UI
    function updateAttachmentUI() {
        if (isAttached) {
            tabStatus.innerHTML = '<span class="attached-badge">🔗 Attached</span>';
            attachBtn.classList.add('hidden');
            detachBtn.classList.remove('hidden');
        } else {
            tabStatus.innerHTML = '<span class="detached-badge">🔗 Detached</span>';
            attachBtn.classList.remove('hidden');
            detachBtn.classList.add('hidden');
        }
    }
    
    // Attach current tab
    async function attachCurrentTab() {
        if (!currentTab) return;
        
        try {
            attachBtn.disabled = true;
            attachBtn.textContent = 'Attaching...';
            
            const result = await chrome.runtime.sendMessage({
                action: 'attachTab',
                tabId: currentTab.id
            });
            
            if (result.success) {
                isAttached = true;
                updateAttachmentUI();
                updateAttachedCount();
                
                // Auto-capture cookies if enabled
                if (settings.captureCookies) {
                    setTimeout(captureCookies, 1000);
                }
                
                showNotification('✅ Tab attached successfully');
            } else {
                showNotification('❌ Failed to attach tab', true);
            }
        } catch (error) {
            console.error('Error attaching tab:', error);
            showNotification('❌ Error attaching tab', true);
        } finally {
            attachBtn.disabled = false;
            attachBtn.textContent = '🔗 Attach Current Tab';
        }
    }
    
    // Detach current tab
    async function detachCurrentTab() {
        if (!currentTab) return;
        
        try {
            detachBtn.disabled = true;
            detachBtn.textContent = 'Detaching...';
            
            const result = await chrome.runtime.sendMessage({
                action: 'detachTab',
                tabId: currentTab.id
            });
            
            if (result.success) {
                isAttached = false;
                updateAttachmentUI();
                updateAttachedCount();
                showNotification('🔗 Tab detached');
            } else {
                showNotification('❌ Failed to detach tab', true);
            }
        } catch (error) {
            console.error('Error detaching tab:', error);
            showNotification('❌ Error detaching tab', true);
        } finally {
            detachBtn.disabled = false;
            detachBtn.textContent = '✂️ Detach Tab';
        }
    }
    
    // Capture cookies from current tab
    async function captureCookies() {
        if (!currentTab) return;
        
        try {
            captureCookiesBtn.disabled = true;
            captureCookiesBtn.textContent = 'Capturing...';
            
            const result = await chrome.runtime.sendMessage({
                action: 'getCookies',
                tabId: currentTab.id,
                domains: [
                    currentTab.url ? new URL(currentTab.url).hostname : null,
                    '.google.com',
                    'accounts.google.com',
                    'console.cloud.google.com'
                ].filter(Boolean)
            });
            
            if (result.cookies) {
                // Export to server
                const exportResult = await chrome.runtime.sendMessage({
                    action: 'exportCookies',
                    cookies: result.cookies,
                    tabId: currentTab.id
                });
                
                if (exportResult.success) {
                    showNotification(`✅ ${result.cookies.length} cookies captured and saved`);
                } else {
                    showNotification('⚠️ Cookies captured but export failed', true);
                }
            } else if (result.error) {
                showNotification(`❌ ${result.error}`, true);
            }
        } catch (error) {
            console.error('Error capturing cookies:', error);
            showNotification('❌ Error capturing cookies', true);
        } finally {
            captureCookiesBtn.disabled = false;
            captureCookiesBtn.textContent = '🍪 Capture Cookies';
        }
    }
    
    // Open login portal
    async function openLoginPortal() {
        try {
            await chrome.tabs.create({ url: 'http://localhost:8080' });
        } catch (error) {
            console.error('Error opening login portal:', error);
            showNotification('❌ Could not open login portal', true);
        }
    }
    
    // Refresh all status
    async function refreshAll() {
        refreshBtn.disabled = true;
        refreshBtn.textContent = 'Refreshing...';
        
        await Promise.all([
            updateCurrentTab(),
            checkGateway(),
            checkLoginServer(),
            updateAttachedCount()
        ]);
        
        refreshBtn.disabled = false;
        refreshBtn.textContent = '🔄 Refresh Status';
    }
    
    // Check OpenClaw gateway
    async function checkGateway() {
        try {
            const result = await chrome.runtime.sendMessage({ action: 'checkGateway' });
            
            if (result.connected) {
                gatewayStatus.textContent = 'Connected';
                gatewayStatus.className = 'status-value connected';
            } else if (result.error) {
                gatewayStatus.textContent = 'Error';
                gatewayStatus.className = 'status-value disconnected';
            } else {
                gatewayStatus.textContent = 'Disconnected';
                gatewayStatus.className = 'status-value disconnected';
            }
        } catch (error) {
            gatewayStatus.textContent = 'Error';
            gatewayStatus.className = 'status-value disconnected';
        }
    }
    
    // Check login server
    async function checkLoginServer() {
        try {
            const response = await fetch('http://localhost:8080/health');
            if (response.ok) {
                serverStatus.textContent = 'Connected';
                serverStatus.className = 'status-value connected';
            } else {
                serverStatus.textContent = 'Disconnected';
                serverStatus.className = 'status-value disconnected';
            }
        } catch (error) {
            serverStatus.textContent = 'Disconnected';
            serverStatus.className = 'status-value disconnected';
        }
    }
    
    // Update attached tab count
    async function updateAttachedCount() {
        try {
            // Get all tabs
            const tabs = await chrome.tabs.query({});
            
            // Check attachment for each tab
            let attached = 0;
            for (const tab of tabs) {
                try {
                    const result = await chrome.runtime.sendMessage({ 
                        action: 'checkTabAttachment',
                        tabId: tab.id 
                    }).catch(() => ({ attached: false }));
                    
                    if (result.attached) attached++;
                } catch (error) {
                    // Tab may not be accessible
                }
            }
            
            attachedCount.textContent = attached;
        } catch (error) {
            console.error('Error counting attached tabs:', error);
            attachedCount.textContent = '?';
        }
    }
    
    // Show notification
    function showNotification(message, isError = false) {
        // Create notification element
        const notification = document.createElement('div');
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            background: ${isError ? '#ea4335' : '#0f9d58'};
            color: white;
            border-radius: 8px;
            z-index: 1000;
            font-size: 14px;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
    
    // Add CSS for animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
    `;
    document.head.appendChild(style);
    
    // Auto-refresh every 10 seconds
    setInterval(refreshAll, 10000);
});