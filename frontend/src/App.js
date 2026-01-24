import React from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import DirectoryList from './components/Directory'
import SportsList from './components/SportList'
import EndpointTypeList from './components/EndpointType'

function App() {
  return (
    <Router>
      <div style={{ padding: "2rem" }}>
        <h1>NCAA Data Platform</h1>

        <nav style={{ marginBottom: "1rem" }}>
          <Link to="/directory">Directory</Link> |{" "}
          <Link to="/sports">Sports</Link> |{" "}
          <Link to="/endpoint-types">EndpointTypes</Link>
        </nav>

        <Routes>
          <Route path="/directory" element={<DirectoryList />} />
          <Route path="/sports" element={<SportsList />} />
          <Route path="/endpoint-types" element={<EndpointTypeList />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
