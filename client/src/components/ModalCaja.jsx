import React from 'react'
import '../styles/checkout.css'



const ModalCaja = ({ showModal, modalData, onClose }) => {
    if (!showModal || !modalData) return null

    const isAbrirCaja = modalData.type === 'abrir'

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-success" onClick={(e) => e.stopPropagation()}>
                <div className="modal-success-icon">
                    {isAbrirCaja ? (
                        // Ícono de caja Abierta
                        <div className="success-checkmark">
                            <div className="check-icon" style={{ borderColor: '#4BB543' }}>
                                <span className="icon-line line-tip"></span>
                                <span className="icon-line line-long"></span>
                                <div className="icon-circle"></div>
                                <div className="icon-fix"></div>
                            </div>
                        </div>
                    ) : (
                        // icono de caja cerrada 
                        <div className="success-checkmark">
                            <div className="check-icon" style={{ borderColor: '#dc3545' }}>
                                <span className="icon-line line-tip" style={{ backgroundColor: '#dc3545' }}></span>
                                <span className="icon-line line-long" style={{ backgroundColor: '#dc3545' }}></span>
                                <div className="icon-circle" style={{ borderColor: 'rgba(220, 53, 69, 0.5)' }}></div>
                                <div className="icon-fix"></div>
                            </div>
                        </div>
                    )}
                </div>
                
                <h2 className="modal-success-title">
                    {isAbrirCaja ? '¡Caja Abierta!' : '¡Caja Cerrada!'}
                </h2>
                
                <p className="modal-success-message">
                    {isAbrirCaja 
                        ? 'La caja ha sido abierta exitosamente' 
                        : 'La caja ha sido cerrada correctamente'}
                </p>
                
                <div className="modal-success-details">
                    <div className="detail-row">
                        <span className="detail-label">Número de Caja:</span>
                        <span className="detail-value">#{modalData.numeroCaja}</span>
                    </div>
                    <div className="detail-row">
                        <span className="detail-label">Empleado:</span>
                        <span className="detail-value">{modalData.empleado}</span>
                    </div>
                    {isAbrirCaja ? (
                        <div className="detail-row">
                            <span className="detail-label">Hora de apertura:</span>
                            <span className="detail-value">{modalData.hora}</span>
                        </div>
                    ) : (
                        <>
                            <div className="detail-row">
                                <span className="detail-label">Apertura:</span>
                                <span className="detail-value">{modalData.apertura}</span>
                            </div>
                            <div className="detail-row">
                                <span className="detail-label">Cierre:</span>
                                <span className="detail-value">{modalData.cierre}</span>
                            </div>
                        </>
                    )}
                </div>
                
                <button 
                    className="modal-success-button"
                    onClick={onClose}
                    style={isAbrirCaja ? {} : { background: 'linear-gradient(135deg, #dc3545 0%, #c82333 100%)' }}
                >
                    {isAbrirCaja ? 'Continuar' : 'Entendido'}
                </button>
            </div>
        </div>
    )
}

export default ModalCaja