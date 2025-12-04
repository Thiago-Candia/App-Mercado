import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getProduct } from '../api/api.products'
import '../styles/product-page.css'
import { useCart } from '../context/CartContext'



const ProductPage = () => {

/*  */
  const navigate = useNavigate()

/* params extrae parametros de la URL actual -> id de un producto */
  const params = useParams()

/* obtener la función addToCart del context */
  const { addToCart } = useCart()

/* ESTADOS */
const [product, setProduct] = useState(null)
const [quantity, setQuantity] = useState(1)
/* Se inicia en false -> no se añaden productos al carrito */
const [addedToCart, setAddedToCart] = useState(false)



useEffect(() => {
  /* Función asincrona porque vamos a hacer una peticion HTTP */
  async function loadProduct(){

    /* Validacion de seguridad, si no hay ID en la URL, vuelve al inicio */
    if (!params.id) navigate('/')

    if(params.id){
      const res = await getProduct(params.id)
      setProduct(res.data)
    }

  }
  //ejecucion de la funcion
  loadProduct()
}, [params.id, navigate])


const handleAddToCart = () => {
  for (let i = 0; i < quantity; i++) {
    addToCart(product)
  }
  setAddedToCart(true)
}

/* FUNCIONES PARA DECREMENTAR E INCREMENTAR CANTIDAD DE PRODUCTOS */

const incrementQuantity = (  ) => {
  /* Solo incrementa si no supera el stock */
  if (quantity < product.stock){
    /* suma uno a la cantidad acutal -> causa re-render del componente */
    setQuantity(quantity + 1)
  }
}

const decrementQuantity = (  ) => {
  if (quantity > 1 ){
    setQuantity(quantity - 1)
  }
}

if (!product) return (
  <div className='product-page-loading'>
    <div className='loading-spinner'></div>
    <p>Cargando Producto</p>
  </div>
)


  return (
    <div className="product-page">
      <header className="product-page-header">
        <div className="header-container">
          <button onClick={() => navigate('/')} className="back-button">
            ← Volver al inicio
          </button>
        </div>
      </header>

      <main className="product-page-main">
        <div className="product-page-container">
          <div className="product-page-grid">
            
            <div className="product-image-section">
              {product.image ? (
                <img
                  src={product.image}
                  alt={product.name}
                  className="product-main-image"
                />
              ) : (
                <div className="product-no-image">
                  <span className="no-image-icon">📦</span>
                  <p>Sin imagen</p>
                </div>
              )}
            </div>

            <div className="product-info-section">
              <div className="product-info-content">
                <div className="product-code">
                  Código: {product.codigo}
                </div>

                <h1 className="product-title">{product.name}</h1>

                <p className="product-description">{product.description}</p>

                <div className="product-price-section">
                  <span className="price-currency">$</span>
                  <span className="price-amount">{product.price}</span>
                  <span className="price-unit">KG</span>
                </div>

                <div className="product-stock">
                  <span className="stock-icon">📦</span>
                  <span className="stock-text">Stock disponible:</span>
                  <span className={`stock-amount ${product.stock > 10 ? 'stock-high' : 'stock-low'}`}>
                    {product.stock} unidades
                  </span>
                </div>
              </div>

              <div className="product-actions">
                <div className="quantity-selector">
                  <span className="quantity-label">Cantidad:</span>
                  <div className="quantity-controls">
                    <button
                      onClick={decrementQuantity}
                      className="quantity-btn"
                      disabled={quantity <= 1}
                    >
                      −
                    </button>
                    <span className="quantity-display">{quantity}</span>
                    <button
                      onClick={incrementQuantity}
                      className="quantity-btn"
                      disabled={quantity >= product.stock}
                    >
                      +
                    </button>
                  </div>
                </div>

                <button
                  onClick={handleAddToCart}
                  disabled={product.stock === 0 || addedToCart}
                  className={`add-to-cart-button ${addedToCart ? 'added' : ''} ${product.stock === 0 ? 'disabled' : ''}`}
                >
                  {addedToCart ? (
                    <>
                      <span className="check-icon">✓</span>
                      <span>Agregado al carrito</span>
                    </>
                  ) : (
                    <>
                      <span className="cart-icon">🛒</span>
                      <span>
                        {product.stock === 0 ? 'Sin stock' : 'Agregar al carrito'}
                      </span>
                    </>
                  )}
                </button>

                <div className="product-total">
                  <div className="total-row">
                    <span className="total-label">Total:</span>
                    <span className="total-amount">
                      ${(product.price * quantity).toFixed(2)}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default ProductPage