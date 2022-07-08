import React from 'react';
import { useNavigate } from 'react-router-dom';


function Error404(props) {

  const navigate = useNavigate();

  return (
    <div className="Error404">
      <p className="Error404__text">404</p>
      <p className="Error404__message">Страница не найдена</p>
      <button className="Error404__back-button" onClick={() => navigate(-1)}>Назад</button>
    </div>
  );
}

export default Error404;

