import React from 'react'
import { useNavigate } from 'react-router-dom'

    
function ProductCard({product}){

    const navigate = useNavigate()

    return (
        <div key={product.id} onClick={() => { navigate(`/product/${product.id}`) }}>
            <h1>{product.name}</h1>
            <p>{product.description}</p>
        <hr />
        </div>
    )
}


export default ProductCard
