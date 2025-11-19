import React, { useState } from 'react'
import ProductList from './ProductList'
import SearchInput from './SearchInput'



const HomeMain = () => {

  const [productFiltered, setProductFiltered] = useState([]);



  return (
<main className='main-container'>

  <section className="search-bar">

    <form className="search-form" onSubmit={(e) => e.preventDefault()}>


      {/* BOTON CATEGORIAS */}
      <div className="form-group">
        <label htmlFor="category-select">Categorias</label>
        <select id="category-select" name="categoria">
          <option value="all">Todas</option>
          {/* mapear categorías desde la API */}
          <option value="oficina">Oficina</option>
          <option value="tecnologia">Tecnología</option>
        </select>
      </div>
        {/* INPUT BOTON DE BUSQUEDA */}
      <div className="form-group search-input-group">
        <label htmlFor="search-input" className="visually-hidden">Criterio de Búsqueda</label>
          <SearchInput onResults={setProductFiltered}/>
        
        {/* 5. El ícono debe ser un <button> para ser accesible y clickeable */}
        <button type="submit" aria-label="Buscar">
          <i>🔍</i>
        </button>
      </div>
    </form>
  </section>
  
  {/* --- SECCIÓN DE PRODUCTOS --- */}
  <section className="product-list-container">
    <ProductList products={productFiltered}/>
  </section>
  </main>
  )
}

export default HomeMain