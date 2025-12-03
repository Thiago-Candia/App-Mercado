


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

CASCADE -> CASCADE Si se borra un producto, borra el ID de ese producto en la DetalleVenta

PROTECT -> PROTECT Si se borra un producto, no deja el ID de ese producto en la DetalleVenta, y lanza una excepción.

El Context API de React es una herramienta que permite pasar datos a través del árbol de componentes sin tener que pasar props manualmente en cada nivel. Se utiliza para compartir información como el estado global, el tema, el idioma o el usuario autenticado, a la que varios componentes pueden acceder sin una cadena de prop-drilling. React proporciona React.createContext() para crear el contexto y useContext (un hook) para que los componentes lo consuman. 











## 📝 Próximos Pasos (Opcionales)

- [ ] Agregar autenticación de usuarios
- [ ] Implementar historial de compras
- [ ] Agregar reportes de ventas
- [ ] Sistema de descuentos
- [ ] Notificaciones por email
- [ ] Modo oscuro
- [ ] Multi-idioma
- [ ] Búsqueda avanzada
- [ ] Filtros por precio
- [ ] Reviews de productos

---

## 🎉 CONCLUSIÓN

**Tu proyecto está completamente funcional y listo para usar.**

Todo está integrado:
✅ Frontend - Carrito visual
✅ Backend - APIs funcionando
✅ Base de datos - Guardando datos
✅ Documentación - Completa