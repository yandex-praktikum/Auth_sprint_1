import React from 'react';
import studenPhotoPath from '../../images/student-min.png';

function Bio(props) {
  return (
    <div className="Bio" id="student">
      <p className="Bio__name">Виталий</p>
      <p className="Bio__about">Фронтенд-разработчик, 30 лет</p>
      <p className="Bio__bio">Я родился и живу в Саратове, закончил факультет экономики СГУ. У меня есть жена 
и дочь. Я люблю слушать музыку, а ещё увлекаюсь бегом. Недавно начал кодить. С 2015 года работал в компании «СКБ Контур». После того, как прошёл курс по веб&#8209;разработке, начал заниматься фриланс&#8209;заказами и ушёл с постоянной работы.</p>
      <ul className="Bio__links">
        <li><a className="Bio__link" href="https://facebook.com" target="_blank" rel="noreferrer">Facebook</a></li>
        <li><a className="Bio__link" href="https://github.com" target="_blank" rel="noreferrer">Github</a></li>
      </ul>
      <img className="Bio__photo" src={studenPhotoPath} alt='Фотография'/>
    </div>
  );
}

export default Bio;

