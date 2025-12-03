import { useState } from 'react'
import { BrowserRouter, Route, Routes, Navigate } from 'react-router-dom'
import './App.css'
import HomeScreen from './screens/HomeScreen.jsx'
import ProductCard from './components/ProductCard.jsx'
import ProductPage from './screens/ProductPage.jsx'
import Checkout from './components/Checkout.jsx'
import { CartProvider } from './context/CartContext.jsx'
import './styles/styles.css'
import CheckoutGuard from './components/CheckoutGuard.jsx'


function App() {


  return (
  <CartProvider>
    <BrowserRouter>
      <div className='container'>
        <Routes>
          <Route path='/' element={<HomeScreen/>}/>
          <Route path='/product/:id' element={<ProductPage/>}/>
          <Route path='/sales/:id' element={<ProductPage/>} />
          <Route path='/checkout' 
            element={
            <CheckoutGuard>
              <Checkout/>
            </CheckoutGuard>
              } 
            />
        </Routes>
      </div>
    </BrowserRouter>
  </CartProvider>
  )
}

export default App
