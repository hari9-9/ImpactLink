import { useNavigate } from 'react-router-dom';

const Home = ({ onLogout }: { onLogout: () => void }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    onLogout();
    navigate('/login');
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>Hello, World!</h1>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default Home;
