<?php
$name=$_POST['name'];
$email=$_POST['email'];
$password=$_POST['password'];
$phno=$_POST['phno'];
$address=$_POST['address'];
if(!empty($name) || !empty($email) || !empty($password) ||!empty($phno) || !empty($address))
{
	$host="localhost";
	$dbusername="root";
	$dbpassword="";
	$dbname="floodcnx";

//create connection
$conn=new mysqli($host,$dbusername,$dbpassword,$dbname);

if(mysqli_connect_error()){
die('connect Error('.
mysqli_connect_errno().')'
. mysqli_connect_error());
}
else
{
	$SELECT="SELECT email From registrationform where email=? limit 1";
	$INSERT="INSERT Into registrationform(name,email,password,phno,address)
	values(?,?,?,?,?)";

	$stmt=$conn->prepare($SELECT);
	$stmt->bind_param("s",$email);
	$stmt->execute();
	$stmt->bind_result($email);
	$stmt->store_result();
	$rnum=$stmt->num_rows;

	if($rnum==0){
		$stmt->close();
		$stmt=$conn->prepare($INSERT);
		$stmt->bind_Param("sssis",$name,$email,$password,$phno,$address);
		$stmt->execute();
		echo "Account created successfully";
	}
	else{
		echo "Someone already register using the same email id .so use another email id ";
	}
	$stmt->close();
	$conn->close();
}
}

else{
		echo "All field are requried";
		die();
	}
?>