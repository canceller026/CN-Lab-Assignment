import "./login.css";
import React from "react";



function LoginView(){


    /*Return function*/    
    return (
        <div className="container">
            <div className="holder">
                <div className="login">
                    <div className="login-box">
                        <h1>Sign in</h1>
                        <form method="POST" action="" id="login-form">
                            <div className="user-box">
                            <input type="text" name="" required=""/>
                            <label>Username</label>
                            </div>
                            <div className="user-box">
                            <input type="password" name="" required=""/>
                            <label>Password</label>
                            </div>
                            <p style={{marginTop:'0em',color:'white'}}>Don't have an account ? <a href="/register" style={{color:'#03e9f4', cursor:'pointer'}}>Sign up</a></p>

                            <a href="#" className="btn">
                            <span></span>
                            <span></span>
                            <span></span>
                            <span></span>
                            Sign in
                            </a>
                        </form>
                    </div>
                </div>
                <div className="image">
                    <div className="holder"><img src="https://upload.wikimedia.org/wikipedia/commons/d/de/HCMUT_official_logo.png" /></div>
                </div>
            </div>
            <div className="decoration">
                <div className="decor0"></div>
                <div className="decor1"></div>
                <div className="decor2"></div>
            </div>
        </div>
        
    );
}
export default LoginView;
