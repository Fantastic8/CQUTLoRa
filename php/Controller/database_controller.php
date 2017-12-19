<?php
error_reporting(E_ALL ^ E_DEPRECATED || ~E_NOTICE);

//session start
session_start();

//check database
$con = mysql_connect("localhost","CQUTLoRa","cqutlora");
if (!$con or !mysql_query("use CQUTLoRa",$con))
{
	die('Could not connect to database: ' . mysql_error().'. Please contact administrator.');
}

//get variables
$type=$_POST['type'];
$param1=$_POST['param1'];
$param2=$_POST['param2'];
$param3=$_POST['param3'];

//global variables
$forbidden=array('LUser','LGateway','LRUser','LRNode','LANode','LCNode','LTRegister');//forbidden tables for data page

//echo string
$respond="";
if(!empty($type))
{
	if(strcmp($type,"page")==0)//Page Request
	{
		$respond.=page($param1,$param2,$param3);
	}
	else if(strcmp($type,"admin")==0)//Admin check
	{
		$respond.=admin($param1);
	}
	else if(strcmp($type,"apply")==0)//Apply for Admin
	{
		$respond.=apply($param1);
	}
	else if(strcmp($type,"adminize")==0)//Adminize
	{
		$respond.=adminize($param1,$param2);
	}
	else if(strcmp($type,"distribute")==0)//response to application of node
	{
		$respond.=distribute($param1,$param2);
	}
	else if(strcmp($type,"deletenode")==0)//delete a node from group
	{
		$respond.=deletenode($param1);
	}
	else if(strcmp($type,"command")==0)//give a command to node
	{
		$respond.=command($param1,$param2);
	}	
	echo $respond;
}
else
{
	echo "False";
}

/************************************************************************************************************************************************
 * 																Function	First Level
 ***********************************************************************************************************************************************/
//page
function page($param1,$param2,$param3)
{
	global $con;
	
	//echo page
	if(!empty($param1))
	{
		if(strcmp($param1,"accessory")==0)//-------------------------------------------Accessory Page
		{
			return accessory_management();
		}
		else if(strcmp($param1,"data")==0)//-------------------------------------------Data Page
		{
			return data_management($param2,$param3);
		}
		else if(strcmp($param1,"node")==0)//-------------------------------------------Node Page
		{
			return node_management();
		}
		else if(strcmp($param1,"user")==0)//-------------------------------------------User Page
		{
			return user_management();
		}
	}
}
//admin
function admin($param1)
{
	global $con;
	$adminsql="select * from LUser where UserName='".$param1."'";
	if($result_admin=mysql_query($adminsql,$con))
	{
		//iterate all data tables from database
		if($row_admin=mysql_fetch_assoc($result_admin))
		{
			return $row_admin['Administrator'];
		}
	}
}

//apply
function apply($param1)
{
	global $con;
	
	//insert into LRUser
	$insert="insert into LRUser values('".$param1."')";
	if(mysql_query($insert,$con))
	{
		return "Your request has been sent to Administrator";
	}
	else
	{
		return "Your request has already been sent, please wait for Administrator to handle it";
	}
}

//adminize
function adminize($username,$flag)
{
	global $con;
	
	//delete from LRUser
	$delete="delete from LRUser where UserName='".$username."'";
	if($result_LRUser=mysql_query($delete,$con))
	{
		if(!empty($flag) and strcmp($flag,"true")==0)
		{
			$modify="update LUser set Administrator=1 where UserName='".$username."'";
			if(mysql_query($modify,$con))
			{
				return "User ".$username." has successfully became an Administrator";
			}
			else
			{
				return "User ".$username." has failed to become an Administrator";
			}
		}
		else
		{
			return "User ".$username." has failed to become an Administrator";
		}
	}
	else
	{
		return "User ".$username." has failed to become an Administrator";
	}
}

