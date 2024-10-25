document.addEventListener("DOMContentLoaded", function () {
    // Selecciona los elementos clave
    const addToCartButtons = document.querySelectorAll('.boton-item');
    const cartItemsContainer = document.querySelector('.carrito-items');
    const totalPriceElement = document.querySelector('.carrito-precio-total');
    let totalPrice = 0;

    // Añade el evento de "Agregar al carrito" a cada botón
    addToCartButtons.forEach(button => {
        button.addEventListener('click', addToCartClicked);
    });

    // Función que se activa cuando se hace clic en "Agregar al carrito"
    function addToCartClicked(event) {
        const button = event.target;
        const productItem = button.closest('.item');
        const title = productItem.querySelector('.titulo-item').textContent;
        const price = parseFloat(productItem.querySelector('.precio-item').textContent.replace('$', '').replace('.', ''));
        const imageSrc = productItem.querySelector('.img-item').src;

        addItemToCart(title, price, imageSrc);
        updateCartTotal();
    }

    // Añade el producto al carrito
    function addItemToCart(title, price, imageSrc) {
        const cartRow = document.createElement('div');
        cartRow.classList.add('carrito-item');

        // Verificar si el producto ya está en el carrito
        const cartItemNames = cartItemsContainer.querySelectorAll('.carrito-item-titulo');
        for (let i = 0; i < cartItemNames.length; i++) {
            if (cartItemNames[i].textContent === title) {
                alert('Este producto ya está en el carrito');
                return;
            }
        }

        // Estructura del producto en el carrito
        const cartRowContents = `
            <img src="${imageSrc}" alt="" class="carrito-item-img">
            <span class="carrito-item-titulo">${title}</span>
            <div class="selector-cantidad">
                <i class="fa fa-minus-circle"></i>
                <span class="carrito-item-cantidad">1</span>
                <i class="fa fa-plus-circle"></i>
            </div>
            <span class="carrito-item-precio">$${price.toLocaleString()}</span>
            <button class="btn-eliminar">X</button>
        `;

        cartRow.innerHTML = cartRowContents;
        cartItemsContainer.append(cartRow);

        // Agregar manejadores de eventos para eliminar y cambiar la cantidad
        cartRow.querySelector('.btn-eliminar').addEventListener('click', removeCartItem);
        cartRow.querySelector('.fa-minus-circle').addEventListener('click', decreaseQuantity);
        cartRow.querySelector('.fa-plus-circle').addEventListener('click', increaseQuantity);
    }

    // Actualiza el total del carrito
    function updateCartTotal() {
        const cartRows = cartItemsContainer.querySelectorAll('.carrito-item');
        totalPrice = 0;
        cartRows.forEach(row => {
            const priceElement = row.querySelector('.carrito-item-precio');
            const quantityElement = row.querySelector('.carrito-item-cantidad');
            const price = parseFloat(priceElement.textContent.replace('$', '').replace('.', ''));
            const quantity = parseInt(quantityElement.textContent);
            totalPrice += price * quantity;
        });

        totalPriceElement.textContent = `$${totalPrice.toLocaleString()}`;
    }

    // Elimina un producto del carrito
    function removeCartItem(event) {
        const buttonClicked = event.target;
        buttonClicked.closest('.carrito-item').remove();
        updateCartTotal();
    }

    // Disminuye la cantidad de un producto
    function decreaseQuantity(event) {
        const buttonClicked = event.target;
        const quantityElement = buttonClicked.nextElementSibling;
        let quantity = parseInt(quantityElement.textContent);
        if (quantity > 1) {
            quantityElement.textContent = quantity - 1;
            updateCartTotal();
        }
    }

    // Aumenta la cantidad de un producto
    function increaseQuantity(event) {
        const buttonClicked = event.target;
        const quantityElement = buttonClicked.previousElementSibling;
        let quantity = parseInt(quantityElement.textContent);
        quantityElement.textContent = quantity + 1;
        updateCartTotal();
    }

    // Manejador del botón de pago
    const payButton = document.querySelector('.btn-pagar');
    payButton.addEventListener('click', function () {
        alert('Usted ha comprado exitosamente');
    });
});
