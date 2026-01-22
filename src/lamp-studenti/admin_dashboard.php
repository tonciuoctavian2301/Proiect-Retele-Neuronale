<?php
session_start();
if (!isset($_SESSION['utilizator_rol']) || $_SESSION['utilizator_rol'] !== 'admin') {
    die("Acces interzis! Această pagină este doar pentru administratori.");
}
?>
<h1>Panou de Control Admin</h1>
<p>Salut, <?php echo $_SESSION['utilizator_nume']; ?>! Aici poți gestiona magazinul.</p>
<a href="index.php">Înapoi la site</a>