import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

function RegistrarTareas(){
    const token = localStorage.getItem('token')
    const navigate = useNavigate()

    const [titulo, setTitulo] = useState('')
    const [descripcion, setDescripcion] = useState('')
    const [estado, setEstado] = useState('')
    const [prioridad, setPrioridad] = useState('')

    const crearTarea = async () => {
        const respuesta = await fetch('http://127.0.0.1:8000/tareas', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                titulo: titulo,
                descripcion: descripcion,
                estado: estado,
                prioridad: prioridad
            })
        })

        const datos = await respuesta.json()
        console.log(datos.message)
        if(respuesta.ok){
            navigate('/tareas')
        }
    }

    return(
        <div>
            <h1>Registrar Tarea</h1>

            <input
            type="text"
            placeholder="titulo"
            value={titulo}
            onChange={(e) => setTitulo(e.target.value)}
            />

            <input
            type="text"
            placeholder="descripcion"
            value={descripcion}
            onChange={(e) => setDescripcion(e.target.value)}
            />

            <input
            type="text"
            placeholder="estado"
            value={estado}
            onChange={(e) => setEstado(e.target.value)}
            />

            <input
            type="text"
            placeholder="prioridad"
            value={prioridad}
            onChange={(e) => setPrioridad(e.target.value)} 
            />

            <button onClick={crearTarea}>
                CREAR TAREA
            </button>
        </div>
    )
}

export default RegistrarTareas