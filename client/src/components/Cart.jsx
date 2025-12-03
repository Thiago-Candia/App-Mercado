import React, { useState, useEffect } from 'react'
import { useCart } from '../context/CartContext'
import { useNavigate } from 'react-router-dom'
import { procesarVentaCompleta, obtenerCajaActiva } from '../api/api.sales'

const Checkout = () => {

    const navigate = useNavigate()
    const { cart, getTotal, clearCart } = useCart()

    const [formData, setFormData] = useState({
        caja_id: 1, // ID de la caja activa
        cliente_nombre: '',
        cliente_dni: '',
        metodo_pago: 'EFE',
        monto_recibido: ''
    })

    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')
    const [cajaActiva, setCajaActiva] = useState(null)

    // useEffect para obetener la caja activa cuando el componente se monte
    useEffect(() => {
    const loadCajaActiva = async () => {
        try {
            const empleadoId = localStorage.setItem('empleado_id')

            if (!empleadoId) {
                setError('No hay empleado seleccionado. Por favor, abre una caja primero.')
                return
            }

            const caja = await obtenerCajaActiva(empleadoId)

            if (caja) {
                setCajaActiva(caja)
                setFormData(prev => ({
                ...prev,
                caja_id: caja.numeroCaja // Cambiar a usar 'id' en lugar de 'numeroCaja'
                }))
            } 
            else {
                setError('No hay ninguna caja activa. Por favor, active una caja primero.')
            }
        } 
        catch (err) {
            console.error('Error al obtener caja activa:', err)
            setError('Error al obtener información de la caja')
        }
    }
    loadCajaActiva()
    }, [])

    //funcion para cambiar los inputs
    const handleInputChange = (e) => {
        const { name, value } = e.target
        setFormData(prev => ({
            ...prev,
            [name]: value
        }))
    }


    //funcion para procesar la venta
    const handleSubmit = async (e) => {
        e.preventDefault()
        
        //si el carrito esta vacio
        if (cart.length === 0) {
            alert('El carrito está vacío')
            return
        }

        //si la caja no esta activa
        if (!cajaActiva) {
            alert('No hay ninguna caja activa')
            return
        }

        const total = getTotal()
        const montoRecibido = parseFloat(formData.monto_recibido)

        if (montoRecibido < total) {
            setError('El monto recibido es insuficiente')
            return
        }

        setLoading(true)
        setError('')

    try {
        // Crear cliente si no existe
        let clienteId = null
        if (formData.cliente_nombre && formData.cliente_dni) {
            const cliente = await createCliente({
                nombre: formData.cliente_nombre,
                dni: parseInt(formData.cliente_dni)
            })
            clienteId = cliente.id
        }

        // Crear venta
        const ventaData = {
            caja_id: cajaActiva.id,
            cliente_id: clienteId,
            metodo_pago: formData.metodo_pago
        }

        const venta = await procesarVentaCompleta(ventaData)

        // Crear detalles de venta (un DetalleVenta por cada producto en el carrito)
        for (const item of cart) {
            await createDetalleVenta({
                venta_id: venta.id,
                producto_id: item.id,
                cantidad: item.quantity,
                precio_unitario: item.price
            })
        }

        // Cobrar la venta
        const total = getTotal()
        await cobrarVenta(venta.id, {
            monto_recibido: parseFloat(formData.monto_recibido),
            descuento: 0
        })

        alert('✅ Compra realizada exitosamente')
        clearCart()
        navigate('/')
        
    } catch (err) {
        console.error('Error:', err)
        setError(err.response?.data?.error || 'Error al procesar la compra')
    } finally {
        setLoading(false)
    }
}

    // Calcular total de la venta
    const total = getTotal()

    return (
    <div className="checkout-container">
        <div className="checkout-wrapper">
        <h1>Finalizar Compra</h1>

        <div className="checkout-content">
            {/* Resumen del pedido */}
            <div className="checkout-summary">
                <h2>Resumen del Pedido</h2>
                <div className="checkout-items">
                    {cart.map(item => (
                    <div key={item.id} className="checkout-item">
                        <img src={item.image || 'https://via.placeholder.com/60'} alt={item.name} />
                        <div className="checkout-item-info">
                        <h4>{item.name}</h4>
                        <p>Cantidad: {item.cantidad}</p>
                        <p className="checkout-item-price">
                          ${(parseFloat(item.price) * item.cantidad).toFixed(2)}
                        </p>
                    </div>
                    </div>
                    ))}
                </div>
                <div className="checkout-total">
                    <h3>Total: ${total.toFixed(2)}</h3>
                </div>
            </div>

            {/* Formulario de pago */}
            <div className="checkout-form-container">
            <h2>Datos de Pago</h2>
            
            {error && (
                <div className="checkout-error">
                    {error}
                </div>
            )}

            <form onSubmit={handleSubmit} className="checkout-form">
                <div className="form-section">
                <h3>Información del Cliente (Opcional)</h3>
                
                <div className="form-group">
                    <label htmlFor="cliente_nombre">Nombre:</label>
                    <input
                        type="text"
                        id="cliente_nombre"
                        name="cliente_nombre"
                        value={formData.cliente_nombre}
                        onChange={handleInputChange}
                        placeholder="Nombre del cliente"
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="cliente_dni">DNI:</label>
                    <input
                        type="text"
                        id="cliente_dni"
                        name="cliente_dni"
                        value={formData.cliente_dni}
                        onChange={handleInputChange}
                        placeholder="DNI del cliente"
                    />
                </div>
                </div>

                <div className="form-section">
                <h3>Método de Pago</h3>
                
                <div className="form-group">
                    <label htmlFor="metodo_pago">Seleccione método:</label>
                    <select
                    id="metodo_pago"
                    name="metodo_pago"
                    value={formData.metodo_pago}
                    onChange={handleInputChange}
                    required
                    >
                    <option value="EFE">Efectivo</option>
                    <option value="CRE">Crédito</option>
                    <option value="DEB">Débito</option>
                    <option value="TRA">Transferencia</option>
                    </select>
                </div>

                <div className="form-group">
                    <label htmlFor="monto_recibido">Monto Recibido: *</label>
                    <input
                    type="number"
                    id="monto_recibido"
                    name="monto_recibido"
                    value={formData.monto_recibido}
                    onChange={handleInputChange}
                    step="0.01"
                    min={total}
                    required
                    placeholder={`Mínimo: $${total.toFixed(2)}`}
                    />
                </div>

                {formData.monto_recibido && (
                    <div className="checkout-change">
                    Cambio: ${(parseFloat(formData.monto_recibido) - total).toFixed(2)}
                    </div>
                )}
              </div>

              <div className="checkout-actions">
                <button
                  type="button"
                  onClick={() => navigate('/')}
                  className="btn-cancel"
                  disabled={loading}
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="btn-submit"
                  disabled={loading}
                >
                  {loading ? 'Procesando...' : 'Confirmar Compra'}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Checkout