# 🚀 APIs - App Mercado

Directorio que contiene todas las integraciones de APIs con el backend Django.

## 📁 Estructura

```
api/
├── api.products.js      # Operaciones CRUD de Productos
├── api.sales.js         # Operaciones CRUD de Ventas, Clientes, Cajas
├── api.sucursal.js      # Operaciones CRUD de Sucursales, Empleados
└── apiTesting.js        # Herramientas de prueba y testing
```

## 🔗 Endpoints por Módulo

### Productos (`api.products.js`)
- **Base:** `http://localhost:8000/products/api`
- Productos, Catálogos, Categorías, Subcategorías

### Ventas (`api.sales.js`)
- **Base:** `http://localhost:8000/ventas/api`
- Ventas, Clientes, Cajas, Detalles de Venta

### Sucursal (`api.sucursal.js`)
- **Base:** `http://localhost:8000/sucursal/api`
- Sucursales, Empleados

## 🧪 Testing

Para probar todas las APIs:

1. Abre la consola del navegador (F12)
2. Ejecuta: `APITesting.testAllAPIs()`

Pruebas individuales:
```javascript
APITesting.testProductsAPIs()
APITesting.testSalesAPIs()
APITesting.testSucursalAPIs()
```

## 📝 Importación

```javascript
// Productos
import { getAllProducts, getProduct, searchProducts } from '../api/api.products'

// Ventas
import { getVentas, getCajaActiva, procesarVentaCompleta } from '../api/api.sales'

// Sucursal
import { getAllEmpleados, getAllSucursales } from '../api/api.sucursal'
```

## ⚙️ Configuración

Las URLs base están definidas en cada archivo:

```javascript
const API_URL = 'http://localhost:8000/{modulo}/api'
```

Para cambiar la URL, edita la constante `API_URL` en el archivo correspondiente.

## ✅ Estado

- ✅ APIs configuradas correctamente
- ✅ Rutas del backend coinciden
- ✅ Manejo de errores implementado
- ✅ Testing disponible
- ✅ Carrito funcional
- ✅ Checkout integrado

## 🐛 Debugging

Si encuentras errores de API:

1. Verifica que Django esté corriendo: `python manage.py runserver`
2. Abre la consola del navegador (F12 → Network)
3. Revisa las peticiones HTTP
4. Usa `APITesting.testAllAPIs()` para diagnosticar

## 📚 Documentación Completa

Ver `API_DOCUMENTATION.md` en la raíz del proyecto cliente para documentación detallada.
