import './AuthLayout.css'; 
import { useState , useEffect } from 'react';
const AuthLayout = ({ children, title, typingTexts }: { children: React.ReactNode; title: string; typingTexts: string[] }) => {
  const [currentText, setCurrentText] = useState('');
  const [index, setIndex] = useState(0);
  const [subIndex, setSubIndex] = useState(0);
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    if (subIndex === typingTexts[index].length + 1 && !isDeleting) {
      setIsDeleting(true);
      setTimeout(() => {}, 1000);
    } else if (subIndex === 0 && isDeleting) {
      setIsDeleting(false);
      setIndex((prev) => (prev + 1) % typingTexts.length);
    }

    const timeout = setTimeout(() => {
      setSubIndex((prev) => (isDeleting ? prev - 1 : prev + 1));
    }, isDeleting ? 50 : 100);

    return () => clearTimeout(timeout);
  }, [subIndex, index, isDeleting]);

  useEffect(() => {
    setCurrentText(typingTexts[index].substring(0, subIndex));
  }, [subIndex, index]);

  return (
    <div className="auth-page-container">
      <div className="auth-container">
        <div className="auth-animated-text">
        <h1>{currentText || '\u00A0'}</h1>
        </div>
        <div className="auth-form">
          <h2>{title}</h2>
          {children}
        </div>
      </div>
    </div>
  );
};

export default AuthLayout;
