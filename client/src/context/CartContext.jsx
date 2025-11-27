import React, { createContext, useContext, useState, useEffect } from 'react'

const CartContext = createContext()

export const useCart = () => {
  const context = useContext(CartContext)
  if (!context) {
    throw new Error('useCart debe usarse dentro de CartProvider')
  }
  return context
}

export const CartProvider = ({ children }) => {
  const [cart, setCart] = useState([])
  const [isCartOpen, setIsCartOpen] = useState(false)

  // Cargar carrito del localStorage al iniciar
  useEffect(() => {
    const savedCart = localStorage.getItem('cart')
    if (savedCart) {
      setCart(JSON.parse(savedCart))
    }
  }, [])

  // Guardar carrito en localStorage cuando cambie
  useEffect(() => {
    localStorage.setItem('cart', JSON.stringify(cart))
  }, [cart])

  // Agregar producto al carrito
  const addToCart = (product) => {
    setCart(prevCart => {
      const existingItem = prevCart.find(item => item.id === product.id)
      
      if (existingItem) {
        // Si el producto ya existe, incrementar cantidad
        return prevCart.map(item =>
          item.id === product.id
            ? { ...item, cantidad: item.cantidad + 1 }
            : item
        )
      } else {
        // Si es nuevo, agregarlo con cantidad 1
        return [...prevCart, { ...product, cantidad: 1 }]
      }
    })
  }

  // Remover producto del carrito
  const removeFromCart = (productId) => {
    setCart(prevCart => prevCart.filter(item => item.id !== productId))
  }

  // Actualizar cantidad de un producto
  const updateQuantity = (productId, newQuantity) => {
    if (newQuantity <= 0) {
      removeFromCart(productId)
      return
    }

    setCart(prevCart =>
      prevCart.map(item =>
        item.id === productId
          ? { ...item, cantidad: newQuantity }
          : item
      )
    )
  }

  // Incrementar cantidad
  const incrementQuantity = (productId) => {
    setCart(prevCart =>
      prevCart.map(item =>
        item.id === productId
          ? { ...item, cantidad: item.cantidad + 1 }
          : item
      )
    )
  }

  // Decrementar cantidad
  const decrementQuantity = (productId) => {
    setCart(prevCart =>
      prevCart.map(item =>
        item.id === productId && item.cantidad > 1
          ? { ...item, cantidad: item.cantidad - 1 }
          : item
      )
    )
  }

    // Limpiar carrito
    const clearCart = () => {
        setCart([])
    }

    // Calcular total
    const getTotal = () => {
    return cart.reduce((total, item) => {
        return total + (parseFloat(item.price) * item.cantidad)
    }, 0)
    }

    // Obtener cantidad total de items
    const getTotalItems = () => {
        return cart.reduce((total, item) => total + item.cantidad, 0)
    }

    // Toggle carrito
  const toggleCart = () => {
    setIsCartOpen(!isCartOpen)
  }

    const value = {
        cart,
        addToCart,
        removeFromCart,
        updateQuantity,
        incrementQuantity,
        decrementQuantity,
        clearCart,
        getTotal,
        getTotalItems,
        isCartOpen,
        toggleCart
    }

    return (
    <CartContext.Provider value={value}>
        {children}
    </CartContext.Provider>
    )
}