import React from 'react'
import ProductList from '../components/ProductList'
import HomeHeader from '../components/HomeHeader'
import '../styles/styles.css'
import HomeNav from '../components/HomeNav'
import HomeArticle from '../components/HomeArticle'
import HomeMain from '../components/HomeMain.jsx'

const HomeScreen = () => {

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
        <h2>Mejores servicios</h2>
      </div>
  </div>


    </div>
  )
}

export default HomeScreen