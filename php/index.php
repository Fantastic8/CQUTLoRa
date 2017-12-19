<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1, user-scalable=no">
<script type="text/javascript" src="JavaScript/jquery-1.12.3.js"></script>
<script type="text/javascript" src="JavaScript/jquery-ui.min.js"></script>
<link type="text/css" rel="stylesheet" href="CSS/jquery-ui.min.css">
<link type="text/css" rel="stylesheet" href="CSS/index.css">
<title>Root Manager</title>
</head>
<body>
<div class="square_logo"><img src="Picture/title2.png"  alt="CQUT LoRa" /></div>
<div class="square_frame">
	<div class="square_content">
		<form action="Controller/login_controller.php" method="post">
			<table align="center">
				<tr><td>User Name</td><td><input type="text" name="username" class="TextInput"></td></tr>
				<tr><td>Password</td><td><input type="password" name="password" class="TextInput"></td></tr>
			</table>
			<p style="font-size:20px;"><?php
			session_start();
			echo $_SESSION['loginmessage'];
		 	$_SESSION['loginmessage']=null;
		 	?></p>
			<input type="submit" value="Login" class="Button">
			<input type="button" onclick="window.location.href='register.php'" value="Register" class="Button">
		</form>
	 </div>
</div>
</body>
</html>