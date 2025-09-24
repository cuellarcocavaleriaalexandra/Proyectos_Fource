const cart = {};
let descuentoCupon = 0;
let descuentoCliente = 0;

function addToCart(productId, productName, productPrice) {
    const quantityElement = document.getElementById(`quantity-${productId}`);
    const quantity = parseInt(quantityElement.textContent);

    if (quantity === 0) {
        alert("Selecciona una cantidad mayor a 0 para agregar al carrito.");
        return;
    }

    if (!cart[productId]) {
        cart[productId] = {
            name: productName,
            price: productPrice,
            quantity: 0,
            total: 0,
        };
    }

    cart[productId].quantity += quantity;
    cart[productId].total = cart[productId].price * cart[productId].quantity;

    quantityElement.textContent = 0;

    renderCart();
    actualizarTotal();
    saveCart(); // Guardar en localStorage
}

function confirmPurchase() {
    if (Object.keys(cart).length === 0) {
        alert("El carrito está vacío. Agrega productos para continuar.");
        return;
    }

    const data = {
        productos: Object.keys(cart), // IDs de productos
        cantidades: Object.fromEntries(
            Object.entries(cart).map(([id, item]) => [id, item.quantity])
        ),
        codigoCupon: document.getElementById("codigo-cupon").value,
        carnetCliente: document.getElementById("carnet_cliente").value,
    };

    fetch("/confirmar", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRF-TOKEN": document.querySelector('meta[name="csrf-token"]')
                .content,
        },
        body: JSON.stringify(data),
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Error en la respuesta del servidor");
            }
            return response.json();
        })
        .then((data) => {
            if (data.success) {
                localStorage.removeItem("cart"); // Limpiar carrito tras confirmar compra
                window.location.href = `/factura/${data.venta_id}`; // Redirigir a la factura
            } else {
                alert(data.error || "Error al confirmar la compra");
            }
        })
        .catch((error) => alert("Error en la solicitud: " + error.message));
}

function cancelPurchase() {
    if (confirm("¿Estás seguro de que deseas cancelar la compra?")) {
        for (let id in cart) delete cart[id];
        renderCart();
        actualizarTotal();
        localStorage.removeItem("cart"); // Limpiar carrito del localStorage
    }
}

function renderCart() {
    const cartItemsContainer = document.getElementById("cart-items");
    cartItemsContainer.innerHTML = `
<table class="cart-table">
    <thead>
<tr>
    <th>Producto</th>
    <th>Cantidad</th>
    <th>Precio Unitario</th>
    <th>Total</th>
</tr>
    </thead>
    <tbody>
${Object.values(cart)
    .map(
        (item) => `
    <tr>
<td>${item.name}</td>
<td>${item.quantity}</td>
<td>BOB ${item.price.toFixed(2)}</td>
<td>BOB ${item.total.toFixed(2)}</td>
    </tr>
`
    )
    .join("")}
    </tbody>
</table>
    `;
}

function actualizarTotal() {
    let total = 0;

    for (let id in cart) {
        total += cart[id].total;
    }

    // Aplicar los descuentos
    total -= total * (descuentoCupon / 100);
    total -= total * (descuentoCliente / 100);

    document.getElementById(
        "total-amount"
    ).textContent = `Total: BOB ${total.toFixed(2)}`;
}

function toggleCart() {
    const cartSummary = document.querySelector(".cart-summary");
    const cartContent = document.querySelector(".cart-content");

    // Mostrar/ocultar el contenido del carrito
    cartSummary.classList.toggle("expanded");
    cartContent.style.display =
        cartContent.style.display === "none" ? "block" : "none";
}

function aplicarCupon() {
    const codigoCupon = document.getElementById("codigo-cupon").value;

    fetch(`/validar-cupon/${codigoCupon}/`)
        .then((response) => {
            if (!response.ok) {
                throw new Error("Cupón no encontrado o error en el servidor");
            }
            return response.json();
        })
        .then((data) => {
            if (data.valido) {
                descuentoCupon = data.descuento;
                document.getElementById(
                    "descuento_cupon"
                ).textContent = `Descuento Cupón: ${descuentoCupon}%`;
                actualizarTotal();
            } else {
                alert("Cupón no válido.");
            }
        })
        .catch((error) => alert("Error al aplicar el cupón: " + error.message));
}

function aplicarCarnet() {
    const carnetCliente = document.getElementById("carnet_cliente").value;

    fetch(`/validar-carnet/${carnetCliente}/`)
        .then((response) => response.json())
        .then((data) => {
            if (data.existe) {
                descuentoCliente = data.descuento;
                document.getElementById(
                    "descuento_cliente"
                ).textContent = `Descuento Cliente: ${descuentoCliente}%`;
                actualizarTotal();
            } else {
                alert("Carnet no válido.");
            }
        })
        .catch((error) => alert("Error al validar el carnet."));
}

function updateQuantity(productId, change) {
    const productCard = document.querySelector(
        `.product-card[data-product-id="${productId}"]`
    );
    const stock = parseInt(productCard.getAttribute("data-stock"));
    const quantityElement = document.getElementById(`quantity-${productId}`);
    let quantity = parseInt(quantityElement.textContent) + change;

    if (quantity < 0) quantity = 0; // Evitar cantidad negativa

    if (quantity > stock) {
        alert("No hay suficiente stock disponible.");
        return; // Detener si no hay suficiente stock
    }

    quantityElement.textContent = quantity; // Actualizar cantidad
}

document.getElementById("search-form").addEventListener("submit", function (e) {
    e.preventDefault();
    const query = new URLSearchParams(new FormData(this));
    query.delete("categoria"); // Elimina categoría si se hace una búsqueda por nombre
    window.location.href = `?${query.toString()}`;
});

document.querySelectorAll(".categories button").forEach((button) => {
    button.addEventListener("click", function (e) {
        e.preventDefault();
        const form = document.getElementById("category-form");
        const query = new URLSearchParams(new FormData(form));
        query.delete("q"); // Elimina el término de búsqueda si se selecciona una categoría
        query.set("categoria", this.value);
        window.location.href = `?${query.toString()}`;
    });
});

function saveCart() {
    localStorage.setItem("cart", JSON.stringify(cart));
}

function loadCart() {
    const savedCart = localStorage.getItem("cart");
    if (savedCart) {
        Object.assign(cart, JSON.parse(savedCart));
        renderCart();
        actualizarTotal();
    }
}

document.addEventListener("DOMContentLoaded", () => {
    loadCart(); // Cargar carrito desde localStorage al iniciar la página
});
