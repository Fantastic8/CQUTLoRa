$(document).ready(function(){	
	var checkun=false;
	var checkpw=false;
	
	//user name check
	$("#username").change(function(){
		if($.ajax({
            type: "POST",
            url: "../Controller/checkusername.php",
            data: "name="+$("#username").val(),
            async: false
         }).responseText=="True")
		{
			$("#usernamemessage").text("User Name available");
			checkun=true;
		}
		else
		{
			$("#usernamemessage").text("User Name unavailable");
			checkun=false;
		}
	});
	
	//password check
	$("#repassword").change(function(){
		if($("#password").val()==$("#repassword").val())
		{
			$("#passwordmessage").text("Correct");
			checkpw=true;
		}
		else
		{
			$("#passwordmessage").text("InCorrect");
			checkpw=false;
		}
	});
	
	$("#password").change(function(){
		if($("#password").val()==$("#repassword").val())
		{
			$("#passwordmessage").text("Correct");
			checkpw=true;
		}
		else
		{
			$("#passwordmessage").text("InCorrect");
			checkpw=false;
		}
	});
	
	//check submit
	$("#registerform").submit(function(){  
	    if(checkun && checkpw)
	    {  
	        return true;  
	    }
	    else
	    {  
	        return false;  
	    }  
	});  
});