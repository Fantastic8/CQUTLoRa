<?php
error_reporting(E_ALL ^ E_DEPRECATED || ~E_NOTICE);

//session start
session_start();

//get attributes
$username=$_POST['username'];
$password=$_POST['password'];

//check database
$con = mysql_connect("localhost","CQUTLoRa","cqutlora");
if (!$con or !mysql_query("use CQUTLoRa",$con))
{
	die('Could not connect to database: ' . mysql_error().'. Please contact administrator.');
}

//insert
$sql="INSERT INTO LUser VALUES('".$username."','".$password."',0)";

if (!mysql_query($sql,$con))
{
	$_SESSION['registermessage']="Register failed.";
}
else
{
	$_SESSION['registermessage']="Register success!";
}
header("Location: ../register.php");
?>