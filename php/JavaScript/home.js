//global variables
var admin;
var username;
var data_table_array;
var data_table_flag=true;
$(document).ready(function(){
	//get user name
	username=$("#username").html()
	
	//check user admin
	admin=$.ajax({
        type: "POST",
        url: "../Controller/database_controller.php",
        data: "type=admin&param1="+username,
        async: false
     }).responseText;
	//load pages
	loadpages();
	
	//set up selectable
	$(".selectable").selectable({
		filter: ".selectee",
		selected: function( event, ui ) {
			to_page($(ui.selected).attr('id'));
		}
	});
	
	//initiate page
	$("#home").addClass("ui-selected");
	to_page("home");
});
/************************************************************************************************************************************************
 * 																Turn Page
 ***********************************************************************************************************************************************/
//load pages
function loadpages()
{
	//distinguish authoritative
	if(admin=="1")//admin
	{
		//add page tags
		$(".navigator ul").prepend(
				"<li id='home' class='selectee'>Home</li>"+
				//"<li id='accessory' class='selectee'>Accessory</li>"+
				"<li id='data' class='selectee'>Data</li>"+
				"<li id='node' class='selectee'>Node</li>");
				//"<li id='user' class='selectee'>User</li>");
		
		//add page contents
		var page_h="<div id='page_home'></div>";
		var page_a="<div id='page_accessory'></div>";
		var page_d="<div id='page_data'></div>";
		var page_n="<div id='page_node'></div>";
		var page_u="<div id='page_user'></div>";
		//$(".content").html(page_h+page_a+page_d+page_n+page_u);
		$(".content").html(page_h+page_d+page_n);
		
		load_page_home();
		//load_page_accessory();
		load_page_data();
		load_page_node();
		//load_page_user();
	}
	else if(admin=="0")//visitor
	{
		//$("#name").after("<li style='float:right' id='apply' onclick=\"apply('"+username+"')\">Apply Admin</li>");
		//add page tags
		$(".navigator ul").prepend(
				"<li id='home' class='selectee'>Home</li>"+
				//"<li id='accessory' class='selectee'>Accessory</li>"+
				"<li id='data' class='selectee'>Data</li>");
				//"<li id='user' class='selectee'>User</li>");
		
		//add page contents
		var page_h="<div id='page_home'></div>";
		var page_a="<div id='page_accessory'></div>";
		var page_d="<div id='page_data'></div>";
		var page_u="<div id='page_user'></div>";
		//$(".content").html(page_h+page_a+page_d+page_u);
		$(".content").html(page_h+page_d);
		
		load_page_home();
		//load_page_accessory();
		load_page_data();
		//load_page_user();
	}
	else
	{
		window.location.href='index.php';
	}
}

//turn to home page
function load_page_home()
{
	$("#page_home").append("<img src='../Picture/HomeBG.jpg' alt='Home' style='width:100%' />");
}

//turn to accessory page
function load_page_accessory()
{
	$("#page_accessory").append("<img src='../Picture/AccessoryBG.jpg' alt='Accessory' style='width:100%' />");
}

//turn to data page
function load_page_data()
{	
	//show data tables
	refresh_tables();
	var inter=setInterval(function(){
		if($("#page_data").length > 0)
		{
			refresh_tables();
		}
		else
		{
			//clear interval when unselected
			clearInterval(inter);
		}
		},2000);
}

//turn to node page
function load_page_node()
{	
	//show nodes
	$("#page_node").html(refresh_node());
	var inter=setInterval(function(){
		if($("#page_node").length > 0)
		{
			$("#page_node").html(refresh_node());
		}
		else
		{
			//clear interval when unselected
			clearInterval(inter);
		}
	},1000);
}

//turn to user page
function load_page_user()
{	
	//admin
	if(admin=="1")
	{
		//show user
		$("#page_user").html(refresh_user());
		/*var inter=setInterval(function(){
			if($("#page_user").length > 0)
			{
				$("#page_user").html(refresh_user());
			}
			else
			{
				//clear interval when unselected
				clearInterval(inter);
			}
		},1000);*/
	}
	else//visitor
	{
		$("#page_user").html("<a onclick=\"apply('"+username+"')\">Apply Admin</a>");
	}
	
}

function to_page(page)
{
	//close all
	$("#page_home").css('display','none');
	$("#page_accessory").css('display','none');
	$("#page_data").css('display','none');
	$("#page_node").css('display','none');
	$("#page_user").css('display','none');
	switch(page)
	{
	case "home":$("#page_home").css('display','inline');break;
	case "accessory":$("#page_accessory").css('display','inline');break;
	case "data":$("#page_data").css('display','inline');break;
	case "node":$("#page_node").css('display','inline');break;
	case "user":$("#page_user").css('display','inline');break;
	case "exit":window.location.href='index.php';break;
	}
}

