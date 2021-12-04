let labels = [];

const data = {
  labels: labels,
  datasets: [{
    label: 'My First dataset',
    backgroundColor: 'rgb(255, 0, 0)',
    borderColor: 'rgb(255, 0, 0)',
    data: []
  }]
};

const config = {
  type: 'line',
  data: data,
  options: {}
};

let myChart = new Chart(
    document.getElementById('myChart'),
    config);

document.addEventListener("DOMContentLoaded", getFundHouses);
document.getElementById("fundHouse").addEventListener("change", getSchemes);
document.getElementById("timeFrame").addEventListener("change", getNAV);

function getFundHouses() {
    const fundHouseSelect = document.getElementById("fundHouse");
    fetch('http://localhost:5000/v1/fundhouses')
        .then(response => response.json())
        .then(data => {
        for(let i = 0; i < data.length; i++) {
            const fundHouseName = data[i].fund_house;
            const fundHouseId = data[i].fund_house_id;
            const option = document.createElement("option");
            option.textContent = fundHouseName;
            option.id = fundHouseId;
            option.value = fundHouseId;
            fundHouseSelect.appendChild(option);
        }});
}

function createGraph(labels, data) {
    const coordinates = {
      labels: labels,
      datasets: [{
        label: 'My First dataset',
        backgroundColor: 'rgb(255, 0, 0)',
        borderColor: 'rgb(255, 0, 0)',
        data: data
      }]};
    const config = {
      type: 'line',
      data: coordinates,
      options: {}
    };
    myChart.destroy();
    myChart = new Chart(
        document.getElementById('myChart'),
        config);
}

function getSchemes(e) {
    const fundHouseId = e.target.value;
    const schemeSelect = document.getElementById("schemeName");
    schemeSelect.length=0;
    fetch(`http://localhost:5000/v1/fundhouse/${fundHouseId}/schemes`)
        .then(response => response.json())
        .then(data => {
        for(let i = 0; i < data.length; i++) {
            const schemeName = data[i].scheme_name;
            const schemeId = data[i].scheme_id;
            const option = document.createElement("option");
            option.textContent = schemeName;
            option.id = schemeId;
            option.value = schemeId;
            schemeSelect.appendChild(option);
        }});
}

const getThisDate = (offsetInDays) => {
        let thisDate = new Date();
        thisDate.setDate(thisDate.getDate()-offsetInDays);
        const d = thisDate.getDate();
        const m = thisDate.getMonth() + 1; //Month from 0 to 11
        const y = thisDate.getFullYear();
        return '' + y + '-' + (m<=9 ? '0' + m : m) + '-' + (d <= 9 ? '0' + d : d);
    }

function getNAV(e) {
    const fundHouseId = document.getElementById("fundHouse").value;
    const schemeId = document.getElementById("schemeName").value;
    const selectedOptions = document.getElementById("timeFrame").selectedOptions;
    const selectedOptionId = selectedOptions[0].id;
    const endDate = getThisDate(0);
    let startDate = getThisDate(1);
    switch(selectedOptionId) {
        case "past-week": {
            startDate = getThisDate(7);
            break;
        }
        case "past-month": {
            startDate = getThisDate(31);
            break;
        }
        case "past-six-months": {
            startDate = getThisDate(186);
            break;
        }
        case "past-one-year": {
            startDate = getThisDate(365);
            break;
        }
        case "past-three-years": {
            startDate = getThisDate(1095);
            break;
        }
        case "past-five-years": {
            startDate = getThisDate(1825);
            break;
        }
        default: startDate = getThisDate(1);
    }
    const data = {
        startDate: startDate,
        endDate: endDate,
        fundHouseId: fundHouseId,
        schemeId: schemeId
        };
    fetch('http://localhost:5000/v1/nav', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            const xCoords = [];
            const yCoords = [];
            for(let i = 0; i < data.length; i++) {
                xCoords.push(data[i].date);
                yCoords.push(data[i].nav);
            }
           createGraph(xCoords, yCoords);
        })
        .catch(error => console.error(error));
}



