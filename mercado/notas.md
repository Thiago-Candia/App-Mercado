


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