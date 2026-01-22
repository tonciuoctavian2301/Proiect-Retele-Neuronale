<?php
session_start();
include 'db.php'; // Conexiunea ta la baza de date

if (isset($_POST['login'])) {
    $username = mysqli_real_escape_string($conn, $_POST['username']);
    $parola = $_POST['parola'];

    $sql = "SELECT id, username, parola, rol FROM utilizatori WHERE username = '$username'";
    $result = mysqli_query($conn, $sql);

    if (mysqli_num_rows($result) === 1) {
        $row = mysqli_fetch_assoc($result);
        
        // Verificăm parola (Notă: folosește password_verify dacă parolele sunt criptate)
        if ($parola === $row['parola']) { 
            $_SESSION['user_id'] = $row['id'];
            $_SESSION['nume'] = $row['username'];
            $_SESSION['rol'] = $row['rol'];

            // Redirecționare în funcție de rol
            if ($row['rol'] === 'admin') {
                header("Location: admin_dashboard.php");
            } else {
                header("Location: index.php");
            }
            exit();
        } else {
            $_SESSION['eroare'] = "Parolă incorectă!";
        }
    } else {
        $_SESSION['eroare'] = "Utilizatorul nu există!";
    }
    header("Location: login.php");
}
?>