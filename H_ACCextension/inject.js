// inject.js
console.log("[inject.js] 🚀 실행됨");

// 메인 세계에서 "fetchProperties" 메시지를 수신하면 속성 가져오기 실행
window.addEventListener("message", (event) => {
    if (event.source !== window || !event.data || event.data.action !== "fetchProperties") {
        return;
    }
    console.log("[inject.js] content.js에서 메시지 수신 - fetchProperties", event.data);
    getSelectedObjectProperties();
});

// 현재 활성 뷰어 인스턴스를 가져오는 함수 (수정됨)
function getViewerInstance() {
    console.log("[inject.js] NOP_VIEWER 확인");
    if (window.NOP_VIEWER && typeof window.NOP_VIEWER.getSelection === "function") {
        return window.NOP_VIEWER;
    } else if (Autodesk.Viewing.Viewer3D.instances && Autodesk.Viewing.Viewer3D.instances.length > 0) {
        return Autodesk.Viewing.Viewer3D.instances[0];
    } else {
        console.error("[inject.js] Viewer 인스턴스를 찾을 수 없습니다!");
        return null;
    }
}


// 선택된 객체 속성 가져오기 함수
function getSelectedObjectProperties() {
    let viewer = getViewerInstance();
    if (!viewer) {
        console.error("[inject.js] 🚨 Viewer 인스턴스 없음");
        return;
    }
    
    console.log("[inject.js] Viewer 인스턴스 확인 완료");
    let selection = viewer.getSelection();
    if (!selection || selection.length === 0) {
        console.log("[inject.js] 선택된 객체가 없습니다.");
        return;
    }
    
    let dbId = selection[0];
    console.log("[inject.js] 선택된 객체 ID:", dbId);
    
    viewer.getProperties(dbId, (props) => {
        let output = "=== 선택된 객체 속성 ===\n";
        props.properties.forEach(prop => {
            output += `${prop.displayName}: ${prop.displayValue}\n`;
        });
        console.log("[inject.js] 속성 데이터 준비 완료");
        window.postMessage({ action: "displayProperties", data: output }, "*");
    });
}
