import axios from 'axios'

const empleadosApi = axios.create({
    baseURL:'http://localhost:8000/sucursal/api/sucursal/'
})


export const getAllEmpleados = () => empleadosApi.get('/')