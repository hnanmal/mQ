console.log("[inject.js] 🚀 실행됨");

// 메인 세계에서 메시지를 수신합니다.
window.addEventListener("message", (event) => {
    if (event.source !== window || !event.data || !event.data.action) return;
    if (event.data.action === "fetchProperties") {
        console.log("[inject.js] fetchProperties 메시지 수신");
        getSelectedObjectProperties();
    } else if (event.data.action === "fetchFamilyTypes") {
        console.log("[inject.js] fetchFamilyTypes 메시지 수신");
        getFamilyTypesByCategory();
    }
});

// ACC에서는 NOP_VIEWER가 실제 Viewer 인스턴스일 가능성이 높습니다.
function getViewerInstance() {
    console.log("[inject.js] Viewer 인스턴스 요청");
    if (window.NOP_VIEWER && typeof window.NOP_VIEWER.getSelection === "function") {
        return window.NOP_VIEWER;
    } else if (Autodesk && Autodesk.Viewing && Autodesk.Viewing.Viewer3D &&
               Autodesk.Viewing.Viewer3D.instances && Autodesk.Viewing.Viewer3D.instances.length > 0) {
        return Autodesk.Viewing.Viewer3D.instances[0];
    } else {
        console.error("[inject.js] Viewer 인스턴스를 찾을 수 없습니다!");
        return null;
    }
}

// 기존 기능: 선택된 객체의 속성 가져오기
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

// 업그레이드 기능: 전체 모델 요소에서 카테고리별 패밀리 타입(또는 타입 이름)을 그룹화 및 정렬
function getFamilyTypesByCategory() {
    let viewer = getViewerInstance();
    if (!viewer) {
        console.error("[inject.js] 🚨 Viewer 인스턴스 없음");
        return;
    }
    
    let instanceTree = viewer.model.getData().instanceTree;
    let allDbIds = [];
    instanceTree.enumNodeChildren(instanceTree.getRootId(), function(dbId) {
        allDbIds.push(dbId);
    }, true);
    
    console.log("[inject.js] 수집된 dbIds 개수:", allDbIds.length);
    
    // Bulk Properties API를 사용하여 각 요소의 "Category", "Type Name", "Family" 속성을 가져옵니다.
    viewer.model.getBulkProperties(allDbIds, ["Category", "Type Name", "Family"], function(results) {
        let grouped = {}; // { category: Set(타입 이름들) }
        results.forEach(result => {
            let category = "";
            let typeName = "";
            result.properties.forEach(prop => {
                if (prop.displayName === "Category") {
                    category = prop.displayValue;
                } else if (prop.displayName === "Type Name") {
                    typeName = prop.displayValue;
                } else if (prop.displayName === "Family" && !typeName) {
                    typeName = prop.displayValue;
                }
            });
            if (category && typeName) {
                if (!grouped[category]) {
                    grouped[category] = new Set();
                }
                grouped[category].add(typeName);
            }
        });
        
        let output = "";
        for (let cat in grouped) {
            let types = Array.from(grouped[cat]).sort();
            output += `Category: ${cat}\n`;
            types.forEach(t => {
                output += `   ${t}\n`;
            });
            output += "\n";
        }
        
        console.log("[inject.js] Grouped Family Types:\n", output);
        window.postMessage({ action: "displayProperties", data: output }, "*");
    });
}
