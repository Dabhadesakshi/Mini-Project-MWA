<?php
include 'db.php';

$username = $_POST['username'];
$password = $_POST['password'];

$sql = "SELECT * FROM users WHERE username='$username'";
$result = mysqli_query($conn, $sql);

if ($row = mysqli_fetch_assoc($result)) {
    if (password_verify($password, $row['password'])) {
        echo "<script>
            alert('Login successful!');
            window.location.href = 'dashboard.html'; // redirect after login
        </script>";
    } else {
        echo "<script>
            alert('Incorrect password.');
            window.location.href = 'index.html';
        </script>";
    }
} else {
    echo "<script>
        alert('User not found.');
        window.location.href = 'index.html';
    </script>";
}
?>
