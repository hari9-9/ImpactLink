import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Signup from './components/Signup';
import Login from './components/Login';
import Logout from './components/Logout';
import Home from './components/Home';

const App = () => {
  const isAuthenticated = localStorage.getItem('token');

  return (
    <Router>
      <div>
        <nav>
          <a href="/signup">Signup</a>
          <a href="/login">Login</a>
          {isAuthenticated && <a href="/home">Home</a>}
        </nav>

        <Routes>
          <Route path="/signup" element={<Signup />} />
          <Route path="/login" element={<Login />} />
          <Route path="/home" element={isAuthenticated ? <Home /> : <Navigate to="/login" />} />
        </Routes>

        {isAuthenticated && <Logout />}
      </div>
    </Router>
  );
};

export default App;
