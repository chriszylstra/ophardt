 var machineXMLFileName = "dispenserData.xml";
 var database = [];
 
	function getMachineDataFromXML() {
		try{			
			var xmlhttp1 = new ActiveXObject("Microsoft.XMLHTTP");
			xmlhttp1.open("GET", machineXMLFileName, true);
			xmlhttp1.send();
			
			var xmlDoc = new ActiveXObject('Microsoft.XMLDOM');
			if( xmlDoc.loadXML(xmlhttp1.responseText) ) {	
				getData(xmlDoc);
			}
		}catch(err) {
			console.log("getMachineDataFromXML: " + err);
		}
	 }
	 
	function getData(xmlDoc){
		try{
			var t0 = 0;
			var t1 = 0;
			var t2 = 0; 
			var t3 = 0;
			var t4 = 0;
			var t5 = 0;
			var t6 = 0;
			var t7 = 0;
			var t8 = 0;
			var t9 = 0;
			var t10 = 0;  
			var t11 = 0;  
			var t12 = 0;  
			var t13 = 0; 
			var t14 = 0; 
			var t15 = 0; 
			var t16 = 0;
			var t17 = 0;
			var t18 = 0; 
			var t19 = 0; 
			var t20 = 0; 
			var t21 = 0; 
			var t22 = 0; 
			var t23 = 0; 
			var machineData = xmlDoc.getElementsByTagName("Machine");
		
			for (var i = 0; i < machineData.length; i++){	
				if (machineData[i].getElementsByTagName("t8")[0].hasChildNodes() == true){
					t8 = parseInt(machineData[i].getElementsByTagName("t8")[0].childNodes[0].nodeValue, 10);
				}
				
				if (machineData[i].getElementsByTagName("t9")[0].hasChildNodes() == true){
					t9 = parseInt(machineData[i].getElementsByTagName("t9")[0].childNodes[0].nodeValue, 10);
				}
				if (machineData[i].getElementsByTagName("t10")[0].hasChildNodes() == true){
					t10 = parseInt(machineData[i].getElementsByTagName("t10")[0].childNodes[0].nodeValue, 10);
				}
				if (machineData[i].getElementsByTagName("t11")[0].hasChildNodes() == true){
					t11 = parseInt(machineData[i].getElementsByTagName("t11")[0].childNodes[0].nodeValue, 10);
				}
				if (machineData[i].getElementsByTagName("t12")[0].hasChildNodes() == true){
					t12 = parseInt(machineData[i].getElementsByTagName("t12")[0].childNodes[0].nodeValue, 10);
				}
				if (machineData[i].getElementsByTagName("t13")[0].hasChildNodes() == true){
					t13 = parseInt(machineData[i].getElementsByTagName("t13")[0].childNodes[0].nodeValue, 10);
				}
				if (machineData[i].getElementsByTagName("t14")[0].hasChildNodes() == true){
					t14 = parseInt(machineData[i].getElementsByTagName("t14")[0].childNodes[0].nodeValue, 10);
				}
				if (machineData[i].getElementsByTagName("t15")[0].hasChildNodes() == true){
					t15 = parseInt(machineData[i].getElementsByTagName("t15")[0].childNodes[0].nodeValue, 10);
				}
				if (machineData[i].getElementsByTagName("t16")[0].hasChildNodes() == true){
					t16 = parseInt(machineData[i].getElementsByTagName("t16")[0].childNodes[0].nodeValue, 10);
				}
				if (machineData[i].getElementsByTagName("t17")[0].hasChildNodes() == true){
					t17 = parseInt(machineData[i].getElementsByTagName("t17")[0].childNodes[0].nodeValue, 10);
				}
				if (machineData[i].getElementsByTagName("t18")[0].hasChildNodes() == true){
					t18 = parseInt(machineData[i].getElementsByTagName("t18")[0].childNodes[0].nodeValue, 10);
				}
				if (machineData[i].getElementsByTagName("t19")[0].hasChildNodes() == true){
					t19 = parseInt(machineData[i].getElementsByTagName("t19")[0].childNodes[0].nodeValue, 10);
				}
				if (machineData[i].getElementsByTagName("t20")[0].hasChildNodes() == true){
					t20 = parseInt(machineData[i].getElementsByTagName("t20")[0].childNodes[0].nodeValue, 10);
				}
				if (machineData[i].getElementsByTagName("t21")[0].hasChildNodes() == true){
					t21 = parseInt(machineData[i].getElementsByTagName("t21")[0].childNodes[0].nodeValue, 10);
				}
				if (machineData[i].getElementsByTagName("t22")[0].hasChildNodes() == true){
					t22 = parseInt(machineData[i].getElementsByTagName("t22")[0].childNodes[0].nodeValue, 10);
				}
				if (machineData[i].getElementsByTagName("t23")[0].hasChildNodes() == true){
					t23 = parseInt(machineData[i].getElementsByTagName("t23")[0].childNodes[0].nodeValue, 10);
				}
				if (machineData[i].getElementsByTagName("t0")[0].hasChildNodes() == true){
					t0 = parseInt(machineData[i].getElementsByTagName("t0")[0].childNodes[0].nodeValue, 10);
				}
				if (machineData[i].getElementsByTagName("t1")[0].hasChildNodes() == true){
					t1 = parseInt(machineData[i].getElementsByTagName("t1")[0].childNodes[0].nodeValue, 10);
				}
				if (machineData[i].getElementsByTagName("t2")[0].hasChildNodes() == true){
					t2 = parseInt(machineData[i].getElementsByTagName("t2")[0].childNodes[0].nodeValue, 10);
				}
				if (machineData[i].getElementsByTagName("t3")[0].hasChildNodes() == true){
					t3 = parseInt(machineData[i].getElementsByTagName("t3")[0].childNodes[0].nodeValue, 10);
				}
				if (machineData[i].getElementsByTagName("t4")[0].hasChildNodes() == true){
					t4 = parseInt(machineData[i].getElementsByTagName("t4")[0].childNodes[0].nodeValue, 10);
				}
				if (machineData[i].getElementsByTagName("t5")[0].hasChildNodes() == true){
					t5 = parseInt(machineData[i].getElementsByTagName("t5")[0].childNodes[0].nodeValue, 10);
				}
				if (machineData[i].getElementsByTagName("t6")[0].hasChildNodes() == true){
					t6 = parseInt(machineData[i].getElementsByTagName("t6")[0].childNodes[0].nodeValue, 10);
				}
				if (machineData[i].getElementsByTagName("t7")[0].hasChildNodes() == true){
					t7 = parseInt(machineData[i].getElementsByTagName("t7")[0].childNodes[0].nodeValue, 10);
				}
				
				var x = new hourlyData(t0,t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21,t22,t23);
				
				database.push(x);
				
			}
			
		} catch(err){
			console.log("getData " + err);
		}
	}
	
	function hourlyData(t0,t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21,t22,t23){
		try{
		this.t0 = t0;
		this.t1 = t1;
		this.t2 = t2;
		this.t3 = t3;
		this.t4 = t4;
		this.t5 = t5;
		this.t6 = t6;
		this.t7 = t7;
		this.t8 = t8;
		this.t9 = t9;
		this.t10 = t10;
		this.t11 = t11;
		this.t12 = t12;
		this.t13 = t13;
		this.t14 = t14;
		this.t15 = t15;
		this.t16 = t16;
		this.t17 = t17;
		this.t18 = t18;
		this.t19 = t19;
		this.t20 = t20;
		this.t21 = t21;
		this.t22 = t22;
		this.t23 = t23;
	
		}
		
		catch(err){
			console.log("hourlyData: " + err);
		}
	}
	
 window.onload = function () {
	getMachineDataFromXML();
	var chart1 = new CanvasJS.Chart("chartContainer1", {            
      title:{
        text: "Neptune TF Dispenser Production - Last 24H",   
		fontSize: 40
      },
	  axisX: {
		interval:1,
		labelFontSize: 30
	  },
	  axisY: {
		includeZero: true,
		maximum: 70
		},	
      data: [  //array of dataSeries     
      {        
       type: "column",
	   color: "red",
	   indexLabelFontSize: 32,
	   indexLabelOrientation: "vertical",
	   lineThickness: 5,
	   markerSize: 15,
       dataPoints: [
       { label: "8", y: database[0].t8}, 
	   { label: "9", y: database[0].t9}, 
	   { label: "10", y: database[0].t10},
	   { label: "11", y: database[0].t11},
	   { label: "12", y: database[0].t12},
	   { label: "13", y: database[0].t13},
	   { label: "14", y: database[0].t14},
	   { label: "15", y: database[0].t15},
	   { label: "16", y: database[0].t16},
	   { label: "17", y: database[0].t17},
	   { label: "18", y: database[0].t18},
	   { label: "19", y: database[0].t19},
	   { label: "20", y: database[0].t20},
	   { label: "21", y: database[0].t21},
	   { label: "22", y: database[0].t22},
	   { label: "23", y: database[0].t23},
	   { label: "0", y: database[0].t0}, 
	   { label: "1", y: database[0].t1}, 
	   { label: "2", y: database[0].t2}, 
	   { label: "3", y: database[0].t3}, 
	   { label: "4", y: database[0].t4}, 
	   { label: "5", y: database[0].t5}, 
	   { label: "6", y: database[0].t6}, 
       { label: "7", y: database[0].t7}, 
       ]
     },
    ] 
  });
 
chart1.render(); 


}