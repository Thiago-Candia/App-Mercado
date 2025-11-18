import React, { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { getProduct } from '../api/api.products'

const ProductPage = () => {

  const navigate = useNavigate()
  const params = useParams()

  const [product, setProduct] = useState(null)

  useEffect(() => {
    async function loadProduct(){
      if(!params.id) navigate('/')
      if(params.id){
        const res = await getProduct(params.id) 
        setProduct(res.data)
      }
    }
    loadProduct()
  }, [])


  if(!product) return null

  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
    </div>
  )
}

export default ProductPage