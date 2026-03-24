function sendData(){

let car=document.getElementById("car").value;
let meat=document.getElementById("meat").value;
let energy=document.getElementById("energy").value;

fetch("/calculate", {
method:"POST",
headers:{
"Content-Type":"application/json"
},
body: JSON.stringify({car, meat, energy})
})
.then(res=>res.json())
.then(data=>{
document.getElementById("result").innerHTML=
"Carbon Footprint: "+data.total.toFixed(2)+" kg CO2/day";
});

}
function loadChart(){

fetch("/history")
.then(res=>res.json())
.then(data=>{

let values=data.map(item=>item[0]);

new Chart(document.getElementById("chart"), {
type: 'line',
data: {
labels: values.map((_,i)=>"Day "+(i+1)),
datasets: [{
label: "Carbon Footprint",
data: values
}]
}
});

});

}

window.onload=loadChart;