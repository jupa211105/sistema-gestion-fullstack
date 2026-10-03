import React,{ useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'



function Tareas(){
    const token = localStorage.getItem('token')
    console.log(token)
    const [tareas, setTareas] = useState([])
    const navigate = useNavigate()

    

    const obtenerTareas = async () => {
        try{
            const respuesta = await fetch('http://127.0.0.1:8000/tareas', {
                method: 'GET',
                headers:{
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            })
        
            const datos = await respuesta.json()
            console.log(datos)

            if (Array.isArray(datos.message)){
                setTareas(datos.message)
            }else{
                setTareas([])
            }
        } catch (error) {
            console.log("Error al obtener las tareas:", error)
        }
    }

    const eliminar_tarea = async(tarea_id) => {
        try{
            const respuesta = await fetch('http://127.0.0.1:8000/tareas/'+ tarea_id, {
                method: 'DELETE',
                headers:{
                    'Authorization': 'Bearer ' + token,
                    'Content-Type': 'application/json'
                }
            })

            if (respuesta.ok) {
                const datos = await respuesta.json()
                console.log(datos)

                setTareas(tareasPrevias =>  tareasPrevias.filter(tarea => tarea.id !== tarea_id))
            }
        } catch (error) {
            console.log("Error al eliminar la tarea:", error)
        }
    }

    const redirigir_tarea = () => {
        navigate('/registrar_tarea')
    }

    const editar_tarea = (tarea_id) => {
        console.log("ID DE TAREA:", tarea_id)
        navigate('/editar_tarea/' + tarea_id )
    }


    useEffect(() => {
        obtenerTareas()
    }, [])

    
    
    return(
        <div>
            <h2>Lista de Tareas</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>TITULO</th>
                        <th>DESCRIPCION</th>
                        <th>ESTADO</th>
                        <th>FECHA DE CREACION</th>
                        <th>PRIORIDAD</th>
                        <th>USUARIO</th>
                        <th>ACCIONES</th>
                    </tr>
                </thead>
                <tbody>
                    {tareas.map((tarea)=>(
                        <tr key={tarea.id}>
                        <td>{tarea.id}</td>
                        <td>{tarea.titulo}</td>
                        <td>{tarea.descripcion}</td>
                        <td>{tarea.estado}</td>
                        <td>{tarea.fecha_creacion}</td>
                        <td>{tarea.prioridad}</td>
                        <td>{tarea.usuario_id}</td>
                        <td><button onClick={() => eliminar_tarea(tarea.id)}>ELIMINAR</button></td>
                        <td><button onClick={() => editar_tarea(tarea.id)}>EDITAR</button></td>
                    </tr>
                    ))}
                </tbody>
            </table>
            <div>
                <button onClick={redirigir_tarea}>REGISTRAR TAREA</button>
            </div>
        </div>
    )   
}

export default Tareas