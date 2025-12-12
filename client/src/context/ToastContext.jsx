import React, { createContext, useContext, useState } from 'react'
import Toast from '../components/Toast'

const ToastContext = createContext()

// Hook para acceder al toast
export const useToast = () => {
    const context = useContext(ToastContext)
    if (!context) {
        throw new Error('useToast debe ser usado dentro de ToastProvider')
    }
    return context
}

// Proveedor del toast
export const ToastProvider = ({ children }) => {
    const [toast, setToast] = useState(null)

    const showToast = (message, type = 'success', duration = 3000) => {
        setToast({ message, type, duration })
    }

    // Funcion para ocultar el toast
    const hideToast = () => {
        setToast(null)
    }


    return (
        <ToastContext.Provider value={{ showToast, hideToast }}>
            {children}
            {toast && (
                <Toast
                    message={toast.message}
                    type={toast.type}
                    duration={toast.duration}
                    onClose={hideToast}
                />
            )}
        </ToastContext.Provider>
    )
}