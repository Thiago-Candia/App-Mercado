import axios from 'axios'

const productsApi = axios.create({
    baseURL:'http://localhost:8000/products/api/products/'
})

export const getAllProducts = () => productsApi.get('/')
export const getProduct = (id) => productsApi.get(`/${id}/`)