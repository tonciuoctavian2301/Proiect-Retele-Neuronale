<?php
session_start();
include 'db.php';

if (isset($_POST['register'])) {
    // Preluăm și curățăm datele pentru a preveni SQL Injection
    $username = mysqli_real_escape_string($conn, $_POST['username']);
    $email = mysqli_real_escape_string($conn, $_POST['email']);
    $parola = mysqli_real_escape_string($conn, $_POST['parola']); 

    // 1. Verificăm dacă utilizatorul există deja
    $check_user = "SELECT * FROM utilizatori WHERE username = '$username' OR email = '$email'";
    $result = mysqli_query($conn, $check_user);

    if (mysqli_num_rows($result) > 0) {
        $_SESSION['eroare'] = "Numele de utilizator sau email-ul este deja folosit!";
        header("Location: register.php");
    } else {
        // 2. Inserăm noul utilizator (rolul va fi 'client' prin DEFAULT)
        $sql = "INSERT INTO utilizatori (username, email, parola, rol) VALUES ('$username', '$email', '$parola', 'client')";
        
        if (mysqli_query($conn, $sql)) {
            $_SESSION['mesaj'] = "Cont creat cu succes! Te poți loga.";
            header("Location: login.php");
        } else {
            $_SESSION['eroare'] = "Eroare la înregistrare: " . mysqli_error($conn);
            header("Location: register.php");
        }
    }
    exit();
}
?>