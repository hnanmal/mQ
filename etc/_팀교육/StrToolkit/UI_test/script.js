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
function appendResultToBody(data) {
    // const str = document.createElement(data);
    document.body.append(data);
}

function get_DL_json() {
    const inputs = document.querySelectorAll('.DLinputGroup input');
    const res = inputs.values()
    const values = [];
    inputs.forEach((input, index) => {
        values.push({ id: index + 1, value: input.value });
    });
    console.log(values);
    return values
}
function get_LL_json() {
    const inputs = document.querySelectorAll('.LLinputGroup input');
    const res = inputs.values()
    const values = [];
    inputs.forEach((input, index) => {
        values.push({ id: index + 1, value: input.value });
    });
    console.log(values);
    return values
}
function get_WindInfo_json() {
    // const inputs = document.querySelectorAll('#wind-codeSelect');
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

    const boddy = document.querySelector('#wind-result');
    console.log(boddy);
    const jsonStr = JSON.stringify(resDict);
    boddy.append(jsonStr);
    // appendResultToBody(jsonStr)
    return boddy;
}

function saveLoadData_asJson() {
    // alert("Save Completed!")
    const selectElement = document.getElementById('riskCategory');
    // alert(selectElement.value)
    const selectedIndex = selectElement.selectedIndex;
    console.log(selectedIndex)
}

function calculateWindLoad() {
    const height = parseFloat(document.getElementById('height').value);
    const windSpeed = parseFloat(document.getElementById('windSpeed').value);
    const exposureCategory = document.getElementById('exposureCategory').value;

    if (isNaN(height) || isNaN(windSpeed)) {
        alert("Please enter valid numerical values for height and wind speed.");
        return;
    }

    // Simplified wind load calculation (example)
    const windPressure = 0.00256 * (windSpeed ** 2);
    const exposureFactors = { "A": 0.8, "B": 1.0, "C": 1.2, "D": 1.6 };
    const exposureFactor = exposureFactors[exposureCategory];
    const windLoad = windPressure * height * exposureFactor;

    document.getElementById('result').innerText = `Calculated Wind Load: ${windLoad.toFixed(2)} N/m²`;
}



setEventListener('DL')
setEventListener('LL')