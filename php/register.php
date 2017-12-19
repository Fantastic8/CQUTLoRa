<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1, user-scalable=no">
<script type="text/javascript" src="JavaScript/jquery-1.12.3.js"></script>
<script type="text/javascript" src="JavaScript/jquery-ui.min.js"></script>
<script src="JavaScript/register.js"></script>
<link type="text/css" rel="stylesheet" href="CSS/jquery-ui.min.css">
<link type="text/css" rel="stylesheet" href="CSS/index.css">
<title>Root Manager</title>
<style>
div{display:inline}
</style> 
</head>
<body>
<div class="square_logo"><img src="Picture/title2.png"  alt="CQUT LoRa" /></div>
<div class="square_frame">
	<div class="square_content">
		<form action="Controller/register_controller.php" method="post" id="registerform">
			<table align="center">
				<tr><td>User Name</td><td><input type="text" name="username" id="username" class="TextInput"></td><td><div id="usernamemessage" style="font-size:10px;"></div></td></tr>
				<tr><td>Password</td><td><input type="password" name="password" id="password" class="TextInput"></td><td> </td></tr>
				<tr><td>Retype Password</td><td><input type="password" name="repassword" id="repassword" class="TextInput"></td><td><div id="passwordmessage" style="font-size:10px;"></div></td></tr>
			</table>
			<p style="font-size:20px;"><?php
			session_start();
		 	echo $_SESSION['registermessage'];
		 	$_SESSION['registermessage']=null;
		 	?></p>
			<input type="submit" value="Register" class="Button">
			<input type="button" onclick="window.location.href='index.php'" value="Back" class="Button">
		</form>
	</div>
</div>
</body>
</html>