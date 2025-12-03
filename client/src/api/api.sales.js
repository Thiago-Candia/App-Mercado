
//BIBLIOTECA AXIOS PARA HACER PETICIONES HTTP A UN SERVIDOR
import axios from 'axios'



// DIRECCION (  /SALES/API  ) OBTENIDA DE URLS.PY => APP SALES BACKEND.
const API_URL = 'http://localhost:8000/sales/api'



//CREAMOS UNA INSTANCIA DE AXIOS
export const salesApi = axios.create({
    baseURL: API_URL
})


// ===== VENTAS =====



//OBTENER UNA VENTA
export const getAllSales = () => salesApi.get('/venta/')



export const postSales = (sale) => salesApi.post('/venta/', sale)



export const getVentas = async () => {
    try {
        const response = await salesApi.get('/venta/')
        return response.data
    } catch (error) {
        console.error('Error al obtener ventas:', error)
        throw error
    }
}




export const getVentaById = async (ventaId) => {
    try {
        const response = await salesApi.get(`/venta/${ventaId}/`)
        return response.data
    } catch (error) {
        console.error('Error al obtener venta:', error)
        throw error
    }
}




export const createVenta = async (ventaData) => {
    try {
        const response = await salesApi.post('/venta/', ventaData)
        return response.data
    } catch (error) {
        console.error('Error al crear venta:', error)
        throw error
    }
}

export const cobrarVenta = async (ventaId, cobrarData) => {
    try {
        const response = await salesApi.post(
            `/venta/${ventaId}/cobrar_venta/`,
            cobrarData
        )
        return response.data
    } catch (error) {
        console.error('Error al cobrar venta:', error)
        throw error
    }
}

export const aplicarDescuento = async (ventaId, descuentoData) => {
    try {
        const response = await salesApi.post(
            `/venta/${ventaId}/hacer_descuento/`,
            descuentoData
        )
        return response.data
    } catch (error) {
        console.error('Error al aplicar descuento:', error)
        throw error
    }
}




// ===== CLIENTES =====


export const createCliente = async (clienteData) => {
    try {
        const response = await salesApi.post('/cliente/', clienteData)
        return response.data
    } catch (error) {
        console.error('Error al crear cliente:', error)
        throw error
    }
}

export const getClientes = async () => {
    try {
        const response = await salesApi.get('/cliente/')
        return response.data
    } catch (error) {
        console.error('Error al obtener clientes:', error)
        throw error
    }
}

// ===== CAJAS =====


export const abrirCaja = async (empleadoId, numeroCaja) => {
    try {
        const response = await salesApi.post('/caja/abrir_caja/', {
            empleado_id: empleadoId,
            numeroCaja: numeroCaja
        })
        return response.data
    } catch (error) {
        console.error('Error al abrir caja:', error)
        throw error
    }
}


export const cerrarCaja = async (cajaId) => {
    try {
        const response = await salesApi.post(`/caja/${cajaId}/cerrar_caja/`)
        return response.data
    } catch (error) {
        console.error('Error al cerrar caja:', error)
        throw error
    }
}


export const obtenerCajaActiva = async (empleadoId) => {
    try {
        const response = await salesApi.get('/caja/obtener_caja_activa/', {
            params: { empleado_id: empleadoId }
        })
        return response.data
    } catch (error) {
        console.error('Error al obtener caja activa:', error)
        throw error
    }
}



export const obtenerEmpleados = async () => {
    try {
        const response = await axios.get('http://localhost:8000/sucursal/api/empleado/')
        return response.data
    } catch (error) {
        console.error('Error al obtener empleados:', error)
        throw error
    }
}

export const procesarVentaCompleta = async (ventaData) => {
    try {
        const response = await salesApi.post('/venta/', ventaData)
        return response.data
    } catch (error) {
        console.error('Error al procesar venta:', error)
        throw error
    }
}




// ===== DETALLE VENTA =====


export const createDetalleVenta = async (detalleData) => {
    try {
        const response = await salesApi.post('/detalleventa/', detalleData)
        return response.data
    } catch (error) {
        console.error('Error al crear detalle de venta:', error)
        throw error
    }
}

// ===== FILTRAR VENTAS =====

export const filtrarVentasPorDia = async (fecha) => {
    try {
        const response = await salesApi.post(
            '/venta/filtrar_ventas/',
            { fecha_filtrada: fecha }
        )
        return response.data
    } 
    catch (error) {
        console.error('Error al filtrar ventas por día:', error)
        throw error
    }
}

export const filtrarVentasPorMes = async (anio, mes) => {
    try {
        const response = await salesApi.post(
            '/venta/filtra_mes/',
            { anio_filtrada: anio, mes_filtrada: mes }
        )
        return response.data
    } catch (error) {
        console.error('Error al filtrar ventas por mes:', error)
        throw error
    }
}





// ===== FUNCIÓN COMPLETA PARA PROCESAR VENTA =====
/* export const procesarVentaCompleta = async (cartItems, formData) => {
    try {
        // 1. Crear o buscar cliente (si proporcionó datos)
        let clienteId = null
        if (formData.cliente_nombre && formData.cliente_dni) {
            const cliente = await createCliente({
                nombre: formData.cliente_nombre,
                dni: parseInt(formData.cliente_dni)
            })
            clienteId = cliente.id
        }

        // 2. Crear la venta
        const ventaData = {
            caja_id: formData.caja_id,
            ...(clienteId && { cliente_id: clienteId })
        }
        const venta = await createVenta(ventaData)

        // 3. Crear detalles de venta para cada producto
        for (const item of cartItems) {
            await createDetalleVenta({
                venta_id: venta.numero_venta,
                producto_id: item.id,
                cantidad: item.cantidad,
                descuento: 0
            })
        }

        // 4. Cobrar la venta
        const cobrarData = {
            venta_id: venta.numero_venta,
            monto_recibido: parseFloat(formData.monto_recibido),
            descuento: 0
        }
        const resultadoCobro = await cobrarVenta(venta.numero_venta, cobrarData)

        return {
            venta,
            cobro: resultadoCobro
        }
    } catch (error) {
        console.error('Error al procesar venta completa:', error)
        throw error
    }
} */