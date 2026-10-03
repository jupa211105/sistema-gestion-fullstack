import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

function Login() {
    const [correo, setCorreo] = useState('')
    const [password, setPassword] = useState('')
    const navigate = useNavigate()

    const iniciarSesion = async () => {
        const respuesta = await fetch('http://127.0.0.1:8000/usuarios/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                correo: correo,
                password: password
            })
        })

        const datos = await respuesta.json()
        console.log(datos.token)
        if (respuesta.ok) {
            localStorage.setItem('token', datos.token)
            navigate('/tareas')
        }
    }
    return(
        <div>
            <h2>Iniciar sesion</h2>

            <input
            type="email"
            placeholder="correo"
            value={correo}
            onChange={(e) => setCorreo(e.target.value)}
            />

            <input
            type="password"
            placeholder="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            />

            <button onClick={iniciarSesion}>
                Iniciar sesion
            </button>
        </div>
    )
}

export default Login 