
import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { obtenerCajaActiva } from '../api/api.sales'


// sCOMPONENTE PARA VERFICIAR SI HAY CAJA ABIERTA

const CheckoutGuard = ({ children }) => {
    const [cajaActiva, setCajaActiva] = useState(null)
    const [loading, setLoading] = useState(true)
    const navigate = useNavigate()

    useEffect(() => {
        const verificarCaja = async () => {
            try {
                // Leer empleado_id de localStorage
                const empleadoId = localStorage.getItem('empleado_id')
                
                console.log('🔍 Verificando caja activa para empleado:', empleadoId)

                if (!empleadoId) {
                    alert('⚠️ No hay empleado seleccionado. Por favor, abre una caja primero.')
                    navigate('/')
                    return
                }

                // Verificar si hay caja activa
                const caja = await obtenerCajaActiva(empleadoId)
                
                console.log('📦 Caja obtenida:', caja)

                if (!caja) {
                    alert('⚠️ No hay ninguna caja activa. Por favor, abre una caja primero.')
                    navigate('/')
                    return
                }

                setCajaActiva(caja)
                setLoading(false)
            } catch (err) {
                console.error('❌ Error verificando caja:', err)
                alert('Error al verificar la caja. Por favor, intenta de nuevo.')
                navigate('/')
            }
        }

        verificarCaja()
    }, [navigate])

    if (loading) {
        return (
            <div style={{ textAlign: 'center', padding: '50px' }}>
                <h2>Verificando caja activa...</h2>
            </div>
        )
    }

    // Pasar la caja activa al componente hijo
    return React.cloneElement(children, { cajaActiva })
}

export default CheckoutGuard