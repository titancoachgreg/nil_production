import { useState } from 'react'
import axios from 'axios'
import useFetch from "./useFetch"

function EndpointTypeList() {
    const {
        data: endpointType,
        setData: setEndpointType,
        loading,
        error
    } = useFetch('http://localhost:8000/api/endpoint-types/', [])

    const [newEndpointType, setNewEndpointType] = useState([])

    const addEndpointType = () => {
        axios.post('http://localhost:8000/api/endpoint-types/', {
            name: newEndpointType
        }).then(res=> {
            setEndpointType([...endpointType, res.data])
            setNewEndpointType('')
        })
    }

    return (
        <div>
            <h2>Endpoint Types</h2>
            <input
                placeholder="New Endpoint Type"
                value = {newEndpointType}
                onChange={e => setNewEndpointType(e.target.value)}/>
            <button onClick={addEndpointType}>Add</button>
            <ul>
                {endpointType.map(item => (
                    <li key={item.id}>
                        <strong>{item.name}</strong>
                    </li>
                ))}
            </ul>
        </div>
    )
}

export default EndpointTypeList