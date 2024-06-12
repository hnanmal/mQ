// document.addEventListener('DOMContentLoaded', () => {
//     const increaseButton = document.getElementById('increaseButton');
//     const decreaseButton = document.getElementById('decreaseButton');
//     const inputContainer = document.getElementById('inputContainer');

//     increaseButton.addEventListener('click', () => {
//         const newInput = document.createElement('input');
//         newInput.type = 'number';
//         newInput.placeholder = 'Enter Load in kN/m²';
//         inputContainer.appendChild(newInput);
//     });

//     decreaseButton.addEventListener('click', () => {
//         if (inputContainer.lastChild) {
//             inputContainer.removeChild(inputContainer.lastChild);
//         }
//     });
// });

document.addEventListener('DOMContentLoaded', () => {
    const increaseButton = document.getElementById('increaseButton');
    const decreaseButton = document.getElementById('decreaseButton');
    const inputContainer = document.getElementById('inputContainer');
    let inputCount = 0;

    increaseButton.addEventListener('click', () => {
        inputCount++;
        const inputGroup = document.createElement('div');
        inputGroup.className = 'inputGroup';

        const label = document.createElement('label');
        label.textContent = inputCount + '.';

        const newInput = document.createElement('input');
        newInput.type = 'text';
        newInput.placeholder = 'Enter text here';

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

const selectElement = document.getElementById('riskCategory');
// alert(selectElement.value)
const selectedIndex = selectElement.selectedIndex;
console.log(selectedIndex)
// const selectedValue = selectElement.options[selectedIndex].value;
 
// console.log(selectedValue); // 선택된 옵션의 값 출력