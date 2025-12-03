import axios from 'axios'

const API_URL = 'http://localhost:8000/sucursal/api'

export const sucursalApi = axios.create({
    baseURL: API_URL
})

// ===== SUCURSALES =====
export const getAllSucursales = () => sucursalApi.get('/sucursal/')

export const getSucursal = (id) => sucursalApi.get(`/sucursal/${id}/`)

export const createSucursal = (data) => sucursalApi.post('/sucursal/', data)

export const updateSucursal = (id, data) => sucursalApi.put(`/sucursal/${id}/`, data)

export const deleteSucursal = (id) => sucursalApi.delete(`/sucursal/${id}/`)

// ===== EMPLEADOS =====
export const getAllEmpleados = () => sucursalApi.get('/empleado/')

export const getEmpleado = (id) => sucursalApi.get(`/empleado/${id}/`)

export const createEmpleado = (data) => sucursalApi.post('/empleado/', data)

export const updateEmpleado = (id, data) => sucursalApi.put(`/empleado/${id}/`, data)

export const deleteEmpleado = (id) => sucursalApi.delete(`/empleado/${id}/`)