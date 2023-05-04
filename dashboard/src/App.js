import React, {useState, useEffect} from 'react'

function App() {
    const [data, setData] = useState([{}])
    useEffect(() => {
        fetch("/api/data").then(
            res => res.json()
        ).then(
            data => {
                setData(data)
                console.log(data)
            }
        )
    }, [])
    return (
        <div>
            {(typeof data.cells === "undefined") ? (
                <p>Loading...</p>
            ): (
                data.cells.map((cells, i) => (
                    <p key={i}>{cells}</p>
                ))
            )}
        </div>
    )
}

export default App
