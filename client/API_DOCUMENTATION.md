# Documentación de APIs - App Mercado

## 📋 Índice
- [Estructura de APIs](#estructura-de-apis)
- [Endpoints Disponibles](#endpoints-disponibles)
- [Configuración](#configuración)
- [Ejemplos de Uso](#ejemplos-de-uso)

---

## Estructura de APIs

Las APIs se encuentran en la carpeta `src/api/` y están organizadas por módulo:

```
src/api/
├── api.products.js      # APIs de productos
├── api.sales.js         # APIs de ventas
└── api.sucursal.js      # APIs de sucursal y empleados
```

---

## Endpoints Disponibles

### 🛍️ PRODUCTOS (api.products.js)

Base URL: `http://localhost:8000/products/api`

| Función | Método | Endpoint |
|---------|--------|----------|
| `getAllProducts()` | GET | `/products/` |
| `getProduct(id)` | GET | `/products/{id}/` |
| `searchProducts(query)` | GET | `/products/buscar/?search={query}` |
| `createProduct(data)` | POST | `/products/` |
| `updateProduct(id, data)` | PUT | `/products/{id}/` |
| `deleteProduct(id)` | DELETE | `/products/{id}/` |

**Catálogos:**
| `getAllCatalogos()` | GET | `/catalogo/` |
| `getCatalogo(id)` | GET | `/catalogo/{id}/` |
| `createCatalogo(data)` | POST | `/catalogo/` |
| `updateCatalogo(id, data)` | PUT | `/catalogo/{id}/` |
| `deleteCatalogo(id)` | DELETE | `/catalogo/{id}/` |

**Categorías:**
| `getAllCategorias()` | GET | `/categoria/` |
| `getCategoria(id)` | GET | `/categoria/{id}/` |
| `createCategoria(data)` | POST | `/categoria/` |
| `updateCategoria(id, data)` | PUT | `/categoria/{id}/` |
| `deleteCategoria(id)` | DELETE | `/categoria/{id}/` |

**Subcategorías:**
| `getAllSubcategorias()` | GET | `/subcategoria/` |
| `getSubcategoria(id)` | GET | `/subcategoria/{id}/` |
| `createSubcategoria(data)` | POST | `/subcategoria/` |
| `updateSubcategoria(id, data)` | PUT | `/subcategoria/{id}/` |
| `deleteSubcategoria(id)` | DELETE | `/subcategoria/{id}/` |

---

### 💰 VENTAS (api.sales.js)

Base URL: `http://localhost:8000/ventas/api`

**Ventas:**
| Función | Método | Endpoint |
|---------|--------|----------|
| `getVentas()` | GET | `/venta/` |
| `getVentaById(id)` | GET | `/venta/{id}/` |
| `createVenta(data)` | POST | `/venta/` |
| `cobrarVenta(ventaId, data)` | POST | `/venta/{id}/cobrar_venta/` |
| `aplicarDescuento(ventaId, data)` | POST | `/venta/{id}/hacer_descuento/` |

**Clientes:**
| `getClientes()` | GET | `/cliente/` |
| `createCliente(data)` | POST | `/cliente/` |

**Cajas:**
| `getCajas()` | GET | `/caja/` |
| `getCajaActiva()` | GET | `/caja/` (filtra por estado='ACT') |

**Detalles de Venta:**
| `createDetalleVenta(data)` | POST | `/detalleventa/` |

**Funciones Especiales:**
| `procesarVentaCompleta(items, formData)` | POST | Crea venta + detalles + cobro en una sola llamada |

---

### 🏢 SUCURSAL (api.sucursal.js)

Base URL: `http://localhost:8000/sucursal/api`

**Sucursales:**
| Función | Método | Endpoint |
|---------|--------|----------|
| `getAllSucursales()` | GET | `/sucursal/` |
| `getSucursal(id)` | GET | `/sucursal/{id}/` |
| `createSucursal(data)` | POST | `/sucursal/` |
| `updateSucursal(id, data)` | PUT | `/sucursal/{id}/` |
| `deleteSucursal(id)` | DELETE | `/sucursal/{id}/` |

**Empleados:**
| `getAllEmpleados()` | GET | `/empleado/` |
| `getEmpleado(id)` | GET | `/empleado/{id}/` |
| `createEmpleado(data)` | POST | `/empleado/` |
| `updateEmpleado(id, data)` | PUT | `/empleado/{id}/` |
| `deleteEmpleado(id)` | DELETE | `/empleado/{id}/` |

---

## Configuración

### URLs Base

Las URLs base están configuradas en cada archivo de API:

```javascript
// api.products.js
const API_URL = 'http://localhost:8000/products/api'

// api.sales.js
const API_URL = 'http://localhost:8000/ventas/api'

// api.sucursal.js
const API_URL = 'http://localhost:8000/sucursal/api'
```

Para cambiar las URLs, edita solo las constantes `API_URL` en cada archivo.

### Configuración Centralizada

También existe un archivo `config/apiConfig.js` con todas las URLs para referencia:

```javascript
import API_CONFIG from '../config/apiConfig'

console.log(API_CONFIG.PRODUCTS.BASE)  // http://localhost:8000/products/api
console.log(API_CONFIG.SALES.BASE)     // http://localhost:8000/ventas/api
```

---

## Ejemplos de Uso

### Obtener todos los productos

```javascript
import { getAllProducts } from '../api/api.products'

async function loadProducts() {
    try {
        const response = await getAllProducts()
        console.log(response.data) // Array de productos
    } catch (error) {
        console.error('Error:', error)
    }
}
```

### Buscar productos

```javascript
import { searchProducts } from '../api/api.products'

async function searchByName(query) {
    try {
        const response = await searchProducts('laptop')
        console.log(response.data) // Productos que coinciden
    } catch (error) {
        console.error('Error:', error)
    }
}
```

### Crear una venta completa

```javascript
import { procesarVentaCompleta } from '../api/api.sales'

const cartItems = [
    { id: 1, name: 'Producto 1', price: 100, cantidad: 2 },
    { id: 2, name: 'Producto 2', price: 50, cantidad: 1 }
]

const formData = {
    caja_id: 1,
    cliente_nombre: 'Juan Pérez',
    cliente_dni: '12345678',
    metodo_pago: 'EFE',
    monto_recibido: 250
}

async function completarCompra() {
    try {
        const resultado = await procesarVentaCompleta(cartItems, formData)
        console.log('Venta realizada:', resultado.venta.numero_venta)
        console.log('Cambio:', resultado.cobro.cambio)
    } catch (error) {
        console.error('Error al procesar venta:', error)
    }
}
```

### Obtener caja activa

```javascript
import { getCajaActiva } from '../api/api.sales'

async function obtenerCaja() {
    try {
        const caja = await getCajaActiva()
        if (caja) {
            console.log('Caja activa:', caja.numeroCaja)
        } else {
            console.log('No hay caja activa')
        }
    } catch (error) {
        console.error('Error:', error)
    }
}
```

### Crear empleado

```javascript
import { createEmpleado } from '../api/api.sucursal'

async function nuevoEmpleado() {
    try {
        const response = await createEmpleado({
            nombre: 'Carlos',
            apellido: 'García',
            dni: 87654321,
            cargo: 'VEN', // Vendedor
            sucursal_id: 1
        })
        console.log('Empleado creado:', response.data)
    } catch (error) {
        console.error('Error:', error)
    }
}
```

---

## Manejo de Errores

Todas las funciones incluyen manejo de errores:

```javascript
try {
    const response = await getAllProducts()
    // Procesar respuesta
} catch (error) {
    console.error('Error al obtener productos:', error)
    // Mostrar mensaje al usuario
}
```

Los errores comunes incluyen:
- **404**: Recurso no encontrado
- **400**: Solicitud inválida
- **500**: Error del servidor
- **Network Error**: Servidor no disponible

---

## Status del Carrito

El carrito está completamente integrado y utiliza:

- `CartContext` para estado global
- `localStorage` para persistencia
- APIs de sales para procesar ventas

**Flujo de compra:**
1. Usuario agrega productos al carrito
2. Abre el carrito lateral
3. Ajusta cantidades si es necesario
4. Hace clic en "Finalizar Compra"
5. Se abre la página de checkout
6. Completa datos del cliente (opcional)
7. Selecciona método de pago
8. Ingresa monto recibido
9. Hace clic en "Confirmar Compra"
10. Se procesa la venta completa

---

## Próximos Pasos

- Implementar autenticación de usuarios
- Agregar validación de datos en cliente
- Implementar manejo de errores mejorado
- Agregar paginación a endpoints
- Implementar filtros avanzados

---

**Última actualización:** 27 de Noviembre de 2025
