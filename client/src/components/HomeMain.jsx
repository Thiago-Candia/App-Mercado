import React, { useState } from 'react'
import ProductList from './ProductList'
import SearchInput from './SearchInput'

const HomeMain = () => {
  const [productFiltered, setProductFiltered] = useState([]);

  return (
    <main className='main-container'>
      {/* BARRA DE BÚSQUEDA */}
      <section className="search-bar">
        <form className="search-form" onSubmit={(e) => e.preventDefault()}>
          {/* SELECTOR DE CATEGORÍAS */}
          <div className="form-group">
            <label htmlFor="category-select">Categorias</label>
            <select id="category-select" name="categoria">
              <option value="all">Todas</option>
              <option value="hardware">Hardware</option>
              <option value="software">Software</option>
              <option value="otros">Otros</option>
              <option value="material">Material</option>
            </select>
          </div>

          {/* INPUT DE BÚSQUEDA */}
          <div className="form-group search-input-group">
            <label htmlFor="search-input">Criterio de Búsqueda</label>
            <SearchInput onResults={setProductFiltered}/>
            <button type="submit" aria-label="Buscar">
              🔍
            </button>
          </div>
        </form>
      </section>
      
      {/* LISTA DE PRODUCTOS */}
      <section className="product-list-container">
        <ProductList products={productFiltered}/>
      </section>
    </main>
  )
}

export default HomeMain