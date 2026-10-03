import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Login from './components/Login'
import Tareas from './components/Tareas'
import Registrar from './components/Registrar'
import Editar from './components/Editar'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/tareas" element={<Tareas />} />
        <Route path="/registrar_tarea" element={<Registrar />} />
        <Route path="/editar_tarea" element={<Editar />} />
        <Route path="/editar_tarea/:id" element={<Editar />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App