/************************************************************************************************************************************************
 * 																Page Ajax
 ***********************************************************************************************************************************************/
//Page_data data tables
function refresh_tables(){
	//get all table name
	$.ajax({
        type: "POST",
        url: "../Controller/database_controller.php",
        dataType: 'json',
        data: "type=page&param1=data",
        async: false,
        success: function(response) {
        	if(data_table_array==null||data_table_array.sort().toString()!=response.sort().toString())
        	{
        		//clear
        		$("#page_data").html("");
        		
        		//reverse flag
        		data_table_flag=!data_table_flag;
        		//update current point of data table name
        		data_table_array=response;
        		
        		//set up each table
        		for(var tableindex in data_table_array)
        		{
        			//show table
        			refresh_table_data(data_table_array[tableindex]);
        		}
        		
        		
        		//set up effects
        		//set resizable
        		$(".section-container").resizable();
        		
        		//bound toggle event for title
        		$(".section-title").on("click",function(){
        			$(this).toggleClass("section-open");
        			if($(this).hasClass("section-open"))
        			{
        				//open section title
        				$(this).animate({
        					padding: "0px",
        			        backgroundColor: "#959595",
        			        color: "#fff",
        			        fontSize:'30px'
        			        }, 500 );
        			}
        			else
        			{
        				//close section title
        				$(this).animate({
        					padding: "10px",
        			        backgroundColor: "#dac292",
        			        color: "#111",
        			        fontSize:'60px'
        			        }, 500 );
        			}
        			//bound toggle event for content
        			$(this).next(".section-container").toggle("blind",500);
        		});
        	}
        }
     });
}

//refresh data for each table
function refresh_table_data(tname)
{
	//build structure
	$("#page_data").append("<div class='section' id='"+tname+"'><div class='section-title'></div><div class='section-container'><div class='section-content' id='"+tname+"-diagram'></div></div></div>");
	
	var chart=null;
	var data_array=new Array();
	var property;
	var showlength=50;
	
	//get property of table to set up chart
	$.ajax({
        type: "POST",
        url: "../Controller/database_controller.php",
        dataType: 'json',
        data: "type=page&param1=data&param2="+tname,
        async: false,
        success: function(response) {
        	
        	//set up title
        	var title;
        	
        	//inter terminate flag
        	var data_update_flag=data_table_flag;
        	
        	//property check
        	try{
        		//property(not null)
	        	property=JSON.parse(response.Property);
	        	title=property.title;
        		//get series
        		$.ajax({
        	        type: "POST",
        	        url: "../Controller/database_controller.php",
        	        dataType: 'json',
        	        data: "type=page&param1=data&param2="+tname+"&param3="+property.series,
        	        async: false,
        	        success: function(response_series) {
        	        	//alert(JSON.stringify(response_series));
        	        	for(var index in response_series)
        	        	{
        	        		data_array.push({
        	        			type: property.datatype,
        	        			name: response_series[index],
        	        			showInLegend: true,
        	        			markerSize: 0,
        	        			dataPoints: new Array()});
        	        	}
        	        }
        		});
        		
        		//set up chart
            	if(property.datatype!=null&&property.datatype!=""&&property.datatype!="plain")
            	{
            		chart = new CanvasJS.Chart(tname+"-diagram", {
            			exportEnabled: true,
            			title :{
            				text: title
            			},
            			axisY: {
            				includeZero: false
            			},
            			data: data_array
            		});
            		
            		
            		//update data
            		var inter=setInterval(function(){
            			if(data_update_flag==data_table_flag)
            			{
            				$.ajax({
            			        type: "POST",
            			        url: "../Controller/database_controller.php",
            			        dataType: 'json',
            			        data: "type=page&param1=data&param2="+tname,
            			        async: false,
            			        success: function(responsedata) {
            			        	var findflag=false;
            			        	var singledata;
            			        	//data_array=new Array();//reset data array
            			        	for(var rowindex in responsedata.Tabledata)//each data
            			        	{
            			        		singledata={ x: new Date(), y: Number(responsedata.Tabledata[rowindex][property.data[1]])};
            			        		//getNowFormatDate()
            			        		findflag=false;
            			        		//find series
            			        		for(var seriesindex in data_array)
            			        		{
            			        			if(data_array[seriesindex]['name']==responsedata.Tabledata[rowindex][property.series])//find
            			        			{
            			        				data_array[seriesindex]['dataPoints'].push(singledata);
            			        				findflag=true;
            			        			}
            			        		}
            			        		if(!findflag)//not find
            			        		{
            			        			var n=new Array();
            			        			data_array.push({
            	        	        			type: property.datatype,
            	        	        			showInLegend: true,
            	        	        			name: responsedata.Tabledata[rowindex][property.series],
            	        	        			markerSize: 0,
            	        	        			dataPoints: n});
            			        			n.push(singledata);
            			        		}
            			        	}
            			        	
            			        	//check showlength
            			        	for(var seriesindex in data_array)
        			        		{
        			        			if(data_array[seriesindex]['dataPoints'].length>showlength)
        			        			{
        			        				data_array[seriesindex]['dataPoints'].shift();
        			        			}
        			        		}
            			        	
            						chart.render();
            			        }
            			     });
            			}
            			else
            			{
            				//clear interval when update
            				alert("Table update");
            				clearInterval(inter);
            			}
            			},1000);
            	}
            	else
            	{
            		//plain table
            		
            	}
        	}
        	catch(error)
        	{
        		//plain table
        		title=tname;
        	}
        	
        	//set up title
        	$("#"+tname+" .section-title").text(title);
        }
     });
}

