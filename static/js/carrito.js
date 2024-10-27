document.addEventListener("DOMContentLoaded", function () {
    const cartItemsContainer = document.querySelector('.carrito-items');
    const totalPriceElement = document.querySelector('.carrito-precio-total');
    const payButton = document.querySelector('.btn-pagar');
    let totalPrice = 0;

    // Añadir eventos a los botones de eliminar, sumar y restar cantidad para los productos ya en el carrito
    cartItemsContainer.querySelectorAll('.carrito-item').forEach(cartItem => {
        cartItem.querySelector('.btn-eliminar').addEventListener('click', removeCartItem);
        cartItem.querySelector('.restar-cantidad').addEventListener('click', decreaseQuantity);
        cartItem.querySelector('.sumar-cantidad').addEventListener('click', increaseQuantity);
    });

    // Función para actualizar el total del carrito
    function updateCartTotal() {
        totalPrice = 0;
        cartItemsContainer.querySelectorAll('.carrito-item').forEach(cartItem => {
            const priceElement = cartItem.querySelector('.carrito-item-precio');
            const quantityElement = cartItem.querySelector('.carrito-item-cantidad');
            const price = parseFloat(priceElement.textContent.replace('CLP', '').replace('$', '').trim().replace('.', ''));
            const quantity = parseInt(quantityElement.textContent);
            totalPrice += price * quantity;
        });

        // Formatear el precio total como "$55.790" y asignarlo al elemento del total
        totalPriceElement.textContent = formatCurrency(totalPrice);
    }

    // Función para formatear en estilo $55.790 sin decimales
    function formatCurrency(amount) {
        return `$${amount.toLocaleString("es-CL", { minimumFractionDigits: 0 })}`;
    }

    // Eliminar un producto del carrito
    function removeCartItem(event) {
        event.target.closest('.carrito-item').remove();
        updateCartTotal();
    }

    // Disminuir la cantidad de un producto
    function decreaseQuantity(event) {
        const quantityElement = event.target.nextElementSibling;
        let quantity = parseInt(quantityElement.textContent);
        if (quantity > 1) {
            quantityElement.textContent = quantity - 1;
            updateCartTotal();
        } else {
            alert("La cantidad no puede ser menor a 1.");
        }
    }

    // Aumentar la cantidad de un producto
    function increaseQuantity(event) {
        const quantityElement = event.target.previousElementSibling;
        let quantity = parseInt(quantityElement.textContent);
        quantityElement.textContent = quantity + 1;
        updateCartTotal();
    }

    // Función de pago
    if (payButton) {
        payButton.addEventListener('click', function () {
            alert('Gracias por su compra');
            cartItemsContainer.innerHTML = ''; // Vacía el carrito
            updateCartTotal();
        });
    }
});
