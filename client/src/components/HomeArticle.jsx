import React from 'react'


const HomeArticle = () => {
    return (
    <article className='catalogo-container'>
        <div>
            <h2 className='catalogo-title'>Catalogo de servicios</h2>
        </div>
        <div>
            <ul className='catalogo-list'>
                <li>
                    <div>
                        <i></i>
                    </div>
                    <div>
                        <button>
                            <span>Hardware</span>
                        </button>
                    </div>
                </li>
                <li>
                    <div>
                        <i></i>
                    </div>
                    <div>
                        <button>
                            <span>Software</span>
                        </button>
                    </div>
                </li>
                <li>
                    <div>
                        <i></i>
                    </div>
                    <div>
                        <button>
                            <span>Otros</span>
                        </button>
                    </div>
                </li>
                <li>
                    <div>
                        <i></i>
                    </div>
                    <div>
                        <button>
                            <span>Material</span>
                        </button>
                    </div>
                </li>
            </ul>
        </div>
    </article>
    )
}

export default HomeArticle