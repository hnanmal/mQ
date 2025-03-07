console.log("[content.js] 🚀 실행됨");

let fileUrl = chrome.runtime.getURL("inject.js");
console.log("[content.js] inject.js URL:", fileUrl);

// popup.js에서 메시지를 받았을 때 로그 출력
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log("[content.js] popup.js로부터 메시지 수신:", message);
    if (message.action === "fetchProperties") {
        console.log("[content.js] inject.js로 메시지 전달 시작");
        window.postMessage({ action: "fetchProperties" }, "*");
        console.log("[content.js] window.postMessage 실행 완료");
    }
});

window.addEventListener("message", (event) => {
    // event.source가 window인지 확인하여, 메인 세계에서 보낸 메시지인지 확인
    if (event.source !== window || !event.data || !event.data.action) {
      return;
    }
    
    if (event.data.action === "fetchProperties") {
      console.log("[content.js] MAIN world로부터 fetchProperties 메시지 수신:", event.data);
      // 이곳에서 inject.js로 메시지를 전달할 필요가 있으면 (예: window.postMessage 다시 전송)
      // 아니면 inject.js 자체가 메인 세계에 주입되어 있으므로, 직접 처리하게 할 수도 있습니다.
    } else if (event.data.action === "displayProperties") {
      console.log("[content.js] inject.js로부터 displayProperties 메시지 수신:", event.data);
      chrome.runtime.sendMessage(event.data);
    }
  });

  function injectScript(file) {
    let fileUrl = chrome.runtime.getURL(file);
    console.log("[content.js] inject.js URL:", fileUrl);
    let script = document.createElement("script");
    script.src = fileUrl;
    script.onload = function () {
        console.log("[content.js] inject.js 스크립트가 삽입되었습니다:", file);
        this.remove(); // 선택사항: 로드 후 스크립트를 제거
    };
    (document.head || document.documentElement).appendChild(script);
}

// inject.js 주입 시도
injectScript("inject.js");