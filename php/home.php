<?php
error_reporting(E_ALL ^ E_DEPRECATED || ~E_NOTICE);

//start session
session_start();

//get attributes
$username=$_SESSION['username'];
//$admin=$_SESSION['admin'];

//check database
$con = mysql_connect("localhost","CQUTLoRa","cqutlora");
if (!$con or !mysql_query("use CQUTLoRa",$con))
{
	die('Could not connect to database: ' . mysql_error().'. Please contact administrator.');
}
?>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1, user-scalable=no">
<script type="text/javascript" src="JavaScript/jquery-1.12.3.js"></script>
<script type="text/javascript" src="JavaScript/jquery-ui.min.js"></script>
<script type="text/javascript" src="JavaScript/jquery.canvasjs.min.js"></script>
<script src="JavaScript/home.js"></script>
<link type="text/css" rel="stylesheet" href="CSS/jquery-ui.min.css">
<link type="text/css" rel="stylesheet" href="CSS/home.css">
<title>Root Manager</title>
</head>
<body>
	<div hidden id="username"><?php echo $username ?></div>
	
	<div class="navigator">
		<ul class="selectable">
			<li style="float:right" id="exit" class="selectee">Exit</li>
			<li style="float:right" id="name"><div><?php echo $username;?></div></li>
		</ul>
	</div>
	
	<div class="content" id="content">
	</div>
</body>
</html>