function diagram_render(tname,datatype)
{
	if(datatype=="none")
	{
		//plain table
	}
	else
	{
		
		var dps = [];
		var dps2 = [];
		var chart = new CanvasJS.Chart(tname+"-diagram", {
			exportEnabled: true,
			title :{
				text: "Dynamic Spline Chart"
			},
			axisY: {
				includeZero: false
			},
			data: [{
				type: "spline",
				name: "LoRa1",
				markerSize: 0,
				dataPoints: dps 
			},
			{
				type: "spline",
				name: "LoRa2",
				markerSize: 0,
				dataPoints: dps2 
			}]
		});

		var xVal = 0;
		var yVal = 100;
		var updateInterval = 1000;
		var dataLength = 50; // number of dataPoints visible at any point

		var updateChart = function (count) {
			count = count || 1;
			// count is number of times loop runs to generate random dataPoints.
			for (var j = 0; j < count; j++) {	
				yVal = yVal + Math.round(5 + Math.random() *(-5-5));
				dps.push({
					x: xVal,
					y: yVal
				});
				dps2.push({
					x: xVal,
					y: yVal+Math.round(5 + Math.random() *(-5-5))
				});
				xVal++;
			}
			if (dps.length > dataLength) {
				dps.shift();
				dps2.shift();
			}
			chart.render();};
		updateChart(dataLength); 
		setInterval(function(){ updateChart() }, updateInterval);
	}
}

//Page_accessory accessories
function refresh_accessory(){
	
}

//Page_node node management
function refresh_node(){
	//get all tables
	var tablesS=$.ajax({
        type: "POST",
        url: "../Controller/database_controller.php",
        data: "type=page&param1=node",
        async: false
     }).responseText;
	if(tablesS=="False")
	{
		return;
	}
	else
	{
		return tablesS;
	}
}

//Page_user user management
function refresh_user(){
	//get all tables
	var tablesS=$.ajax({
        type: "POST",
        url: "../Controller/database_controller.php",
        data: "type=page&param1=user",
        async: false
     }).responseText;
	if(tablesS=="False")
	{
		return;
	}
	else
	{
		return tablesS;
	}
}
/************************************************************************************************************************************************
 * 																redirected PHP functions
 ***********************************************************************************************************************************************/
//apply for administrator
function apply(name){
	//get all tables
	alert($.ajax({
        type: "POST",
        url: "../Controller/database_controller.php",
        data: "type=apply&param1="+name,
        async: false
     }).responseText);
}


function distribute(src,accept)
{
	alert($.ajax({
	    type: "POST",
	    url: "../Controller/database_controller.php",
	    data: "type=distribute&param1="+src+"&param2="+accept,
	    async: false
	 }).responseText);
}
function deleteNode(src)
{
	alert($.ajax({
	    type: "POST",
	    url: "../Controller/database_controller.php",
	    data: "type=deletenode&param1="+src,
	    async: false
	 }).responseText);
}

function command(src,command)
{
	alert($.ajax({
	    type: "POST",
	    url: "../Controller/database_controller.php",
	    data: "type=command&param1="+src+"&param2="+command,
	    async: false
	 }).responseText);
}

function adminize(name,accept)
{
	alert($.ajax({
	    type: "POST",
	    url: "../Controller/database_controller.php",
	    data: "type=adminize&param1="+name+"&param2="+accept,
	    async: false
	 }).responseText);
}
/************************************************************************************************************************************************
 * 																    Toolbox
 ***********************************************************************************************************************************************/
function getNowFormatDate() {
    var date = new Date();
    var seperator1 = "-";
    var seperator2 = ":";
    var month = date.getMonth() + 1;
    var strDate = date.getDate();
    if (month >= 1 && month <= 9) {
        month = "0" + month;
    }
    if (strDate >= 0 && strDate <= 9) {
        strDate = "0" + strDate;
    }
    var currentdate = date.getFullYear() + seperator1 + month + seperator1 + strDate
            + " " + date.getHours() + seperator2 + date.getMinutes()
            + seperator2 + date.getSeconds();
    return currentdate;
}
//----------------------------------------------------------------------------------------------------------Administrator
//----------------------------------------------------------------------------------------------------------Visitor