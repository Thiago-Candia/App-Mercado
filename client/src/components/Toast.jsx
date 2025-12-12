import React, { useState, useEffect } from 'react'
import '../styles/toast.css'


/* Componente toast, por parametro se para un mensaje, tipo, duracion y funcion de cierre*/
const Toast = ({ message, type = 'success', duration = 3000, onClose }) => {

    /* UseEffect para cerrar el toast */
    useEffect(() => {
        /* funcion interna para cerrar el toast */
        const timer = setTimeout(() => {
            onClose()
        }, duration)

        /* limpiar el timer */
        return () => clearTimeout(timer)
    }, [duration, onClose])


    /* renderizacion del toast */
    return (
        <div className={`toast toast-${type}`}>
            <span className="toast-icon">
                {type === 'success' && '✓'}
                {type === 'error' && '✕'}
                {type === 'info' && 'ℹ'}
            </span>
            <span className="toast-message">{message}</span>
        </div>
    )
}

export default Toast
