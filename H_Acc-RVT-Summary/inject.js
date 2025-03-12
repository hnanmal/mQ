console.log("[inject.js] 🚀 실행됨");

// 메인 세계에서 메시지를 수신합니다.
// window.addEventListener("message", (event) => {
//     if (event.source !== window || !event.data || !event.data.action) return;
//     if (event.data.action === "fetchProperties") {
//         console.log("[inject.js] fetchProperties 메시지 수신");
//         getSelectedObjectProperties();
//     } else if (event.data.action === "fetchFamilyTypes") {
//         console.log("[inject.js] fetchFamilyTypes 메시지 수신");
//         getFamilyTypesByCategory();
//     }
// });
window.addEventListener("message", (event) => {
    if (event.source !== window || !event.data || !event.data.action) return;
    if (event.data.action === "fetchProperties") {
        console.log("[inject.js] fetchProperties 메시지 수신");
        getSelectedObjectProperties();
    } else if (event.data.action === "fetchFamilyTypes") {
        console.log("[inject.js] fetchFamilyTypes 메시지 수신");
        getFamilyTypesByCategory();
    } else if (event.data.action === "fetchRooms") {
        console.log("[inject.js] fetchRooms 메시지 수신");
        getRoomsData();
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

// 새 기능: 전체 모델 요소에서 Room 객체의 데이터를 조회하기
// function getRoomsData() {
//     let viewer = getViewerInstance();
//     if (!viewer) {
//         console.error("[inject.js] 🚨 Viewer 인스턴스 없음");
//         return;
//     }
    
//     let instanceTree = viewer.model.getData().instanceTree;
//     let allDbIds = [];
//     // instanceTree.enumNodeChildren(instanceTree.getRootId(), function(dbId) {
//     //     allDbIds.push(dbId);
//     // }, true);
//     instanceTree.enumNodeChildren(instanceTree.getNodeName(), function(dbId){
//         allDbIds.push(dbId)
//     }, true);
//     console.log("[inject.js] 수집된 instanceTree" , instanceTree.getNodeName());
    
//     console.log("[inject.js] 수집된 dbIds 개수:", allDbIds.length);
//     console.log("[inject.js] 수집된 dbIds!! :", allDbIds)
    
//     // Bulk Properties API로 "Category", "Room Number", "Name", "Area" 속성을 가져옵니다.
//     viewer.model.getBulkProperties(allDbIds, ["Category", "Number", "Name", "Area"], function(results) {
//         let rooms = results.filter(result => {
//             let categoryProp = result.properties.find(p => p.displayName === "Category");
//             // console.log("[inject.js] 수집된 result.properties :", result.properties)
//             return categoryProp && categoryProp.displayValue.toLowerCase().includes("room");
//             // return categoryProp && categoryProp.displayValue.toLowerCase().includes("wall");
//         });
//         console.log("[inject.js] 수집된 rooms :", rooms)
        

//         let output = "=== Room Data ===\n\n";
//         rooms.forEach(room => {
//             // 원하는 정보를 추출합니다. (필요에 따라 속성명을 조정하세요)
//             let roomNumber = "";
//             let roomName = "";
//             let area = "";
//             room.properties.forEach(prop => {
//                 if (prop.displayName === "Number") {
//                     roomNumber = prop.displayValue;
//                 } else if (prop.displayName === "Name") {
//                     roomName = prop.displayValue;
//                 } else if (prop.displayName === "Area") {
//                     area = prop.displayValue;
//                 }
//             });
//             output += `Room Number: ${roomNumber}\nName: ${roomName}\nArea: ${area}\n\n`;
//         });
        
//         console.log("[inject.js] Room Data 준비 완료:\n", output);
//         window.postMessage({ action: "displayProperties", data: output }, "*");
//     });
// }

// function getRoomsData() {
//     let viewer = getViewerInstance();
//     if (!viewer) {
//         console.error("[inject.js] 🚨 Viewer 인스턴스 없음");
//         return;
//     }

//     // ACC 모델의 instanceTree를 가져옵니다.
//     let instanceTree = viewer.model.getData().instanceTree;

//     // 루트 노드의 dbId를 가져옵니다.
//     let rootId = instanceTree.getRootId();
//     console.log("Root Node ID:", rootId);

//     // 재귀적으로 모든 자식 노드를 열거하는 함수
//     function traverseTree(nodeId) {
//     instanceTree.enumNodeChildren(nodeId, function(childId) {
//         // 각 자식 노드의 이름을 가져옵니다.
//         let name = instanceTree.getNodeName(childId);
//         console.log("Node ID:", childId, "Name:", name);
//         // 재귀 호출로 하위 노드도 탐색합니다.
//         traverseTree(childId);
//     }, false);
//     }

//     // 루트 노드부터 트리 순회를 시작합니다.
//     traverseTree(rootId);

// }

function getRoomsData() {
    // Method 1:
    let viewer = getViewerInstance();
    if (!viewer) {
        console.error("[inject.js] 🚨 Viewer 인스턴스 없음");
        return;
    }
    const viewerDocument = viewer.model.getDocumentNode().getDocument();

    const root = viewerDocument.getRoot() ;
    const viewables = root.search({'type': 'geometry', 'role': '3d'});
    console.log ('Viewables:' , viewables);
    const phaseViews = viewables.filter (v => v.data.name === v.data.phaseNames
    && v.getViewableRootPath().includes('08f99ae5-b8be-4f8d-881b-128675723c10'));  // pass the guid
    console.log('Master Views:', phaseViews);

    // // Method 2: if you just have one master view (phase) inside your model.
    // viewerDocument.getRoot().getDefaultGeometry(true);

    let roomids;
    viewer.search('Revit Rooms',
        ids => { roomids=ids },
        err => { console.error(err); },
        ['Category'], { searchHidden: true 
    });
    
    console.log("roomids", roomids)

    roomids.forEach((id)=>{viewer.model.getProperties(id, (p) => {
        console.log(p);
        });
    })
}