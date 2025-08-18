import { useState } from "react"
import LoginForm from "../components/LoginForm"
import RegisterForm from "../components/RegisterForm"
import WelcomeSection from "../components/WelcomeSection"

const Welcome =()=>{

    const[login,setLogin]= useState(true)
    const toggleAuth = () => { 
        setLogin(!login)
    }

    return(
        <div className="container-welcome">
            <div className="welcome-card">
                <div className="left-container-welcome ">
                    <WelcomeSection/>

                </div>
                <div className="right-welcome-container"> 
                    
                    <div className="title-welcome-container">
                        <h2 className="hello">Hello!</h2>
                        {login?<p className="title-welcome-right"> <span>Login</span> your Account</p>:<p className="title-welcome-right"> <span>Create</span> a new Account</p> }
                    </div>
                    {login ? <LoginForm/> : <RegisterForm/>}
                    {login ? 
                        <p className="sign" >Don't have account? <span className="span-sign" onClick={toggleAuth}>Sign Up</span></p> :
                        <p className="sign">Already have an account? <span className="span-sign" onClick={toggleAuth}>Sign In</span></p>
                    }
                </div>
            </div>
        </div>
    )
}

export default Welcome