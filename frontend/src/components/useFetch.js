import { useState, useEffect } from 'react'
import axios from 'axios'

function useFetch(url, initialData = []) {
  const [data, setData] = useState(initialData)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    let isMounted = true
    setLoading(true)

    axios.get(url)
      .then(res => {
        if (isMounted) {
          setData(res.data)
          setLoading(false)
        }
      })
      .catch(err => {
        if (isMounted) {
          console.error(err)
          setError(err)
          setLoading(false)
        }
      })

    return () => { isMounted = false }
  }, [url])

  return { data, setData, loading, error }
}

export default useFetch
