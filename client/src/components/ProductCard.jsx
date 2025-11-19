import React from 'react'
import { useNavigate } from 'react-router-dom'





function ProductCard({product}){

    const navigate = useNavigate()

    return (
        <div className='product-card' key={product.id} onClick={() => { navigate(`/product/${product.id}`) }}>
            <div className='product-image-container'>
                <img src={product.image} alt="" />
            </div>
            <h3>{product.name}</h3>
            <div>
                {product.price}
            </div>
        </div>
    )
}


export default ProductCard