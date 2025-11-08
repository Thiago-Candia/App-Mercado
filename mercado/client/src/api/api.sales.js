import axios from 'axios'

export const salesApi = axios.create({
    baseURL:'http://localhost:8000/sales/api/sales/'
})

export const getAllSales = () => salesApi.get('/')

export const postSales = (sale) => salesApi.post('/', sale)