//distribute
function distribute($param1,$param2)
{
	global $con;
	
	//get package from LRNode
	$tablesql="select * from LRNode where LoRaId='".$param1."'";
	$package="";
	if($result_LRNode=mysql_query($tablesql,$con))
	{
		//iterate all data from tables
		if($row_LRNode=mysql_fetch_assoc($result_LRNode))
		{
			$package=$row_LRNode['RPackage'];
		}
		
		//insert into other table
		if(!empty($param2) and strcmp($param2,"true")==0 and !empty($package))
		{
			//insert into LANode
			$insertsql="insert into LANode values('".$package."')";
			mysql_query($insertsql,$con);
			
		}
		
		//delete original data
		$deletesql="delete from LRNode where LoRaId='".$param1."'";
		if(mysql_query($deletesql,$con) and strcmp($param2,"true")==0)
		{
			return "LoRa Node ".$param1." has been successfully added to system";
		}
		else
		{
			return "LoRa Node ".$param1." has failed to be added to system";
		}
	}
}

//delete node from group
function deletenode($param1)
{
	global $con;
	
	
	//delete from LGateway
	$delete="delete from LGateway where LoRaId='".$param1."'";
	if(mysql_query($delete,$con))
	{
		return "LoRa Node ".$param1." has been removed from system.";
	}
	else
	{
		return "Remove LoRa Node ".$param1." failed.";
	}
}

//command
function command($param1,$param2)
{
	global $con;
	//insert into LCNode
	$insert="insert into LCNode values('".$param1."','".$param2."')";
	if(mysql_query($insert,$con))
	{
		return "Command package has been sent to LoRa Node ".$param1;
	}
	else
	{
		return "Failed to send command package";
	}
}
/************************************************************************************************************************************************
 * 																Function	Second Level
 ***********************************************************************************************************************************************/
//get accessory html
function accessory_management()
{
	global $con;
	
}

//get data html
function data_management($param2,$param3)
{
	global $con;
	
	if(empty($param2) or strcmp($param2,"")==0)//tables
	{
		//contains all tables
		$tables=array();
		
		//$tablesql="show tables";
		$tablesql="select * from LTRegister";
		if($result_tablename=mysql_query($tablesql,$con))
		{
			//iterate all data tables from database
			while($row_tablename=mysql_fetch_assoc($result_tablename))
			{
				array_push($tables,$row_tablename['TName']);
				array_push($tables,$row_tablename['TName']);
			}
		}
		return json_encode($tables);
	}
	else if(!empty($param3) and strcmp($param3,"")!=0)//series
	{
		//contains all tables
		$series=array();
		
		//$tablesql="show tables";
		$seriessql="select distinct(".$param3.") from ".$param2;
		if($result_series=mysql_query($seriessql,$con))
		{
			//get distinct series
			while($row_series=mysql_fetch_assoc($result_series))
			{
				array_push($series,$row_series[$param3]);
			}
		}
		return json_encode($series);
	}
	else
	{
		return json_encode(gettable($param2));
	}
	
	
}


//get node html
function node_management()
{
	global $con;
	$str="";
	//LGateway
	$tablesqlLGateway="select * from LGateway";
	if($result_LGateway=mysql_query($tablesqlLGateway,$con))
	{
		$str.="<br><h3>LoRa Nodes</h3><table class='bordered'><thead><tr><th>LoRa's Physical Address</th><th>Action</th></tr></thead>";
		//iterate all data from tables
		while($row_LGateway=mysql_fetch_assoc($result_LGateway))
		{
			$str.="<tr><td>".$row_LGateway['LoRaId']."</td><td><input type=\"button\" onclick=\"command('".$row_LGateway['LoRaId']."','STANDBY')\" value=\"StandBy\"><input type=\"button\" onclick=\"command('".$row_LGateway['LoRaId']."','AWAKE')\" value=\"Awake\"><input type=\"button\" onclick=\"command('".$row_LGateway['LoRaId']."','RESET')\" value=\"Reset\"><input type=\"button\" onclick=\"deleteNode('".$row_LGateway['LoRaId']."')\" value=\"Delete\"></td></tr>";
		}
		$str.="</table>";
	}
	
	//LRNode
	$tablesql="select * from LRNode";
	if($result_LRNode=mysql_query($tablesql,$con))
	{
		$str.="<br><h3>LoRa Node requests for PP</h3><br><table class='bordered'><thead><tr><th>LoRa's Physical Address</th><th>Action</th></tr></thead>";
		//iterate all data from tables
		while($row_LRNode=mysql_fetch_assoc($result_LRNode))
		{
			$str.="<tr><td>".$row_LRNode['LoRaId']."</td><td><input type=\"button\" onclick=\"distribute('".$row_LRNode['LoRaId']."',true)\" value=\"Accept\"><input type=\"button\" onclick=\"distribute('".$row_LRNode['LoRaId']."',false)\" value=\"Refuse\"></td></tr>";
		}
		$str.="</table>";
	}
	return $str;
}

