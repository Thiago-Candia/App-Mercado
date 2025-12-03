import React from 'react';
import { useCart } from '../context/CartContext';

function CartButton() {
    const { getTotalItems, toggleCart } = useCart();

    return (
        <button className="cart-button" onClick={toggleCart}>
            🛒 Carrito ({getTotalItems()})
        </button>
    );
}

export default CartButton;