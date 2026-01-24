import { useState } from 'react'
import axios from 'axios'
import useFetch from './useFetch'
import AliasModal from './AliasModal'

function SportsList () {
    const {
        data: sports,
        setData: setSports,
        loading,
        error
    } = useFetch('http://localhost:8000/api/sports', [])

    const [editingId, setEditingId] = useState(null)
    const [tempSport, setTempSport] = useState({})
    const [aliasSportId, setAliasSportId] = useState(null)

    const startEditing = sport => {
        setEditingId(sport.id)
        setTempSport({ ...sport })
    }

    const cancelEdit = () => {
        setEditingId(null)
        setTempSport({})
    }

    const sanitizeData = obj => {
        const cleaned = {}
        for (const key in obj) {
            cleaned[key] =
            obj[key] === '' || obj[key] === undefined ? null : obj[key]
        }
        return cleaned
    }

    const saveEdit = () => {
        const payload = sanitizeData(tempSport)

        axios.put(`http://localhost:8000/api/sports/${editingId}/`, payload)
            .then(res => {
                setSports(sports.map(s =>
                    s.id === editingId ? res.data : s
                ))
                cancelEdit()
            })
            .catch(err => console.error('Failed to save sport', err))
    }

    const deleteSport = id => {
        axios.delete(`http://localhost:8000/api/sports/${id}`)
            .then(() => {
                setSports(sports.filter(s => s.id !== id))                
            })
            .catch(err => console.error(err))
        }

    if (loading) return <p>Loading sports...</p>
    if (error) return <p>Failed to load sports</p>

    return (
        <div>
            <h2>Sports</h2>

            <table>
                <thead>
                    <tr>
                        <th>Sport</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {sports.map(sport => (
                        <tr key={sport.id}>
                            <td>
                                {editingId === sport.id ? (
                                    <input
                                        value={tempSport.name || ''}
                                        onChange={e =>
                                            setTempSport({ ...tempSport, name: e.target.value})
                                        }
                                        />
                                ) : (
                                    <strong>{sport.name}</strong>
                                )}
                            </td>

                            <td>
                                {editingId === sport.id ? (
                                    <>
                                        <button onClick={saveEdit}>Save</button>
                                        <button onClick={cancelEdit}>Cancel</button>   
                                    </>
                                ) : (
                                    <>
                                        <button onClick={() => startEditing(sport)}>Edit</button>
                                        <button onClick={() => deleteSport(sport.id)}>Delete</button>
                                        <button
                                            onClick={() => setAliasSportId(sport.id)}
                                        >
                                            Aliases
                                        </button>
                                    </>
                                )}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {aliasSportId && (
                <AliasModal
                    sportId={aliasSportId}
                    onClose={() => setAliasSportId(null)}
                />
            )}
        </div>
    )
}

export default SportsList

