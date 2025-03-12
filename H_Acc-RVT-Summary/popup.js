// fetchProperties 버튼 (기존 기능)
document.getElementById("fetchProperties").addEventListener("click", async () => {
    console.log("[popup.js] 버튼 클릭됨 - fetchProperties 메시지 전송");
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: () => {
            console.log("[popup.js] MAIN world에서 window.postMessage 실행 (fetchProperties)");
            window.postMessage({ action: "fetchProperties" }, "*");
        },
        world: "MAIN"
    });
});

// fetchFamilyTypes 버튼 (업그레이드 기능)
document.getElementById("fetchFamilyTypes").addEventListener("click", async () => {
    console.log("[popup.js] 버튼 클릭됨 - fetchFamilyTypes 메시지 전송");
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: () => {
            console.log("[popup.js] MAIN world에서 window.postMessage 실행 (fetchFamilyTypes)");
            window.postMessage({ action: "fetchFamilyTypes" }, "*");
        },
        world: "MAIN"
    });
});

// 새 기능: 룸 정보 가져오기
document.getElementById("fetchRooms").addEventListener("click", async () => {
    console.log("[popup.js] 버튼 클릭됨 - fetchRooms 메시지 전송");
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: () => {
            console.log("[popup.js] MAIN world에서 window.postMessage 실행 (fetchRooms)");
            window.postMessage({ action: "fetchRooms" }, "*");
        },
        world: "MAIN"
    });
});

// popup.js가 content.js로부터 결과 메시지를 받으면 새 창에 출력
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log("[popup.js] 메시지 수신:", message);
    if (message.action === "displayProperties") {
        let resultWindow = window.open("", "ACC_Result", "width=800,height=600");
        resultWindow.document.write(`
            <html>
            <head>
                <title>ACC 결과</title>
                <style>
                    body { font-family: Arial, sans-serif; padding: 20px; }
                    pre { font-size: 14px; background: #f7f7f7; padding: 10px; border: 1px solid #ddd; }
                </style>
            </head>
            <body>
                <h2>결과</h2>
                <pre>${message.data}</pre>
            </body>
            </html>
        `);
    }
});
