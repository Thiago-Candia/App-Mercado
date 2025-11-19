import React, { useState } from 'react'
import axios from 'axios'


export default function SearchInput({ onResults }){

    const [query, setQuery] = useState('')

    const handleSearch = async (e) => {
        const value = e.target.value
        setQuery(value)

        if (value.trim() === '') {
            onResults([])
            return
        }

        try {
            const response = await axios.get(
                `http://localhost:8000/products/productos/buscar/?search=${value}`

            );
            onResults(response.data);
        } 
        catch (error) {
            console.log(error);
        }
    }



    return (
        <input type="text" 
        id='search-input' 
        className="form-control" 
        placeholder="Criterio de Búsqueda" 
        value={query}
        onChange={handleSearch}
        />
    )

}

