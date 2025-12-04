import React, { useState, useEffect } from 'react'
import { abrirCaja, cerrarCaja, obtenerCajaActiva, obtenerEmpleados } from '../api/api.sales'
import '../styles/caja-manager.css'

const CajaManager = ({ onCajaChange }) => {




    const [empleados, setEmpleados] = useState([])
    const [cajaActiva, setCajaActiva] = useState(null)
    const [empleadoSeleccionado, setEmpleadoSeleccionado] = useState('')
    const [numeroCaja, setNumeroCaja] = useState('')
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')



    // Cargar empleados al montar el componente
    useEffect(() => {
        const loadEmpleados = async () => {
            try {
                const data = await obtenerEmpleados()
                setEmpleados(data)
            } 
            catch (err) {
                console.error('Error cargando empleados:', err)
                setError('Error al cargar empleados')
            }
        }
        loadEmpleados()
    }, [])

    // Verificar si hay caja activa del empleado seleccionado
    useEffect(() => {
        const verificarCajaActiva = async () => {
            if (empleadoSeleccionado) {
                try {
                    const caja = await obtenerCajaActiva(empleadoSeleccionado)
                    if (caja) {
                        setCajaActiva(caja)
                        setNumeroCaja(caja.numeroCaja)
                        onCajaChange(caja)
                    } 
                    else {
                        setCajaActiva(null)
                        setNumeroCaja('')
                        onCajaChange(null)
                    }
                } 
                catch (err) {
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
        
            //Guardar en localStorage
            localStorage.setItem('empleado_id', empleadoSeleccionado)
            localStorage.setItem('caja_id', caja.id)
            localStorage.setItem('caja_numero', caja.numeroCaja)
            
            console.log('✅ Datos guardados en localStorage:', {
                empleado_id: empleadoSeleccionado,
                caja_id: caja.id,
                caja_numero: caja.numeroCaja
            })

            setError('')
            alert(`✅ Caja ${caja.numeroCaja} abierta exitosamente`)
        
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

        const confirmar = window.confirm(`¿Cerrar caja ${cajaActiva.numeroCaja}?`)
        if (!confirmar) return

        setLoading(true)
        setError('')
        
        try {
            await cerrarCaja(cajaActiva.id)
            setCajaActiva(null)
            setEmpleadoSeleccionado('')
            setNumeroCaja('')
            onCajaChange(null)
            alert('✅ Caja cerrada exitosamente')
        } 
        catch (err) {
            console.error('Error:', err)
            setError(err.response?.data?.error || 'Error al cerrar caja')
        } 
        finally {
            setLoading(false)
        }
    }

    return (
        <div className='caja-manager'>
            {error && <div className='error-message'>{error}</div>}
            
            {!cajaActiva ? (
                <form onSubmit={handleAbrirCaja} className='caja-form'>
                    <h3>📂 Abrir Caja</h3>
                    
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
                        <p><strong>Caja:</strong> {cajaActiva.numeroCaja}</p>
                        <p><strong>Empleado:</strong> {cajaActiva.empleado}</p>
                        <p><strong>Apertura:</strong> {cajaActiva.apertura}</p>
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
    )
}

export default CajaManager