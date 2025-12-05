import React, { useState, useEffect } from 'react'
import { abrirCaja, cerrarCaja, obtenerCajaActiva, obtenerEmpleados } from '../api/api.sales'
import '../styles/caja-manager.css'
import ModalCaja from './ModalCaja'

const CajaManager = ({ onCajaChange }) => {
    const [empleados, setEmpleados] = useState([])
    const [cajaActiva, setCajaActiva] = useState(null)
    const [empleadoSeleccionado, setEmpleadoSeleccionado] = useState('')
    const [numeroCaja, setNumeroCaja] = useState('')
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')
    const [verificandoCaja, setVerificandoCaja] = useState(true)
    
    // Estados para el modal
    const [showModal, setShowModal] = useState(false)
    const [modalData, setModalData] = useState(null)

    // Verificar caja activa al montar el componente
    useEffect(() => {
        const verificarCajaInicial = async () => {
            try {
                const empleadoId = localStorage.getItem('empleado_id')
                
                if (empleadoId) {
                    console.log('verificando caja activa para empleado:', empleadoId)
                    
                    const caja = await obtenerCajaActiva(empleadoId)
                    
                    if (caja) {
                        console.log('se encontro la caja activa:', caja)
                        setCajaActiva(caja)
                        setEmpleadoSeleccionado(empleadoId)
                        setNumeroCaja(caja.numeroCaja)
                        onCajaChange(caja)
                    } else {
                        console.log('no se encontro la caja activa')
                        // Limpiar localStorage si no hay caja activa
                        localStorage.removeItem('empleado_id')
                        localStorage.removeItem('caja_id')
                        localStorage.removeItem('caja_numero')
                    }
                }
            } catch (err) {
                console.error('Error verificando caja inicial:', err)
            } finally {
                setVerificandoCaja(false)
            }
        }
        
        verificarCajaInicial()
    }, [onCajaChange])

    // Cargar empleados al montar el componente
    useEffect(() => {
        const loadEmpleados = async () => {
            try {
                const data = await obtenerEmpleados()
                setEmpleados(data)
            } catch (err) {
                console.error('Error cargando empleados:', err)
                setError('Error al cargar empleados')
            }
        }
        loadEmpleados()
    }, [])

    // Verificar si hay caja activa del empleado seleccionado (solo cuando cambia manualmente)
    useEffect(() => {
        const verificarCajaActiva = async () => {
            if (empleadoSeleccionado && !cajaActiva) {
                try {
                    const caja = await obtenerCajaActiva(empleadoSeleccionado)
                    if (caja) {
                        setCajaActiva(caja)
                        setNumeroCaja(caja.numeroCaja)
                        onCajaChange(caja)
                    } else {
                        setNumeroCaja('')
                        onCajaChange(null)
                    }
                } catch (err) {
                    console.error('Error verificando caja:', err)
                }
            }
        }
        verificarCajaActiva()
    }, [empleadoSeleccionado])

    const handleAbrirCaja = async (e) => {
        e.preventDefault()
        
        if (!empleadoSeleccionado || !numeroCaja) {
            setError('Por favor selecciona empleado y número de caja')
            return
        }

        setLoading(true)
        setError('')
        
        try {
            const caja = await abrirCaja(empleadoSeleccionado, parseInt(numeroCaja))
            setCajaActiva(caja)
            onCajaChange(caja)
        
            // Guardar en localStorage
            localStorage.setItem('empleado_id', empleadoSeleccionado)
            localStorage.setItem('caja_id', caja.id)
            localStorage.setItem('caja_numero', caja.numeroCaja)
            
            console.log('Datos guardados en localStorage:', {
                empleado_id: empleadoSeleccionado,
                caja_id: caja.id,
                caja_numero: caja.numeroCaja
            })

            // Mostrar modal de éxito
            setModalData({
                type: 'abrir',
                numeroCaja: caja.numeroCaja,
                empleado: `${empleados.find(e => e.id == empleadoSeleccionado)?.nombre} ${empleados.find(e => e.id == empleadoSeleccionado)?.apellido}`,
                hora: caja.apertura 
            })
            setShowModal(true)
            setError('')
        } 
        catch (err) {
            console.error('Error:', err)
            setError(err.response?.data?.error || 'Error al abrir caja')
        } 
        finally {
            setLoading(false)
        }
    }




    const handleCerrarCaja = async () => {
        if (!cajaActiva) return

        setLoading(true)
        setError('')
        
        try {
            // Obtener la respuesta del backend con la hora de cierre actualizada
            const cajaActualizada = await cerrarCaja(cajaActiva.id)
            
            const datosParaModal = {
                type: 'cerrar',
                numeroCaja: cajaActualizada.numeroCaja,
                empleado: cajaActualizada.empleado,
                apertura: cajaActualizada.apertura,
                cierre: cajaActualizada.cierre  // Usar la hora que viene del backend
            }
            
            // Limpiar estado y localStorage
            setCajaActiva(null)
            setEmpleadoSeleccionado('')
            setNumeroCaja('')
            onCajaChange(null)
            
            localStorage.removeItem('empleado_id')
            localStorage.removeItem('caja_id')
            localStorage.removeItem('caja_numero')
            
            // Mostrar modal de cierre
            setModalData(datosParaModal)
            setShowModal(true)
        } catch (err) {
            console.error('Error:', err)
            setError(err.response?.data?.error || 'Error al cerrar caja')
        } finally {
            setLoading(false)
        }
    }

    // Mostrar loading mientras verifica
    if (verificandoCaja) {
        return (
            <div className='caja-manager'>
                <div style={{ textAlign: 'center', padding: '20px' }}>
                    <p>Verificando estado de caja...</p>
                </div>
            </div>
        )
    }

    return (
        <>
            <div className='caja-manager'>
                {error && <div className='error-message'>{error}</div>}
                
                {!cajaActiva ? (
                    <form onSubmit={handleAbrirCaja} className='caja-form'>
                        <h3>Abrir Caja</h3>
                        
                        <div className='form-group'>
                            <label>Empleado:</label>
                            <select
                                value={empleadoSeleccionado}
                                onChange={(e) => setEmpleadoSeleccionado(e.target.value)}
                                required
                            >
                                <option value=''>Selecciona empleado</option>
                                {empleados.map(emp => (
                                    <option key={emp.id} value={emp.id}>
                                        {emp.nombre} {emp.apellido}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div className='form-group'>
                            <label>Número de Caja:</label>
                            <input
                                type='number'
                                value={numeroCaja}
                                onChange={(e) => setNumeroCaja(e.target.value)}
                                placeholder='Ej: 1'
                                required
                            />
                        </div>

                        <button 
                            type='submit' 
                            disabled={loading}
                            className='btn-abrir'
                        >
                            {loading ? 'Abriendo...' : '🟢 Abrir Caja'}
                        </button>
                    </form>
                ) : (
                    <div className='caja-activa'>
                        <div className='status-active'>
                            <span className='status-badge'>🟢 ACTIVA</span>
                        </div>
                        <div className='caja-info'>
                            <p>
                                <strong>Caja:</strong> 
                                {cajaActiva.numeroCaja}
                            </p>
                            <p>
                                <strong>Empleado:</strong> 
                                {cajaActiva.empleado}
                            </p>
                            <p>
                                <strong>Apertura:</strong> 
                                {cajaActiva.apertura}
                            </p>
                        </div>
                        <button 
                            onClick={handleCerrarCaja}
                            disabled={loading}
                            className='btn-cerrar'
                        >
                            {loading ? 'Cerrando...' : '🔴 Cerrar Caja'}
                        </button>
                    </div>
                )}
            </div>
            
            {/* Modal de Caja */}
            <ModalCaja
                showModal={showModal}
                modalData={modalData}
                onClose={() => setShowModal(false)}
            />
        </>
    )
}

export default CajaManager