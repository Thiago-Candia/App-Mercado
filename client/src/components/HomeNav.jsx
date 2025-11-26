import React from 'react'


const HomeNav = () => {


    return (

        <nav className='nav-home'>
            <div className='nav-box'>
                <ul className='ul-nav-box'>
                    <li>
                        <button>
                            <i></i>
                            <span>Inicio</span>
                        </button>
                    </li>
                    <li>
                        <button>
                            <i></i>
                            <span>Soluciones</span>
                        </button>
                    </li>
                    <li>
                        <button>
                            <i></i>
                            <span>Catalago de servicios</span>
                        </button>
                    </li>
                        <li>
                        <button>
                            <i></i>
                            <span>Ayuda</span>
                        </button>
                    </li>
                </ul>
            </div>
            <div className='nav-box'>
                <ul className='ul-nav-box'>
                    <li>
                        <button>
                            <i></i>
                            <span>Servicios</span>
                        </button>
                    </li>
                    <li>
                        <button>
                            <i></i>
                            <span>IT Servicio Managment</span>
                        </button>
                    </li>
                    <li>
                        <button>
                            <i></i>
                            <span>Preferencias</span>
                        </button>
                    </li>
                    <li>
                        <button>
                            <i></i>
                            <span>Salir</span>
                        </button>
                    </li>
                </ul>
            </div>
        </nav>
    )
}

export default HomeNav