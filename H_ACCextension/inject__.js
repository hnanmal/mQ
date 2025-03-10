// inject.js
console.log("[inject.js] 🚀 실행됨");

// 메인 세계에서 전달되는 메시지를 수신합니다.
window.addEventListener("message", (event) => {
  if (event.source !== window || !event.data || !event.data.action) {
    return;
  }
  if (event.data.action === "fetchProperties") {
    console.log("[inject.js] content.js에서 메시지 수신 - fetchProperties", event.data);
    getSelectedObjectProperties();
  } else if (event.data.action === "fetchFamilyTypes") {
    console.log("[inject.js] content.js에서 메시지 수신 - fetchFamilyTypes", event.data);
    getFamilyTypesByCategory();
  }
});

// 현재 활성 뷰어 인스턴스를 반환합니다.
// ACC에서는 NOP_VIEWER가 사용될 가능성이 높습니다.
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

// 기존 기능: 선택된 객체의 속성을 가져오기
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

// 업그레이드 기능: 모델의 모든 요소를 순회하여,
// 각 카테고리별로 사용된 '패밀리 타입(또는 타입 이름)'을 그룹화하고 정렬합니다.
function getFamilyTypesByCategory() {
  let viewer = getViewerInstance();
  if (!viewer) {
    console.error("[inject.js] 🚨 Viewer 인스턴스 없음");
    return;
  }
  
  let instanceTree = viewer.model.getData().instanceTree;
  let allDbIds = [];
  // 재귀적으로 전체 요소의 dbId를 수집
  instanceTree.enumNodeChildren(instanceTree.getRootId(), function(dbId) {
    allDbIds.push(dbId);
  }, true);
  
  console.log("[inject.js] 수집된 dbIds 개수:", allDbIds.length);
  
  // Bulk Properties API를 사용하여 각 요소의 Category, Type Name, Family 속성을 한 번에 가져옵니다.
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
          // 만약 "Type Name"이 없는 경우, Family 속성을 대체로 사용
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
    
    // 그룹화된 데이터를 문자열로 변환 (각 카테고리별로 정렬)
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
    // 결과를 content.js 또는 popup.js로 전달
    window.postMessage({ action: "displayProperties", data: output }, "*");
  });
}
