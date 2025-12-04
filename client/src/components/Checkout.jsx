import React, { useState, useEffect } from 'react'
import { useCart } from '../context/CartContext'
import { useNavigate } from 'react-router-dom'
import { procesarVentaCompleta, createCliente, createDetalleVenta, cobrarVenta } from '../api/api.sales'
import '../styles/checkout.css'
import ModalCheckout from './ModalCheckout'

const Checkout = ({ cajaActiva: cajaActivaProp }) => {

    //navegacion 
    const navigate = useNavigate()

    //funcion de CartContext
    const { cart, getTotal, clearCart } = useCart()


    //form data de venta
    const [formData, setFormData] = useState({
        cliente_nombre: '',
        cliente_dni: '',
        metodo_pago: 'EFE',
        monto_recibido: ''
    })


    //la funcion useState para manejar la venta, funcion que se encarga de procesar la venta
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')
    const [cajaActiva, setCajaActiva] = useState(cajaActivaProp || null)
    const [showSuccessModal, setShowSuccessModal] = useState(false)
    const [ventaCompletada, setVentaCompletada] = useState(null)



    // Si no recibimos caja por props, intentar obtenerla de localStorage
    useEffect(() => {
        if (!cajaActiva) {
            const cajaId = localStorage.getItem('caja_id')
            const empleadoId = localStorage.getItem('empleado_id')
            
            if (!cajaId || !empleadoId) {
                setError('No hay empleado seleccionado. Por favor, abre una caja primero.')
                return
            }


        // Usar los datos de localStorage
            setCajaActiva({
                id: parseInt(cajaId),
                empleado_id: parseInt(empleadoId)
            })
        }
    }, [cajaActiva])



    const handleCloseModal = () => {
        setShowSuccessModal(false)
    }


    const handleInputChange = (e) => {
        const { name, value } = e.target
        setFormData(prev => ({
            ...prev,
            [name]: value
        }))
    }


    const handleSubmit = async (e) => {
        e.preventDefault()
        
        console.log('🛒 Iniciando compra...')
        console.log('📦 Carrito:', cart)
        console.log('🏦 Caja activa:', cajaActiva)
        
        // Validaciones
        if (!cart || cart.length === 0) {
            alert('El carrito está vacío')
            return
        }

        if (!cajaActiva || !cajaActiva.id) {
            alert('No hay ninguna caja activa. Por favor, abre una caja primero.')
            navigate('/')
            return
        }

        const total = getTotal()
        const montoRecibido = parseFloat(formData.monto_recibido)

        if (!montoRecibido || montoRecibido < total) {
            setError('El monto recibido es insuficiente')
            return
        }

        setLoading(true)
        setError('')

        try {
            let clienteId = null
            if (formData.cliente_nombre.trim() && formData.cliente_dni.trim()) {
                console.log('👤 Creando cliente...')
                const cliente = await createCliente({
                    nombre: formData.cliente_nombre,
                    dni: parseInt(formData.cliente_dni)
                })
                clienteId = cliente.id
                console.log('✅ Cliente creado:', cliente)
            }

            console.log('📄 Creando venta...')
            const ventaData = {
                caja_id: cajaActiva.id,
                cliente_id: clienteId,
                metodo_pago: formData.metodo_pago
            }
            
            console.log('📄 Datos de venta:', ventaData)

            const venta = await procesarVentaCompleta(ventaData)
            
            console.log('🔍 venta.id:', venta.id)
            console.log('✅ Venta creada:', venta)

            // Crear detalles de venta
            console.log('📦 Creando detalles...')
            for (const item of cart) {
                await createDetalleVenta({
                    venta_id: venta.id,
                    producto_id: item.id,
                    cantidad: item.quantity || item.cantidad,
                    precio_unitario: item.price
                })
                console.log('✅ Detalle creado para:', item.name)
            }

            // Cobrar la venta
            console.log('💰 Cobrando venta...')
            await cobrarVenta(venta.id, {
                monto_recibido: montoRecibido,
                descuento: 0
            })

            console.log('✅ Compra completada exitosamente')
            
            // Guardar datos de la venta para mostrar en el modal
            setVentaCompletada({
                total: total,
                cambio: montoRecibido - total,
                items: cart.length
            })
            
            // Mostrar modal de éxito
            setShowSuccessModal(true)
        } 
        catch (err) {
            console.error('❌ Error completo:', err)
            console.error('❌ Respuesta del servidor:', err.response?.data)
            setError(err.response?.data?.error || 'Error al procesar la compra')
        } 
        finally {
            setLoading(false)
        }
    }

    const total = getTotal()


    return (
        <div className="checkout-container">
            <div className="checkout-wrapper">
                <h1>Finalizar Compra</h1>

                {/* Mostrar información de la caja */}
                {cajaActiva && (
                    <div className="caja-active-badge">
                        <strong>🟢 Caja Activa:</strong> Caja #{localStorage.getItem('caja_numero')}
                    </div>
                )}

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
                                        <p>Cantidad: {item.quantity || item.cantidad}</p>
                                        <p className="checkout-item-price">
                                            ${(parseFloat(item.price) * (item.quantity || item.cantidad)).toFixed(2)}
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
                                        <strong>Cambio: ${(parseFloat(formData.monto_recibido) - total).toFixed(2)}</strong>
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
            
            <ModalCheckout
                showSuccessModal={showSuccessModal}
                ventaCompletada={ventaCompletada}
                onClose={() => setShowSuccessModal(false)}
            />
            
        </div>
    )
}

export default Checkout