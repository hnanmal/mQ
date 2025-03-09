// document.getElementById("fetchProperties").addEventListener("click", async () => {
//     console.log("[popup.js] 버튼 클릭됨 - 메시지 전송 시작");

//     let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

//     chrome.scripting.executeScript({
//         target: { tabId: tab.id },
//         function: () => {
//             console.log("[popup.js] content.js로 메시지 전송 중...");
//             window.postMessage({ action: "fetchProperties" }, "*");
//         }
//     });

//     console.log("[popup.js] 메시지 전송 완료");
// });
document.getElementById("fetchProperties").addEventListener("click", async () => {
    console.log("[popup.js] 버튼 클릭됨 - content.js로 메시지 전송");

    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: () => {
            console.log("[popup.js] MAIN world에서 window.postMessage 실행");
            window.postMessage({ action: "fetchProperties" }, "*");
        },
        world: "MAIN"  // 이 옵션을 추가합니다.
    });
    console.log("[popup.js] 메시지 전송 완료");
});


// popup.js가 content.js로부터 메시지를 받아 UI 업데이트

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "displayProperties") {
        // 새 창을 열어서 결과를 출력합니다.
        const resultWindow = window.open("", "ACC_Properties", "width=800,height=600");
        resultWindow.document.write(`
            <html>
            <head>
                <title>객체 속성 결과</title>
                <style>
                    body { font-family: Arial, sans-serif; padding: 20px; }
                    pre { font-size: 14px; background: #f7f7f7; padding: 10px; border: 1px solid #ddd; }
                </style>
            </head>
            <body>
                <h2>선택된 객체 속성</h2>
                <pre>${message.data}</pre>
            </body>
            </html>
        `);
    }
});
