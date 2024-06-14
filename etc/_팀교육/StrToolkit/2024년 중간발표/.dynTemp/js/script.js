
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
    element.setAttribute('download', filename);
  
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
    
    download(filename, jsonStr) 
    alert("Save Completed!")

}




setEventListener('DL');
setEventListener('LL');
	
