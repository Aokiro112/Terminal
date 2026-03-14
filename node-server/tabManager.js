class TabManager {
    constructor() {
        this.tabs = new Map();
        this.activeTab = null;
    }

    createTab(id = null) {
        const tabId = id || `tab_${Date.now()}`;
        this.tabs.set(tabId, {
            id: tabId,
            history: [],
            cwd: "~",
            created: new Date()
        });
        this.activeTab = tabId;
        return tabId;
    }

    getTab(tabId) {
        return this.tabs.get(tabId);
    }

    getAllTabs() {
        return Array.from(this.tabs.values());
    }

    closeTab(tabId) {
        this.tabs.delete(tabId);
        if (this.activeTab === tabId) {
            const remaining = this.getAllTabs();
            this.activeTab = remaining.length ? remaining[0].id : null;
        }
    }

    addToHistory(tabId, cmd, result) {
        const tab = this.tabs.get(tabId);
        if (tab) tab.history.push({ cmd, result, time: new Date() });
    }
}

module.exports = new TabManager();