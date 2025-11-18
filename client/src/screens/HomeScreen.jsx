import React from 'react'
import ProductList from '../components/ProductList'
import HomeHeader from '../components/HomeHeader'

import '../styles/styles.css'
import HomeNav from '../components/HomeNav'
import HomeArticle from '../components/HomeArticle'

const HomeScreen = () => {

  return (

  <div className='home-screen'>
      {/* HEADER */}
      <HomeHeader/>

      {/* NAV */}
      <HomeNav/>


    {/* ARTICLE */}
  <div>
    <HomeArticle/>
  </div>


    {/* MAIN */}
  <div>
  </div>


  <div>
    <div>
      <h2>Mejores servicios</h2>
    </div>
  </div>


      <ProductList/>

    </div>
  )
}

export default HomeScreen