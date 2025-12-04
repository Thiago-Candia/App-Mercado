import React, { useState } from 'react'
import '../styles/checkout.css'
import { useNavigate } from 'react-router-dom'
import { useCart } from '../context/CartContext'




const ModalCheckout = ({ showSuccessModal, ventaCompletada, onClose }) => {

    const navigate = useNavigate()
    const { clearCart } = useCart()


    const handleCloseModal = () => {
        clearCart()
        navigate('/')
        onClose()
    }

    if (!showSuccessModal) return null


    return (
    <>
        {/* Modal de Éxito */}
        {showSuccessModal && (
            <div className="modal-overlay" onClick={handleCloseModal}>
                <div className="modal-success" onClick={(e) => e.stopPropagation()}>
                    <div className="modal-success-icon">
                        <div className="success-checkmark">
                            <div className="check-icon">
                                <span className="icon-line line-tip"></span>
                                <span className="icon-line line-long"></span>
                                <div className="icon-circle"></div>
                                <div className="icon-fix"></div>
                            </div>
                        </div>
                    </div>
                    
                    <h2 className="modal-success-title">¡Compra Exitosa!</h2>
                    
                    <p className="modal-success-message">
                        Tu compra ha sido procesada correctamente
                    </p>
                    
                    {ventaCompletada && (
                        <div className="modal-success-details">
                            <div className="detail-row">
                                <span className="detail-label">Total pagado:</span>
                                <span className="detail-value">${ventaCompletada.total.toFixed(2)}</span>
                            </div>
                            <div className="detail-row">
                                <span className="detail-label">Cambio:</span>
                                <span className="detail-value">${ventaCompletada.cambio.toFixed(2)}</span>
                            </div>
                            <div className="detail-row">
                                <span className="detail-label">Artículos:</span>
                                <span className="detail-value">{ventaCompletada.items}</span>
                            </div>
                        </div>
                    )}
                    
                    <button 
                        className="modal-success-button"
                        onClick={handleCloseModal}
                    >
                        Volver al inicio
                    </button>
                </div>
            </div>
        )}
    </>
    )
}

export default ModalCheckout