import React, { useState, useEffect } from 'react'
import '../styles/toast.css'

const Toast = ({ message, type = 'success', duration = 3000, onClose }) => {
    useEffect(() => {
        const timer = setTimeout(() => {
            onClose()
        }, duration)

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
