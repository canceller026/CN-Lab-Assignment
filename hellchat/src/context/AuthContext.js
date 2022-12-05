import React, { createContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios'
import jwt_decode from 'jwt-decode'


const AuthContext = createContext();
export default AuthContext;

export const AuthProvider = ({ children }) => {
  const [User, setUser] = useState(null);
  const [AuthToken, setAuthToken] = useState(null);
  const [LoginError, setLoginError] = useState('');
  const [RegisterError, setRegisterError] = useState('');

  const navigate = useNavigate()

  const loginUser = async (username, password) => {
    axios({
      baseURL: 'http://127.0.0.1:8000/api/token/',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      data: {
        username: username,
        password: password,
      },
    })
      .then((response) => {
        setAuthToken(() => response.data);
        setUser(() => jwt_decode(response.data.access));
        localStorage.setItem('authToken', JSON.stringify(response.data));
        navigate('/');
      })
      .catch((error) => setLoginError(() => error.response.data.detail));
  };

  const logoutUser = () => {
    setAuthToken(null);
    setUser(null);
    localStorage.removeItem('authToken');
    navigate('/login');
  };

  const AuthData = {
    User: User,
    setUser: setUser,
    AuthToken: AuthToken,
    setAuthToken: setAuthToken,
    loginUser: loginUser,
    logoutUser: logoutUser,
    LoginError: LoginError,
    RegisterError: RegisterError,
  };
  return (
    <AuthContext.Provider value={AuthData}>{children}</AuthContext.Provider>
  );
};
