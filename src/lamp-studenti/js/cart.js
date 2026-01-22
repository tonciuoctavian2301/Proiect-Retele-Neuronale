/* === LOGICA PENTRU COȘUL DE CUMPĂRĂTURI === */

// Așteaptă ca întregul document HTML să fie încărcat înainte de a rula scriptul
document.addEventListener('DOMContentLoaded', () => {

    // --- Funcții de bază ---

    /**
     * Ia coșul din localStorage (memoria browserului).
     * @returns {Array} Un array de obiecte (produse) sau un array gol.
     */
    function getCart() {
        return JSON.parse(localStorage.getItem('cart')) || [];
    }

    /**
     * Salvează coșul în localStorage.
     * @param {Array} cart - Array-ul de produse.
     */
    function saveCart(cart) {
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartCount(); // Actualizează și numărul din header
    }

    /**
     * Actualizează numărul de produse afișat în header.
     */
    function updateCartCount() {
        const cartCountElement = document.getElementById('cart-count');
        if (cartCountElement) {
            cartCountElement.textContent = getCart().length;
        }
    }

    /**
     * Adaugă un produs în coș.
     * @param {Event} e - Evenimentul de click de la buton.
     */
    function addToCart(e) {
        // Ia datele produsului de pe atributele `data-*` ale butonului
        const button = e.target;
        const product = {
            id: button.dataset.id,
            name: button.dataset.name,
            price: parseFloat(button.dataset.price),
            image: button.dataset.image
        };

        const cart = getCart();
        cart.push(product); // Adaugă noul produs în array
        saveCart(cart); // Salvează noul coș

        alert(`${product.name} a fost adăugat în coș!`); // Confirmare vizuală
    }


    // --- Logica pentru Pagina `cos.html` ---

    /**
     * Afișează produsele pe pagina coșului.
     */
    function displayCart() {
        const cart = getCart();
        const cartContainer = document.getElementById('cart-container');
        const cartTotalElement = document.getElementById('cart-total');
        
        if (!cartContainer) return; // Ieși dacă nu suntem pe pagina cos.html

        cartContainer.innerHTML = ''; // Golește containerul
        let total = 0;

        if (cart.length === 0) {
            cartContainer.innerHTML = '<p>Coșul tău este gol.</p>';
        } else {
            // Creează un card pentru fiecare produs din coș
            cart.forEach((product, index) => {
                total += product.price;
                const productElement = document.createElement('div');
                productElement.classList.add('cart-item');
                productElement.innerHTML = `
                    <img src="${product.image}" alt="${product.name}" class="cart-item-image">
                    <div class="cart-item-details">
                        <h3>${product.name}</h3>
                        <p>${product.price.toFixed(2)} RON</p>
                    </div>
                    <button class="remove-from-cart-btn" data-index="${index}">Șterge</button>
                `;
                cartContainer.appendChild(productElement);
            });
        }
        
        // Actualizează prețul total
        cartTotalElement.textContent = total.toFixed(2);

        // Adaugă funcționalitate pe butoanele "Șterge"
        document.querySelectorAll('.remove-from-cart-btn').forEach(button => {
            button.addEventListener('click', removeFromCart);
        });
    }

    /**
     * Șterge un produs din coș.
     * @param {Event} e - Evenimentul de click de la buton.
     */
    function removeFromCart(e) {
        const indexToRemove = parseInt(e.target.dataset.index);
        let cart = getCart();
        cart.splice(indexToRemove, 1); // Șterge elementul de la indexul respectiv
        saveCart(cart);
        displayCart(); // Re-afișează coșul
    }

    /**
     * Golește complet coșul.
     */
    function clearCart() {
        if (confirm('Ești sigur că vrei să golești coșul?')) {
            saveCart([]); // Salvează un coș gol
            displayCart(); // Re-afișează
        }
    }


    // --- Inițializare ---

    // 1. Actualizează numărul din header pe orice pagină
    updateCartCount();

    // 2. Adaugă event listeners pentru butoanele "Adaugă în coș" (pe paginile de produs)
    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', addToCart);
    });

    // 3. Dacă suntem pe pagina `cos.html`, afișează coșul
    if (document.getElementById('cart-container')) {
        displayCart();

        // Adaugă event listener pentru "Golește Coșul"
        const clearCartBtn = document.querySelector('.clear-cart-btn');
        if (clearCartBtn) {
            clearCartBtn.addEventListener('click', clearCart);
        }

        // Adaugă event listener pentru "Finalizează Comanda" (momentan doar afișează o alertă)
        const checkoutBtn = document.querySelector('.checkout-btn');
        if (checkoutBtn) {
            checkoutBtn.addEventListener('click', () => {
                if(getCart().length > 0) {
                    alert('Mulțumim pentru comandă! (Acesta este sfârșitul demo-ului)');
                    saveCart([]);
                    displayCart();
                } else {
                    alert('Coșul tău este gol.');
                }
            });
        }
    }
});