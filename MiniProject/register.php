<?php
ob_start(); 

$servername = "localhost";
$username = "root";
$password = "";
$database = "e-commerce";


$conn = new mysqli($servername, $username, $password, $database);


if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
  $user = $_POST['username'];
  $email = $_POST['email'];
  $pass = password_hash($_POST['password'], PASSWORD_DEFAULT); 

  $sql = "INSERT INTO users (username, email, password) VALUES ('$user', '$email', '$pass')";

  if ($conn->query($sql) === TRUE) {
    echo "Registered successfully. Redirecting to login...";
    header("Refresh: 2; URL=login.html"); 
    exit();
  } else {
    echo " Error: " . $conn->error;
  }
}

$conn->close();
ob_end_flush(); 
?>
