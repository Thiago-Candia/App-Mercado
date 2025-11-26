import React, { useEffect, useState } from 'react'
import { getAllProducts } from '../api/api.products.js'
import ProductCard from './ProductCard.jsx'


export const ProductList = ({ products }) => {

const [allProducts, setAllProducts] = useState([])


/* Llamada a la API para cargar los productos */
useEffect(() => {
    async function loadProducts(){
    const res = await getAllProducts()
    setAllProducts(res.data)
    }
    loadProducts()
}, [])

//SI HAY PRODUCTOS FILTRADOS SE MUESTRAN
const shownProducts = products && products.length > 0 ? products : allProducts

    return (
    <div>
        <h2>Productos</h2>
        <div className='product-list'>
        {shownProducts.map((product) => (
            <ProductCard key={product.id} product={product} />
        ))}
        </div>
    </div>
    )
}

export default ProductList