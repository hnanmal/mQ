chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "displayProperties") {
        chrome.storage.local.set({ lastData: message.data });
    }
});
