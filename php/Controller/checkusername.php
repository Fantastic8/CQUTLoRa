<?php
error_reporting(E_ALL ^ E_DEPRECATED || ~E_NOTICE);

//check database
$con = mysql_connect("localhost","CQUTLoRa","cqutlora");
if (!$con or !mysql_query("use CQUTLoRa",$con))
{
	die();
}

//check username on LUser table
$tables="select * from LUser where UserName='".$_POST['name']."'";
if($result=mysql_query($tables,$con))
{
	if(mysql_fetch_assoc($result))
	{
		echo "False";
	}
	else
	{
		echo "True";
	}
}
?>