//get user html
function user_management()
{
	global $con;
	
	$str="";
	//LRUser
	$tablesqlLRUser="select * from LRUser";
	if($result_LRUser=mysql_query($tablesqlLRUser,$con))
	{
		$str.="<br><h3>Users apply for Administrator</h3><table class='zebra'><thead><tr><th>UserName</th><th>Action</th></tr></thead>";
		//iterate all data from tables
		while($row_LRUser=mysql_fetch_assoc($result_LRUser))
		{
			$str.="<tr><td>".$row_LRUser['UserName']."</td><td><input type=\"button\" onclick=\"adminize('".$row_LRUser['UserName']."',true)\" value=\"Accept\"><input type=\"button\" onclick=\"adminize('".$row_LRUser['UserName']."',false)\" value=\"Refuse\"></td></tr>";
		}
		$str.="</table>";
	}
	
	return $str;
}

/************************************************************************************************************************************************
 * 																Function	Third Level
 ***********************************************************************************************************************************************/

//get table html
function gettable($tname)
{
	global $con;
	
	//$str="";
	$tabledata=array();
	
	//get table titles
	$sql="describe ".$tname;
	if($result_tabletitle=mysql_query($sql,$con))
	{
		//table name
		//$str.="<br><h3>".$tname."</h3><table border='1' cellspacing=0 cellpadding=0>";

		//iterate all title from tables
		$titles=array();
		//$str.="<tr>";
		while($row_tabletitle=mysql_fetch_assoc($result_tabletitle))
		{
			$title=$row_tabletitle['Field'];
			if(!empty($title))
			{
				array_push($titles,$title);
				//$str.="<th>".$title."</th>";
			}
		}
		//$str.="</tr>";
		
		//get all data from table
		$datasql="select * from ".$tname;
		if($result_tabledata=mysql_query($datasql,$con))
		{
			while($row_tabledata=mysql_fetch_assoc($result_tabledata))
			{
				array_push($tabledata,$row_tabledata);
				
				/*//search data from each title
				$str.="<tr>";
				foreach($titles as $data)
				{
					$str.="<td>".$row_tabledata[$data]."</td>";
				}
				$str.="</tr>";*/
			}
			
		}
		//$str.="</table><br>";
		
		//return $str;
		
		//get property
		$property="";
		$tablep="select * from LTRegister where TName='".$tname."'";
		if($result_tablep=mysql_query($tablep,$con))
		{
			if($row_tablep=mysql_fetch_assoc($result_tablep))
			{
				$property=$row_tablep['Property'];
			}
		}
		return array("Tname"=>$tname,"Titles"=>$titles,"Tabledata"=>$tabledata,"Property"=>$property);
	}
	else
	{
		return null;
	}
}

//check forbidden tables for data page
function checkforbidden($name)
{
	global $forbidden;
	if(empty($name))
	{
		return false;
	}
	foreach($forbidden as $t)
	{
		if(strcmp($name,$t)==0)
		{
			return false;
		}
	}
	return true;
}
?>