var browser;
//MC Info
var mcName = "Incident";
var XMLFileName = "Incident.xml";

//Images
var machineOverheadImage = new Image();
machineOverheadImage.src = "images/map" + mcName + ".png";
var bgCanvas;
var canvas;
var canvasContainer;
var bgContext;
var context;

//                                                                 |  Max Length before this line.
var days = [0,0,0,0];
var count_days = [0,0,0,0];
var Day_array = [];
var yesterday = new Date();
yesterday.setDate(yesterday.getDate()-1);
var one_day = 1000*60*60*24;
	var startTime = new Date();
//                                                                 | Max Length before this line.

	


function writeText() {
	try{
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("Incidents").innerHTML =
      this.responseText;
    }
  };
  xhttp.open("GET", XMLFileName, true);
  xhttp.send();
	}
	catch (err){
		console.log (err)
	}
}

//Interval timers
var intID1
var ONE_FRAME_TIME = 1000;


//Save the windows position so scada tv comes up formatted
window.onbeforeunload = beforeClose;



//Called when everything is loaded
function init() {
    try {
	
        bgCanvas = document.getElementById("bgCanvas");
        canvas = document.getElementById("canvasID");
        leftContainer = document.getElementById("leftContainer");
        canvasContainer = document.getElementById("canvasContainer");
        bgContext = bgCanvas.getContext("2d");
        context = canvas.getContext("2d");
        canvasContainer.style.width = machineOverheadImage.width + 'px';
        canvasContainer.style.height = machineOverheadImage.height + 'px';
        leftContainer.style.width = machineOverheadImage.width + 'px';
        leftContainer.style.height = machineOverheadImage.height + canvasContainer.offsetTop + 'px';
        bgCanvas.width = machineOverheadImage.width;
        bgCanvas.height = machineOverheadImage.height;
        bgContext.drawImage(machineOverheadImage, 0, 0);
        canvas.width = bgCanvas.width;
        canvas.height = bgCanvas.height;
        intID1 = setInterval(mainloop, ONE_FRAME_TIME);
    } catch (err) {
		console.log (err);
	}
}

function mainloop() {
    try {
        context.clearRect(0, 0, canvas.width, canvas.height);
        getDataFromXML();
		print(context);
		changeover();
    } catch (err) {
		console.log (err);
	}
}

function changeover(){
	var endTime = new Date();
	var timeDiff = endTime - startTime;
	timeDiff /= 1000;
	console.log(timeDiff);
	if (timeDiff > 15){
		window.close();
	}
	return;
}

function getDataFromXML() {
    try {
        //Open XML file
        var xmlhttp1 = new ActiveXObject("Microsoft.XMLHTTP");
        xmlhttp1.open("GET", XMLFileName, true);
        xmlhttp1.send();
        var xmlDoc = new ActiveXObject('Microsoft.XMLDOM');
        if (xmlDoc.loadXML(xmlhttp1.responseText)) {
            getData(xmlDoc);
        }
    } catch (err) {
		console.log(err)
	}
}


function getData(xmlDoc) {
	try{
		var days = xmlDoc.getElementsByTagName("Incident");
		var i = 0;
		var T = "T00:00:00"
		for (i = 0; i < days.length; i++){
			Day_array[i] = days[i].getElementsByTagName("days")[0].childNodes[0].nodeValue;
			Day_array[i] = Day_array[i].concat(T);
			count_days[i] = calculate_days(Day_array[i]);
			if (count_days[i] < 0){
				count_days[i] *= -1;
			}
		}
	}
	catch (err) {
		console.log (err);
	}
}

function calculate_days(x) {
	var date2 = new Date(x);
	return (Math.round((yesterday.getTime()-date2.getTime())/(one_day)))
}

function print(ctx) {
	try {
		//console.log(Day_array[0]);
		var oldFont = ctx.font;
		ctx.font = "300px Arial";
		var divideW = (machineOverheadImage.width/4);
		var divideH = machineOverheadImage.height/4;
		
		ctx.fillStyle = "black";
		ctx.textAlign = "center";
		ctx.fillText(count_days[0], divideW, divideH);
		ctx.fillText(count_days[1], divideW*3, divideH);
		ctx.fillText(count_days[2], divideW, divideH*3);
		ctx.fillText(count_days[3], divideW*3, divideH*3);
		ctx.save();
		ctx.translate(divideW*2,divideH*2);
		ctx.font = "150px Arial";
		ctx.fillStyle = "blue";
		ctx.rotate(-Math.PI /4);
		ctx.fillText("Test Data - WIP", 0,0);
		ctx.restore();
		ctx.font = oldFont;
		
	}
	catch (err) {
		console.log(err)
	}
}

function beforeClose() {
    try {
		window.clearInterval(intID1);
    } catch (err) {
		console.log (err);
	}
}
