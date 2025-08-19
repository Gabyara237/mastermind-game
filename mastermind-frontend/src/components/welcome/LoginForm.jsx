import { useState } from "react"

const LoginForm =({onLogin})=>{

    const [data,setData] = useState({
        username:"",
        password:""
    })

    const [isLoading,setIsLoading] = useState(false);
    const [error,setError] = useState('');
    const [success, setSuccess] = useState(false);

    const handleChange = (e) =>{
        setData({...data,[e.target.name]:e.target.value});
    };

    const handleSubmit = async (e) =>{
        e.preventDefault(); 
        setIsLoading(true);
        setError('');
        setSuccess(false);

        try{
            const response = await fetch('http://localhost:8000/api/v1/auth/login',{
                method: 'POST',
                headers:{
                    'Content-Type':'application/json',
                },
                body: JSON.stringify(data)
            });

            if(response.ok){
                const responseData = await response.json();
                localStorage.setItem('token',responseData.access_token);
                setSuccess(true); 
                setData({ username: "", password: "" }); 
                onLogin();
            }else{
                setError('Incorrect credentials');
            }
        }catch (err){
            console.error('Error',err)
            setError(`Connection error:${err}`)
        }finally{
            setIsLoading(false);
        }
    };

    return(
        <div className="login-form-section">
            
            <form onSubmit={handleSubmit} className="login-form">
                {error && <div className="error-message">{error}</div>}
                {success && <div className="success-message">Successfully login!</div>}

                <div className="form-group">
                    <label htmlFor="username">Username:</label>
                    <input
                        type="text"
                        id="username"
                        name="username"
                        value={data.username}
                        onChange={handleChange}
                        required
                        disabled={isLoading}
                    />

                </div>

                <div className="form-group">
                    <label htmlFor="password">Password:</label>
                    <input
                        type="password"
                        id="password"
                        name="password"
                        value={data.password}
                        onChange={handleChange}
                        required
                        disabled={isLoading}
                    />

                </div>
                <button
                        type="submit"
                        disabled={isLoading}
                        className="submit-button"
                    >
                        {isLoading? 'Logging in...':'Login'}
                    </button>
            </form>            
        </div>
    )

} 

export default LoginForm