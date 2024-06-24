

function hideAllPages() {
  document.querySelector("#frame_MenuBtn").style.fontWeight = "normal";
  document.querySelector("#framePage").style.display = "None";
  document.querySelector("#material_MenuBtn").style.fontWeight = "normal";
  document.querySelector("#materialPage").style.display = "None";
  document.querySelector("#load_MenuBtn").style.fontWeight = "normal";
  document.querySelector("#loadPage").style.display = "None";

}


// 페이지가 로드되면 실행될 함수
window.addEventListener('load', init);


function init() {
  // canvas 엘리먼트 생성
  const canvas = document.createElement('canvas');
  canvas.setAttribute('id', 'framePage');
  console.log(canvas)

  // canvas 크기 설정
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  // HTML 문서의 body 요소에 canvas 추가
  document.body.appendChild(canvas);
 
  // WebGLRenderer 생성 및 설정
  const renderer = new THREE.WebGLRenderer({ canvas });
  renderer.setSize(canvas.width, canvas.height);
  renderer.setClearColor(0xfdfdfd, 0.5);

  // 씬(Scene) 생성
  const scene = new THREE.Scene();

  // 카메라(Camera) 생성 (원근 투영 카메라)
  const camera = new THREE.PerspectiveCamera(30, window.innerWidth / window.innerHeight,1,500);
 
  // 카메라 위치 설정 (x, y, z 좌표)
  //camera.position.z =5;
  camera.position.set(50, 50, 100);
  camera.lookAt(0, 0, 0)
  
  // 오빗컨트롤 설정
  //new OrbitControls(camera, canvas);
  
  // 큐브(Geometry) 생성
  //const geometry = new THREE.BoxGeometry();
 
  // 재질(Material) 생성 (색상 지정)
  //const material = new THREE.MeshBasicMaterial({ color:"red" });
  const material = new THREE.LineBasicMaterial( { color: "black" } );
 
  // 메쉬(Mesh) 생성 (큐브와 재질을 결합)
  //const cube = new THREE.Mesh(geometry, material);
  
  // 선 생성
  const points = [];
  points.push( new THREE.Vector3( - 10, 0, 0 ) );
  points.push( new THREE.Vector3( 0, 10, 0 ) );
  points.push( new THREE.Vector3( 10, 0, 0 ) );
  
  const geometry = new THREE.BufferGeometry().setFromPoints( points );
  const line = new THREE.Line( geometry, material );
 
  // 씬에 메쉬 추가 
  //scene.add(cube);
  scene.add(line);
  renderer.render( scene, camera );

  
  function animate() {
    requestAnimationFrame(animate); 
    
    cube.rotation.x +=0.01;
    cube.rotation.y +=0.01;
   
    renderer.render(scene,camera); 
  }
  
  //animate(); 
}

function getCheckboxValue() {
    const query = 'input[name="isSlab"]'//:checked'
    const selectedEls = document.querySelectorAll(query);
    console.log(selectedEls[0]);
    
    //let result = '';
    let result = [];
    selectedEls.forEach((el) => {
        //result += el.value + ' ';
        if (el.checked) {
            result.push(el.value);
        } else {
            result.push('off');
        }
        
    });
    
    const resElem = document.getElementById('DL-result');
    resElem.setAttribute('data-result', result);
}

function setEventListener(target) {
    document.addEventListener('DOMContentLoaded', () => {
        const increaseButton = document.getElementById('increaseButton');
        const decreaseButton = document.getElementById('decreaseButton');
        const inputContainer = document.getElementById(target + 'inputContainer');
        console.log(target=='DL');
        console.log(target=='LL');
        let inputCount = 0;

        increaseButton.addEventListener('click', () => {
            inputCount++;
            const inputGroup = document.createElement('div');
            inputGroup.className = target + 'inputGroup';

            const label = document.createElement('label');
            label.textContent = inputCount + '.';

            const newInput = document.createElement('input');
            newInput.type = 'number';
            newInput.setAttribute('display', 'inline');
            newInput.placeholder = 'Enter load in kN/m²';
            
            const new_chkBoxLabel = document.createElement('label');
            const newInput_chkBox = document.createElement('input');
            
            if ( target == 'DL' ) {
                new_chkBoxLabel.textContent = "slab 여부 - "
                new_chkBoxLabel.setAttribute('display', 'inline');
                
                newInput_chkBox.type = 'checkbox';
                newInput_chkBox.setAttribute('name', 'isSlab');
                newInput_chkBox.setAttribute('onclick', 'getCheckboxValue()');
                newInput_chkBox.setAttribute('checked', 'checked');
                newInput_chkBox.setAttribute('display', 'inline');
            } else if ( target == 'LL' ) {
                new_chkBoxLabel.textContent = "slab 여부 - "
                new_chkBoxLabel.setAttribute('display', 'inline');
                new_chkBoxLabel.setAttribute('style', 'color:white');
                newInput_chkBox.type = 'checkbox';
                newInput_chkBox.setAttribute('name', 'noUse');
                newInput_chkBox.setAttribute('disabled', 'true');
            }
            
            
            inputGroup.appendChild(label);
            inputGroup.appendChild(newInput);
            inputGroup.appendChild(new_chkBoxLabel);
            inputGroup.appendChild(newInput_chkBox);
            inputContainer.appendChild(inputGroup);
        });

        decreaseButton.addEventListener('click', () => {
            if (inputContainer.lastChild) {
                inputContainer.removeChild(inputContainer.lastChild);
                inputCount--;
            }
        });
    });
}


