import React, { useState } from 'react'
import ProductList from '../components/ProductList'
import HomeHeader from '../components/HomeHeader'
import '../styles/styles.css'
import HomeNav from '../components/HomeNav'
import HomeArticle from '../components/HomeArticle'
import HomeMain from '../components/HomeMain.jsx'
import CajaManager from '../components/CajaManager.jsx'

const HomeScreen = () => {

  const [cajaActiva, setCajaActiva] = useState(null)


  return (

  <div className='home-screen'>
      {/* HEADER */}
      <HomeHeader/>

      {/* NAV */}
      <HomeNav/>

    <div className='home-screen-article'>
      {/* ARTICLE */}
      <div className='home-screen-component'>
        <HomeArticle/>
      </div>
      {/* MAIN */}
      <div className='home-screen-component'>
        <HomeMain/>
      </div>
      <div className='home-screen-component'>
        <h2>Caja</h2>
            {/* MANAGER DE CAJA */}
            <CajaManager onCajaChange={setCajaActiva} />
            
            {/* ESTADO DE CAJA */}
            {cajaActiva && (
                <div className='caja-status-banner'>
                    Caja {cajaActiva.numeroCaja} activa - Puedes proceder a comprar
                </div>
            )}
      </div>
  </div>

    </div>
  )
}

export default HomeScreen