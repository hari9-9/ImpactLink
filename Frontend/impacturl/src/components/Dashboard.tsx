import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Dashboard.css';

interface Product {
  product_name: string;
  original_url: string;
  shortened_url: string;
  total_clicks: number;
}

const Dashboard = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProductStats = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/linker/product-stats', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('accessToken')}`
          }
        });
        setProducts(response.data.products);
      } catch (err) {
        setError('Failed to fetch product data.');
      } finally {
        setLoading(false);
      }
    };

    fetchProductStats();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    navigate('/login');
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h2>Product Statistics</h2>
        <button className="logout-button" onClick={handleLogout}>Logout</button>
      </div>
      <table border="1" cellPadding="10" style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ backgroundColor: '#007bff', color: 'white' }}>
            <th>Product Name</th>
            <th>Original URL</th>
            <th>Shortened URL</th>
            <th>Total Clicks</th>
          </tr>
        </thead>
        <tbody>
          {products.map((product, index) => (
            <tr key={index}>
              <td>{product.product_name}</td>
              <td><a href={product.original_url} target="_blank" rel="noopener noreferrer">{product.original_url}</a></td>
              <td><a href={product.shortened_url} target="_blank" rel="noopener noreferrer">{product.shortened_url}</a></td>
              <td>{product.total_clicks}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Dashboard;
