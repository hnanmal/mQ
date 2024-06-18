
//import { OrbitControls} from "https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/examples/js/controls/OrbitControls.js"

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


function setEventListener(target) {
    document.addEventListener('DOMContentLoaded', () => {
        const increaseButton = document.getElementById('increaseButton');
        const decreaseButton = document.getElementById('decreaseButton');
        const inputContainer = document.getElementById(target + 'inputContainer');
        let inputCount = 0;

        increaseButton.addEventListener('click', () => {
            inputCount++;
            const inputGroup = document.createElement('div');
            inputGroup.className = target + 'inputGroup';

            const label = document.createElement('label');
            label.textContent = inputCount + '.';

            const newInput = document.createElement('input');
            newInput.type = 'number';
            newInput.placeholder = 'Enter load in kN/m²';

            inputGroup.appendChild(label);
            inputGroup.appendChild(newInput);
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
    const res = inputs.values()
    const values = [];
    inputs.forEach((input, index) => {
        values.push({ id: index + 1, value: input.value });
    });
    console.log(values);
    const jsonStr = JSON.stringify(values);
    return jsonStr;
}

function get_LL_json() {
    const inputs = document.querySelectorAll('.LLinputGroup input');
    const res = inputs.values()
    const values = [];
    inputs.forEach((input, index) => {
        values.push({ id: index + 1, value: input.value });
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
	
