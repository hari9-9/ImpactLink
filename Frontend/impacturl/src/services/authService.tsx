import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/accounts";

export const signup = async (email: string, password: string) => {
    return axios.post(`${API_BASE_URL}/signup/`, { email, password });
};

// export const login = async (email: string, password: string) => {
//     console.log("API Base URL:", API_BASE_URL);
//     return axios.post(`${API_BASE_URL}/login/`, { email, password });
// };

export const login = async (email: string, password: string) => {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/login/`, // Correct endpoint based on project structure
        {
          email: email,
          password: password
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
          withCredentials: true,  // Include if cookies/session authentication is used
        }
      );
      console.log("Login Response:", response.data);
      return response.data;
    } catch (error) {
      console.error("Login error:", error.response ? error.response.data : error.message);
      throw error;
    }
  };
  

export const logout = () => {
    localStorage.removeItem('token');
};
