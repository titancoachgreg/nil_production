import { useState } from 'react'
import axios from 'axios'
import useFetch from './useFetch'
import './AliasModal.css'

function AliasModal({ sportId, onClose }) {
    const {
        data: aliases,
        setData: setAliases,
        loading
    } = useFetch(`http://localhost:8000/api/sport-aliases/?ncaa_directory_sport=${sportId}`,[])

    const [newAlias, setNewAlias] = useState([])

    const addAlias = () => {
        axios.post('http://localhost:8000/api/sport-aliases/', {
            ncaa_directory_sport: sportId,
            name: newAlias
        }).then(res => {
            setAliases([...aliases, res.data])
            setNewAlias('')
        }).catch(err => console.error(err))
    }

    const updateAlias = (id, name) => {
        axios.put(`http://localhost:8000/api/sport-aliases/${id}/`,
            {
                ncaa_directory_sport: sportId,
                name
            }
        ).then(res => {
            setAliases(aliases.map(a => a.id === id ? res.data : a))
        }).catch(err => console.error(err))
    }

    const deleteAlias = id => {
        axios.delete(`http://localhost:8000/api/sport-aliases/${id}/`)
        .then(() => {
            setAliases(aliases.filter(a => a.id !== id))
        }).catch(err => console.error(err))
    }

    return (
        <div className="modal-backdrop">
            <div className="modal">

            <h3>Sport Aliases</h3>

            {loading ? <p>Loading</p> : (
                <ul>
                    {aliases.map(alias => {
                        const [editedName, setEditedName] = useState(alias.name)

                        const hasChanged = editedName !== alias.name

                        return (
                            <li key={alias.id}>
                                <input 
                                    value={editedName}
                                    onChange={e => setEditedName(e.target.value)}
                                    />
                                <button
                                    onClick={() => updateAlias(alias.id, editedName)}
                                    disabled={!hasChanged}
                                >
                                Save
                                </button>
                                <button onClick={() => deleteAlias(alias.id)}>✕</button>
                            </li>
                        )
                    })}
                </ul>
            )}

            <input 
                placeholder="New alias"
                value ={newAlias}
                onChange={e => setNewAlias(e.target.value)}
            />
            <button onClick={addAlias}>Add</button>
            <button onClick={onClose}>Close</button>
        </div>
    </div>
    )
}

export default AliasModal