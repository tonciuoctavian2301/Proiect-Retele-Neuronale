<?php
session_start();
session_destroy(); // Șterge toate datele din sesiune
header("Location: index.php");
exit();
?>