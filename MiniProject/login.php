<?php
$servername = "localhost";
$username = "root";
$password = "";
$database = "e-commerce";


$conn = new mysqli($servername, $username, $password, $database);
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

$user = $_POST['username'];
$pass = $_POST['password'];

$sql = "SELECT * FROM users WHERE username = '$user'";
$result = $conn->query($sql);

if ($result->num_rows === 1) {
  $row = $result->fetch_assoc();
  if (password_verify($pass, $row['password'])) {
    echo \"Login successful! Welcome, $user\";
  } else {
    echo \"Invalid password.\";
  }
} else {
  echo \"User not found.\";
}
$conn->close();
?>
