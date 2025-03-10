console.log("[content.js] 실행됨");

// inject.js를 페이지에 주입하는 함수
function injectScript(file) {
    let fileUrl = chrome.runtime.getURL(file);
    console.log("[content.js] inject.js URL:", fileUrl);
    let script = document.createElement("script");
    script.src = fileUrl;
    script.onload = function () {
        console.log("[content.js] inject.js 주입 완료:", file);
        this.remove();
    };
    (document.head || document.documentElement).appendChild(script);
}
injectScript("inject.js");

// 메인 세계에서 inject.js가 보내는 메시지를 수신하여 popup.js로 전달
window.addEventListener("message", (event) => {
    if (event.source !== window || !event.data || !event.data.action) return;
    if (event.data.action === "displayProperties") {
        console.log("[content.js] inject.js로부터 displayProperties 메시지 수신:", event.data);
        chrome.runtime.sendMessage(event.data);
    }
});

// popup.js에서 보내는 메시지를 메인 세계로 전달 (필요 시)
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log("[content.js] popup.js 메시지 수신:", message);
    if (message.action === "fetchProperties" || message.action === "fetchFamilyTypes") {
        window.postMessage(message, "*");
    }
});
