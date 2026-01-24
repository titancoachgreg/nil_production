import useFetch from './useFetch'

function DirectoryList () {
  const {
    data: directory,
    loading,
    error
  } = useFetch('http://localhost:8000/api/ncaa-directory/', [])

  if (loading) return <p>Loading directory...</p>
  if (error) return <p>Failed to load directory...</p>

  return (
    <div>
      <h2>NCAA Directory</h2>
      <ul>
        {directory.map(item => (
          <li key={item.external_id}>
            <strong>{item.name}</strong> - {item.member_type} 
          </li>
        ))}
      </ul>
    </div>

  )
}

export default DirectoryList