import { useState } from 'react'
import { BrowserRouter, Route, Routes, Navigate } from 'react-router-dom'
import './App.css'
import HomeScreen from './screens/HomeScreen.jsx'
import ProductCard from './components/ProductCard.jsx'
import ProductPage from './screens/ProductPage.jsx'


function App() {

  return (
  <BrowserRouter>
    <div className='container'>
      <Routes>
        <Route path='/' element={<HomeScreen/>}/>
        <Route path='/product/:id' element={<ProductPage/>}/>
        <Route path='/sales/:id' element={<ProductPage/>} />
      </Routes>
    </div>
  </BrowserRouter>
  )
}

export default App
