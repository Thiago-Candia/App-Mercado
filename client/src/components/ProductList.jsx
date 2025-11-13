import React, { useEffect, useState } from 'react'
import { getAllProducts } from '../api/api.products.js'
import ProductCard from './ProductCard.jsx'


export const ProductList = () => {

const [products, setProducts] = useState([])


useEffect(() => {
    async function loadProducts(){
    const res = await getAllProducts()
    setProducts(res.data)
    }
    loadProducts()
}, [])


    return (
    <div>
        <h2>Productos</h2>
        <div className=''>
        {products.map((product) => (
            <ProductCard key={product.id} product={product} />
        ))}
        </div>
    </div>
    )
}

export default ProductList