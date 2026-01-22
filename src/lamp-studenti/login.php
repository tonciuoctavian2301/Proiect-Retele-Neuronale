<?php
session_start();
include 'db.php'; // Asigură-te că db.php are conexiunea corectă

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $email = mysqli_real_escape_string($conn, $_POST['email']);
    $parola = $_POST['parola']; // În proiecte reale folosim password_verify, dar pentru curs e ok așa

    $sql = "SELECT * FROM utilizatori WHERE email = '$email' AND parola = '$parola'";
    $result = mysqli_query($conn, $sql);

    if (mysqli_num_rows($result) == 1) {
        $user = mysqli_fetch_assoc($result);
        
        // Salvăm datele în sesiune pentru ca index.php să le recunoască
        $_SESSION['utilizator_id'] = $user['id'];
        $_SESSION['utilizator_nume'] = $user['username'];
        $_SESSION['utilizator_rol'] = $user['rol'];

        header("Location: index.php");
        exit();
    } else {
        $eroare = "Email sau parolă incorectă!";
    }
}
?>

<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <title>Login - MusicShop</title>
    <style>
        body { font-family: Arial; display: flex; justify-content: center; align-items: center; height: 100vh; background: #f4f4f4; }
        .login-card { background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); width: 300px; }
        input { width: 100%; padding: 10px; margin: 10px 0; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background: #333; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <div class="login-card">
        <h2>Autentificare</h2>
        <?php if(isset($eroare)) echo "<p style='color:red'>$eroare</p>"; ?>
        <form method="POST">
            <input type="email" name="email" placeholder="Email" required>
            <input type="password" name="parola" placeholder="Parolă" required>
            <button type="submit">Intră în cont</button>
        </form>
        <p><a href="index.php">Înapoi la magazin</a></p>
    </div>
</body>
</html>