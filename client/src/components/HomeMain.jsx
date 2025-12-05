import React, { useState, useEffect } from 'react'
import ProductList from './ProductList'
import SearchInput from './SearchInput'
import { getAllCategorias, getProductsByCategory, getAllProducts } from '../api/api.products'

const HomeMain = () => {

  /* Estados de busqueda y filtro  */
  const [productFiltered, setProductFiltered] = useState([]);
  const [categorias, setCategorias] = useState([]);



  // UseEffect para carga inicial de productos
  useEffect(() => {
    async function loadInitialProducts() {
        try {
            const res = await getAllProducts();
            setProductFiltered(res.data);
        } catch (error) {
            console.error(error);
        }
    }
    loadInitialProducts();
  }, []);

  // UseEffect para carga de categorias para el select
  useEffect(() => {
    async function loadCategorias() {
      try {
        const res = await getAllCategorias();
        setCategorias(res.data);
      } catch (error) {
        console.error("Error cargando categorías:", error);
      }
    }
    loadCategorias();
  }, []);

  // funcion para la logica del filtro
  const handleCategoryChange = async (e) => {
    const categoriaId = e.target.value;
    
    try {
        let res;
        
        // 1. Si selecciona "Todas", traemos todo el listado
        if (categoriaId === 'all') {
            res = await getAllProducts(); 
        } 
        else {
            // si selecciona una específica, filtramos por backend
            // Esto llamará a: /products/?categoria=ID
            res = await getProductsByCategory(categoriaId);
        }
        
        // se actualzia el estado que usa ProductList
        setProductFiltered(res.data);

    } 
    catch (error) {
      console.error("error filtrando productos:", error);
    }
  };

  return (
    <main className='main-container'>
      <section className="search-bar">
        <form className="search-form" onSubmit={(e) => e.preventDefault()}>
          
          <div className="form-group">
            <label htmlFor="category-select">Categorias</label>
            <select 
                id="category-select" 
                name="categoria"
                onChange={handleCategoryChange} // <-- conexion con la funcion de buscar por categoria
            >
              <option value="all">Todas</option>
              
              {categorias.map((cat) => (
                <option key={cat.id} value={cat.id}>
                  {cat.name}
                </option>
              ))}

            </select>
          </div>

          <div className="form-group search-input-group">
            <label htmlFor="search-input">Criterio de Búsqueda</label>
            {/* Se pasa setProductFiltered para que el buscador tambien actualice la lista */}
            <SearchInput onResults={setProductFiltered}/>
            <button type="submit" aria-label="Buscar">
              🔍
            </button>
          </div>
        </form>
      </section>
      
      <section className="product-list-container">
        {/* lista se renderiza basada en el estado productFiltered */}
        <ProductList products={productFiltered}/>
      </section>
    </main>
  )
}

export default HomeMain