
App para supermercado.
Es un sistema web de punto de venta desarrollado con Django REST Framework y React, diseñado para la gestión completa de ventas, productos, cajas y empleados en comercios minoristas.

Características Principales

- **Gestión de Productos**: CRUD completo con imágenes, categorías y subcategorías
- **Sistema de Cajas**: Apertura/cierre de cajas con asignación de empleados y control de efectivo
- **Carrito de Compras**: Gestión de productos con cantidades y cálculo automático de totales
- **Procesamiento de Ventas**: Registro completo de ventas con múltiples métodos de pago
- **Búsqueda Inteligente**: Búsqueda de productos por nombre o código
- **Interfaz Moderna**: Diseño minimalista y responsivo

Tecnologías Utilizadas

-Backend (Django)
- **Django 5.2.7**: Framework web principal
- **Django REST Framework**: API RESTful
- **SQLite**: Base de datos (desarrollo)
- **django-cors-headers**: Manejo de CORS para conectar con React

-Frontend (React)
- **React 18+**: Biblioteca de interfaz de usuario
- **React Router DOM**: Navegación entre páginas
- **Axios**: Peticiones HTTP al backend
- **Context API**: Gestión de estado global (carrito)

Estructura del Proyecto
mercado/
├── backend/
│   ├── sales/          # App de ventas y cajas
│   ├── products/       # App de productos y catálogo
│   ├── sucursal/       # App de sucursales
│   └── core/           # Configuración principal
└── frontend/
    ├── src/
    │   ├── components/    # Componentes reutilizables
    │   ├── context/       # Context API (CartContext)
    │   ├── api/           # Servicios de API
    │   └── styles/        # Archivos CSS
    └── public/


Flujo de Trabajo

### 1. Inicio de Sesión de Caja
Seleccionar Empleado + Caja → Asignar → Ingresar Monto → Abrir Caja
### 2. Proceso de Venta
Buscar Productos → Agregar al Carrito → Checkout → Ingresar Datos → Confirmar
### 3. Cierre de Caja
Ingresar Monto Final → Cerrar Caja → Guardar en Historial


Endpoints Principales

### Productos
```
GET    /products/api/products/           -> Listar productos
GET    /products/api/products/{id}/      -> Detalle de producto
GET    /products/products/buscar/        -> Buscar productos
```

### Ventas
```
POST   /ventas/api/venta/                -> Crear venta
POST   /ventas/api/venta/{id}/cobrar/    -> Cobrar venta
POST   /ventas/api/detalle/              -> Crear detalle de venta
```

### Cajas
```
GET    /ventas/api/caja/disponibles/              -> Cajas disponibles
POST   /ventas/api/caja/{id}/asignar_empleado/    -> Asignar empleado
POST   /ventas/api/caja/{id}/abrir_caja/          -> Abrir caja
POST   /ventas/api/caja/{id}/cerrar_caja/         -> Cerrar caja
```

Seguridad

- CORS configurado para permitir solo origen específico (localhost:5173)
- Validaciones en backend y frontend
- Control de acceso por empleado/caja
- Sanitización de entradas de usuario

Modelos Principales

**Product**: Productos del catálogo
**Caja**: Cajas registradoras
**Empleado**: Personal del comercio
**Venta**: Transacciones de venta
**DetalleVenta**: Líneas de venta (productos × cantidades)
**Cliente**: Clientes (opcional)


---------------------------------Posibles mejoras a futuro---------------------------------

-Notificaciones por email
-Agregar reportes de ventas
-Sistema de descuentos
-Búsqueda avanzada
-Mejoras a futuro
-Autenticación de usuarios
-Modo oscuro
-Multi-idioma
-Filtros por precio
-Reviews de productos
-Impresión de tickets
-Historial de ventas por empleado
-Gestión de inventario avanzada


-------------------------------------EXPLICACIONES DE CODIGO/COMPONENTES-------------------------------------


Algunos componentes claves

Backend:

**`CajaManager`** 
- Gestión de cajas registradoras
- Asignación de empleados a cajas
- Control de apertura/cierre con montos
- Historial de cierres en JSON

**`VentaViewSet`** 
- Procesamiento de ventas
- Registro de ventas con cliente opcional
- Detalles de venta (productos, cantidades, precios)
- Sistema de cobro con múltiples métodos de pago

**`ProductViewSet`** 
- Gestión de productos
- CRUD completo de productos
- Actualización de stock y precios
- Búsqueda por nombre/código

Frontend:

**`CartContext`** 
- Estado global del carrito
addToCart(product)      -> Agregar producto
removeFromCart(id)      -> Eliminar producto
getTotal()              -> Calcular total
clearCart()             -> Vaciar carrito


**`CajaManager`** 
- Componente de gestión de cajas
- Flujo de 2 pasos: Asignar empleado → Abrir caja
- Formulario de cierre con validaciones
- Persistencia en localStorage

**`Checkout`** 
- Proceso de compra
- Resumen del pedido
- Datos del cliente (opcional)
- Modal de éxito con animación

**`ProductPage`** 
- Página de detalle de producto
- Información completa del producto
- Selector de cantidad con validación de stock
- Cálculo automático de total


-------------------------------------DJANGO-------------------------------------

Un serializer es un componente que:
Convierte modelos de Django (objetos de la base de datos) ➡️ JSON
Convierte JSON recibido desde el frontend (por ejemplo, React) ➡️ objetos del modelo
Sin serializer → no podés enviar ni recibir datos en JSON desde el frontend.


permite agrupar toda la lógica de una API CRUD (Crear, Leer, Actualizar, Borrar) para un modelo específico, como Product, en un solo lugar.
Su propósito principal es reducir drásticamente el código repetitivo.
En lugar de crear múltiples clases de vista (una para listar productos, otra para ver un producto, otra para crearlo), un ViewSet maneja todas esas responsabilidades en una sola clase.

MODELS

Ejemplos realizados con los modelos de ventaDetalle y Venta.

DO_NOTHING -> DO_NOTHING Si se borra un producto, deja el ID de ese producto en la DetalleVenta aunque ya no exista.
base de datos se llenará de "IDs huérfanos"

CASCADE -> si se borra un producto, borra el ID de ese producto en la DetalleVenta

PROTECT -> si se borra un producto, no deja el ID de ese producto en la DetalleVenta, y lanza una excepción.

-------------------------------------REACT-------------------------------------

USESTATE.

USESTATE ES UNA MANERA DE MANEJAR EL ESTADO DE UN COMPONENTE EN REACT. Se llama como un array con dos elementos en donde el primero es el estado y el segundo es una funcion para actualizar el estado

CONTEXT.

El Context API de React es una herramienta que permite pasar datos a través del árbol de componentes sin tener que pasar props manualmente en cada nivel. Se utiliza para compartir información como el estado global, el tema, el idioma o el usuario autenticado, a la que varios componentes pueden acceder sin una cadena de prop-drilling. React proporciona React.createContext() para crear el contexto y useContext (un hook) para que los componentes lo consuman. 

