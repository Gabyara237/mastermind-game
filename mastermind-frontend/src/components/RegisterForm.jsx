import { useState } from "react"

const RegisterForm =() =>{
    const [data,setData] = useState({
        username: "",
        email: "",
        password: ""
    })

    const [isLoading,setIsLoading] = useState(false);
    const [error,setError] = useState("");
    const [success, setSuccess] = useState(false);

    const handleChange = (e)=>{
        setData({...data,[e.target.name]:e.target.value});
    }

    const handleSubmit= async (e) =>{
        e.preventDefault();
        setIsLoading(true);
        setError('');
        setSuccess(false);

        try{

            const response= await fetch('http://localhost:8000/api/v1/auth/register',{
                method: 'POST',
                headers:{
                    'Content-Type':'application/json',
                },
                body: JSON.stringify(data)
            })

            if (response.ok){
                const responseData= await response.json();
                console.log('Successful register!', responseData);
                setSuccess(true); 
                setData({ username: "", email: "", password: "" }); 
                alert('Account successfully created')
            }else{

                const errorData = await response.json();
                setError(errorData.detail || 'Registration error');
            }

        }catch(err){
            console.error('Error:', err);
            setError(`Registration Error: ${err.message}`);
        }finally{
            setIsLoading(false);
        }

    }

    return(
        <>
            <form onSubmit={handleSubmit} className="register-form">
                {error && <div className="error-message">{error}</div>}
                {success && <div className="success-message">Account successfully created!</div>}
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
                    <label htmlFor="email">Email:</label>
                    <input
                        type="email"
                        id="email"
                        name="email"
                        value={data.email}
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

                    <button
                        type="submit"
                        disabled={isLoading}
                        className="submit-button"
                    >
                        {isLoading ? 'Creating account...' : 'Create Account'}
                    </button>

                </div>
            </form>       
        </>
    )
}

export default RegisterForm