<?php
error_reporting(E_ALL ^ E_DEPRECATED || ~E_NOTICE);

//start session
session_start();

//create connection
$con = mysql_connect("localhost","CQUTLoRa","cqutlora");

if (!$con or !mysql_query("use CQUTLoRa",$con))
{
	die('Could not connect to database: ' . mysql_error().'. Please contact administrator.');
}
// conect success

//get attributes
$username=$_POST["username"];
$password=$_POST["password"];
if(empty($username) or empty($password))
{
	$_SESSION['loginmessage']="User Name or Password cannot be empty!";
	header("Location: ../index.php");
}

$login="select * from LUser where UserName='{$username}'";

if(!$result=mysql_query($login,$con))
{
	$_SESSION['loginmessage']="Failed to login. Please contact Administrator.";
	header("Location: ../index.php");
}
else
{
	$row=mysql_fetch_assoc($result);
	if(!empty($row['Passwd']) and strcmp($row['Passwd'],$password)==0)
	{
		//echo "Login Success!";
		$_SESSION['username']=$username;
		header("Location: ../home.php");
	}
	else
	{
		$_SESSION['loginmessage']="Password Incorrect!";
		header("Location: ../index.php");
	}
}
?>