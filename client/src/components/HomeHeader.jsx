import React from 'react'
import '../styles/styles.css'


const HomeHeader = () => {
    return (
    <header className='header-home'>
        <div className='header-box'>
            <div className='header-box-img'>
                <img src="https://i.pinimg.com/736x/f8/af/e1/f8afe13cf25c09ed404b1a94baee9192.jpg" alt="" />
            </div>
            <div>
                <h1>PRODUCTOS LA ESQUINA DE APU</h1>
            </div>
            <div className='header-box-img'>
                <img src="https://media.newyorker.com/photos/5a0dd9b7ae84d238abda66cb/1:1/w_892,h_892,c_limit/Hsu-Soft-Racism-of-Apu.jpg" alt="" />
            </div>
        </div>
        <hr />
    </header>
    )
}

export default HomeHeader