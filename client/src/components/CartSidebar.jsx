import React from 'react'
import { useCart } from '../context/CartContext'
import { useNavigate } from 'react-router-dom'
import '../styles/cart-sidebar.css'

const CartSidebar = () => {
    const { 
        cart, 
        removeFromCart, 
        incrementQuantity, 
        decrementQuantity, 
        getTotal, 
        toggleCart 
    } = useCart()
    const navigate = useNavigate()

    const handleCheckout = () => {
        if (cart.length === 0) {
            alert('El carrito está vacío')
            return
        }
        toggleCart()
        navigate('/checkout')
    }

    return (
        <div className="cart-sidebar-overlay" onClick={toggleCart}>
            <div className="cart-sidebar" onClick={(e) => e.stopPropagation()}>
                <div className="cart-sidebar-header">
                    <h2>🛒 Mi Carrito</h2>
                    <button className="cart-close-btn" onClick={toggleCart}>✕</button>
                </div>

                {cart.length === 0 ? (
                    <div className="cart-empty">
                        <p>Tu carrito está vacío</p>
                        <button onClick={toggleCart} className="continue-shopping-btn">
                            Continuar comprando
                        </button>
                    </div>
                ) : (
                    <>
                        <div className="cart-items-list">
                            {cart.map((item) => (
                                <div key={item.id} className="cart-item">
                                    <img src={item.image} alt={item.name} className="cart-item-image" />
                                    
                                    <div className="cart-item-details">
                                        <h4>{item.name}</h4>
                                        <p className="cart-item-price">${parseFloat(item.price).toFixed(2)}</p>
                                    </div>

                                    <div className="cart-item-quantity">
                                        <button 
                                            className="qty-btn"
                                            onClick={() => decrementQuantity(item.id)}
                                        >
                                            −
                                        </button>
                                        <span className="qty-display">{item.cantidad}</span>
                                        <button 
                                            className="qty-btn"
                                            onClick={() => incrementQuantity(item.id)}
                                        >
                                            +
                                        </button>
                                    </div>

                                    <div className="cart-item-total">
                                        ${(parseFloat(item.price) * item.cantidad).toFixed(2)}
                                    </div>

                                    <button 
                                        className="cart-remove-btn"
                                        onClick={() => removeFromCart(item.id)}
                                        title="Eliminar del carrito"
                                    >
                                        🗑️
                                    </button>
                                </div>
                            ))}
                        </div>

                        <div className="cart-sidebar-footer">
                            <div className="cart-total">
                                <h3>Total: ${getTotal().toFixed(2)}</h3>
                            </div>
                            
                            <button 
                                className="checkout-btn"
                                onClick={handleCheckout}
                            >
                                Finalizar Compra
                            </button>
                            
                            <button 
                                className="continue-shopping-btn"
                                onClick={toggleCart}
                            >
                                Continuar comprando
                            </button>
                        </div>
                    </>
                )}
            </div>
        </div>
    )
}

export default CartSidebar
