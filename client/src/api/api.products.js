import axios from 'axios'

const API_URL = 'http://localhost:8000/products/api'

export const productsApi = axios.create({
    baseURL: API_URL
})

// ===== PRODUCTOS =====
export const getAllProducts = () => productsApi.get('/products/')

export const getProduct = (id) => productsApi.get(`/products/${id}/`)

export const searchProducts = (query) => productsApi.get(`/products/buscar/?search=${query}`)

export const updateProduct = (id, data) => productsApi.put(`/products/${id}/`, data)

export const createProduct = (data) => productsApi.post('/products/', data)

export const deleteProduct = (id) => productsApi.delete(`/products/${id}/`)

// ===== CATÁLOGOS =====
export const getAllCatalogos = () => productsApi.get('/catalogo/')

export const getCatalogo = (id) => productsApi.get(`/catalogo/${id}/`)

export const createCatalogo = (data) => productsApi.post('/catalogo/', data)

export const updateCatalogo = (id, data) => productsApi.put(`/catalogo/${id}/`, data)

export const deleteCatalogo = (id) => productsApi.delete(`/catalogo/${id}/`)

// ===== CATEGORÍAS =====
export const getAllCategorias = () => productsApi.get('/categoria/')

export const getCategoria = (id) => productsApi.get(`/categoria/${id}/`)

export const createCategoria = (data) => productsApi.post('/categoria/', data)

export const updateCategoria = (id, data) => productsApi.put(`/categoria/${id}/`, data)

export const deleteCategoria = (id) => productsApi.delete(`/categoria/${id}/`)

// ===== SUBCATEGORÍAS =====
export const getAllSubcategorias = () => productsApi.get('/subcategoria/')

export const getSubcategoria = (id) => productsApi.get(`/subcategoria/${id}/`)

export const createSubcategoria = (data) => productsApi.post('/subcategoria/', data)

export const updateSubcategoria = (id, data) => productsApi.put(`/subcategoria/${id}/`, data)

export const deleteSubcategoria = (id) => productsApi.delete(`/subcategoria/${id}/`)