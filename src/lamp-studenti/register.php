<?php
include 'db.php';

$mesaj = "";

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $nume = mysqli_real_escape_string($conn, $_POST['username']);
    $email = mysqli_real_escape_string($conn, $_POST['email']);
    $parola = $_POST['parola']; // Într-un proiect real folosim password_hash

    // 1. Verificăm dacă email-ul există deja
    $verificare = mysqli_query($conn, "SELECT * FROM utilizatori WHERE email = '$email'");
    
    if (mysqli_num_rows($verificare) > 0) {
        $mesaj = "<p style='color:red'>Acest email este deja folosit!</p>";
    } else {
        // 2. Inserăm utilizatorul nou (rolul implicit va fi 'user')
        $sql = "INSERT INTO utilizatori (username, parola, email, rol) VALUES ('$username', '$parola', '$email', 'user')";
        
        // ... codul tău anterior ...
$sql = "INSERT INTO utilizatori (username, email, parola, rol) VALUES ('$nume', '$email', '$parola', 'user')";

// ADAUGĂ ACEASTĂ LINIE PENTRU TEST:
echo "DEBUG SQL: " . $sql; 

if (mysqli_query($conn, $sql)) {
// ... restul codului ...
            $mesaj = "<p style='color:green'>Cont creat cu succes! <a href='login.php'>Loghează-te aici</a></p>";
        } else {
            $mesaj = "<p style='color:red'>Eroare la înregistrare: " . mysqli_error($conn) . "</p>";
        } 
    }
}
?>

<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <title>Înregistrare - MusicShop</title>
    <link rel="stylesheet" href="css/style.css">
    <style>
        .register-box { width: 300px; margin: 80px auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; text-align: center; font-family: Arial; }
        input { width: 90%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; }
        button { width: 95%; padding: 10px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #218838; }
    </style>
</head>
<body>
    <div class="register-box">
        <h2>Cont Nou</h2>
        <?php echo $mesaj; ?>
        <form method="POST">
            <input type="text" name="nume" placeholder="Nume Complet" required>
            <input type="email" name="email" placeholder="Adresa Email" required>
            <input type="password" name="parola" placeholder="Parolă" required>
            <button type="submit">Creează Cont</button>
        </form>
        <p>Ai deja cont? <a href="login.php">Loghează-te</a></p>
        <p><a href="index.php">Înapoi la magazin</a></p>
    </div>
</body>
</html>