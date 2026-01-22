<?php
$host = "mysql";      // Numele serviciului din docker-compose.yml
$user = "root";       // Utilizatorul setat în yml
$pass = "root";       // Parola root setată în yml (MYSQL_ROOT_PASSWORD)
$db   = "magazin_muzica"; // Numele bazei de date din yml

// Aici se creează variabila $conn
$conn = mysqli_connect($host, $user, $pass, $db);
mysqli_set_charset($conn, "utf8mb4");
// Verificăm dacă variabila s-a creat cu succes
if (!$conn) {
    die("Conexiune eșuată la baza de date: " . mysqli_connect_error());
}
?>