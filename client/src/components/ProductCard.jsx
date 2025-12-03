import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useCart } from '../context/CartContext'


function ProductCard({ product }){


    //funcin addToCart de CartContext
    const { addToCart } = useCart()

    const navigate = useNavigate()

    const handleAddToCart = (e) => {
        e.stopPropagation()
        addToCart(product)
    }

    return (
        <div className='product-card' key={product.id} onClick={() => { navigate(`/product/${product.id}`) }}>
            <div className='product-image-container'>
                <img src={product.image} alt="" />
            </div>
            <h3>{product.name}</h3>
            <div className='product-price-container'>
                <span className='product-price'>${product.price}</span>
            </div>
            <button
                className='add-to-cart-btn'
                onClick={handleAddToCart}
            >
                🛒 Agregar al carrito
            </button>
        </div>
    )
}


export default ProductCard