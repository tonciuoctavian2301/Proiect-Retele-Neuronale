<?php
// 1. Începem sesiunea - trebuie să fie prima linie din fișier!
include 'db.php';
session_start();

// 2. Includem conexiunea la baza de date (opțional aici, dar util dacă vrei să afișezi produse)
// include 'db.php'; 
?>

<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Magazin Instrumente Muzicale</title>
    <link rel="stylesheet" href="css/style.css"> 
    <style>
        /* Câteva stiluri rapide pentru meniu */
        nav { background: #333; color: white; padding: 1rem; display: flex; justify-content: space-between; }
        nav a { color: white; text-decoration: none; margin: 0 10px; }
        .user-zone { font-weight: bold; color: #ffcc00; }
        .container { padding: 20px; text-align: center; }
        .instrument-grid { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-top: 30px; }
        .card { border: 1px solid #ddd; padding: 10px; width: 200px; border-radius: 8px; }
        .card img { width: 100%; height: auto; border-radius: 5px; }
    </style>
</head>
<body>

    <nav>
        <div class="logo">
            <a href="index.php"><strong>MusicShop</strong></a>
        </div>
        
        <div class="menu">
            <a href="chitare.html">Chitare</a>
            <a href="clape.html">Clape</a>
            <a href="percutie.html">Percuție</a>
            <a href="cosultau.html">Coșul meu</a>
        </div>

        <div class="auth-buttons">
            <?php if (isset($_SESSION['utilizator_nume'])): ?>
                <span class="user-zone">Salut, <?php echo htmlspecialchars($_SESSION['utilizator_nume']); ?>!</span>
                <a href="admin_dashboard.php" style="font-size: 0.8em;">Panou</a>
                <a href="logout.php" style="color: #ff4444;">Ieșire</a>
            <?php else: ?>
                <a href="login.php">Login</a>
                <a href="register.php">Înregistrare</a>
            <?php endif; ?>
        </div>
    </nav>

    <div class="container">
        <h1>Bun venit la Magazinul de Instrumente Muzicale</h1>
        <p>Alege instrumentul preferat din categoriile de mai jos.</p>

        <div class="instrument-grid">

    <?php
    // Interogăm baza de date
    $query = "SELECT * FROM categorii";
    $rezultat = mysqli_query($conn, $query);

    // Bucla care generează cardurile automat
    while($row = mysqli_fetch_assoc($rezultat)) {
        ?>
        <div class="card">
            <img src="<?php echo $row['imagine']; ?>" alt="<?php echo $row['nume']; ?>">
            <h3><?php echo $row['nume']; ?></h3>
            <a href="categorie.php?id=<?php echo $row['id']; ?>">Vezi detalii</a>
        </div>
        <?php
    }
    ?>

</div>
    </div>

    <hr>
    <footer style="text-align: center; padding: 20px;">
        <p>&copy; <?php echo date("Y"); ?> Proiect Instrumente Muzicale - Toate drepturile rezervate.</p>
    </footer>

</body>
</html>