function download(filename, text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    const timeFilename = filename + Date.now().toString()
    element.setAttribute('download', timeFilename);
  
    element.style.display = 'none';
    document.body.appendChild(element);
  
    element.click();
  
    document.body.removeChild(element);
}

// download('test.txt', 'Hello world!');

function get_DL_json() {
    const inputs = document.querySelectorAll('.DLinputGroup input');
    let isSlab = document.getElementById('DL-result').getAttribute('data-result');
    console.log(isSlab);
    const res = inputs.values()
    const load_values = [];
    inputs.forEach((input, index) => {
        if (input.value != 'on') {
            load_values.push({ id: index + 1, value: input.value });
        }
        
    });
    if ( isSlab == null ) {
        isSlab = [];
        for (let i=0; i<load_values.length; i++){
            isSlab.push('on');
        };
    };
    console.log(load_values);
    
    const final = {
      "DL_info": load_values,
      "isSlab": isSlab
    };
    const jsonStr = JSON.stringify(final);
    return jsonStr;
}

function get_LL_json() {
    const inputs = document.querySelectorAll('.LLinputGroup input');
    const res = inputs.values()
    const values = [];
    inputs.forEach((input, index) => {
        if (input.value != 'on') {
            values.push({ id: index + 1, value: input.value });
        }
    });
    console.log(values);
    const jsonStr = JSON.stringify(values);
    return jsonStr;
}

function get_WindInfo_json() {
    const labels_ = document.querySelectorAll('.form-group-wind label');
    
    const labels = [];
    labels_.forEach((e) => {
        labels.push(e.innerHTML)
    });

    var vals_ = document.querySelectorAll('.wind_vals');
    const vals = [];
    vals_.forEach((e) => {
        vals.push(e.value)
    });

    const kvPairDict = {};
    for (let i = 0; i < labels.length; i++) {
        kvPairDict[labels[i]] = vals[i];
      };
    
    const resDict = {
        "wind_info": kvPairDict
    };
    const jsonStr = JSON.stringify(resDict);
    console.log(jsonStr);
    return jsonStr;
}

function get_SeismicInfo_json() {
    const labels_ = document.querySelectorAll('.form-group-seismic label');
    
    const labels = [];
    labels_.forEach((e) => {
        labels.push(e.innerHTML)
    });

    var vals_ = document.querySelectorAll('.seismic_vals');
    const vals = [];
    vals_.forEach((e) => {
        vals.push(e.value)
    });

    const kvPairDict = {};
    for (let i = 0; i < labels.length; i++) {
        kvPairDict[labels[i]] = vals[i];
      };
    
    const resDict = {
        "seismic_info": kvPairDict
    };
    const jsonStr = JSON.stringify(resDict);
    console.log(jsonStr);
    return jsonStr;
}

function saveLoadData_asJson(filename,jsonStr) {
    
    download(filename, jsonStr);
    alert("Save Completed!");

}

document.querySelector("#frame_MenuBtn").onclick = function() {
  hideAllPages();
  document.querySelector("#frame_MenuBtn").style.fontWeight = "bolder";
  document.querySelector("#framePage").style.display = "inline";
};

document.querySelector("#material_MenuBtn").onclick = function() {
  hideAllPages();
  document.querySelector("#material_MenuBtn").style.fontWeight = "bolder";
  document.querySelector("#materialPage").style.display = "inline";
};

document.querySelector("#load_MenuBtn").onclick = function() {
  hideAllPages();
  document.querySelector("#load_MenuBtn").style.fontWeight = "bolder";
  document.querySelector("#loadPage").style.display = "inline";
};


setEventListener('DL');
setEventListener('LL');
	
