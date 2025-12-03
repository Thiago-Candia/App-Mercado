/**
 * Configuración centralizada de APIs
 * Cambiar solo aquí las URLs base si cambian los puertos o hosts
 */

export const API_CONFIG = {
    BASE_URL: 'http://localhost:8000',
    
    // URLs de los endpoints
    PRODUCTS: {
        BASE: 'http://localhost:8000/products/api',
        PRODUCTS_ENDPOINT: '/products/',
        CATALOGO_ENDPOINT: '/catalogo/',
        CATEGORIA_ENDPOINT: '/categoria/',
        SUBCATEGORIA_ENDPOINT: '/subcategoria/',
        SEARCH_ENDPOINT: '/products/buscar/'
    },
    
    SALES: {
        BASE: 'http://localhost:8000/ventas/api',
        VENTA_ENDPOINT: '/venta/',
        CLIENTE_ENDPOINT: '/cliente/',
        CAJA_ENDPOINT: '/caja/',
        DETALLEVENTA_ENDPOINT: '/detalleventa/'
    },
    
    SUCURSAL: {
        BASE: 'http://localhost:8000/sucursal/api',
        SUCURSAL_ENDPOINT: '/sucursal/',
        EMPLEADO_ENDPOINT: '/empleado/'
    }
}

export default API_CONFIG
