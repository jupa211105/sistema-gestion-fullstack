import { useState, useEffect  } from 'react'
import { useNavigate, useParams } from 'react-router-dom'

function Editar(){
    const   { id } = useParams()
    const token = localStorage.getItem('token')
    const navigate = useNavigate()

    const [tarea, setTarea] = useState({
        titulo: '',
        descripcion: '',
        estado: '',
        prioridad: ''
    })


    const EditarTarea = async () => {
        const respuesta = await fetch('http://127.0.0.1:8000/tareas/' + id, {
            method: 'PUT',
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                titulo: tarea.titulo,
                descripcion: tarea.descripcion,
                estado: tarea.estado,
                prioridad: tarea.prioridad
            })
        })

        const datos = await respuesta.json()
        console.log(datos.message)
        if(respuesta.ok){
            navigate('/tareas')
        }
    }

    const BuscarTarea = async () => {
        try{
            const respuesta = await fetch('http://127.0.0.1:8000/tareas/' + id,  {
                method: "GET",
                headers:{
                    'Authorization': 'Bearer ' + token,
                    'Content-Type': 'application/json'
                }
            })

            const datos = await respuesta.json()
            console.log(datos)

            if (datos && datos.message){
                setTarea(datos.message)
            }
        } catch (error) {
            console.log("Error al obtener la tarea:", error)
        }
    }

    useEffect(() => {
        BuscarTarea()
    }, [])

    return(
        <div>
            <h1>Editar Tarea</h1>

            <input
            type="text"
            value={tarea.titulo || ''}
            onChange={(e) => setTarea({ ...tarea, titulo: e.target.value })}
            />

            <input
            type="text"
            value={tarea.descripcion || ''}
            onChange={(e) => setTarea({ ...tarea, descripcion: e.target.value })}
            />

            <input
            type="text"
            value={tarea.estado || ''}
            onChange={(e) => setTarea({ ...tarea, estado: e.target.value })}
            />

            <input
            type="text"
            value={tarea.prioridad || ''}
            onChange={(e) => setTarea({ ...tarea, prioridad: e.target.value })} 
            />

            <button onClick={EditarTarea}>
                ACEPTAR
            </button>
        </div>
    )
}

export default Editar