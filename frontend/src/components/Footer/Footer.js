import React from 'react';

function Footer(props) {
  return (
    <footer className="Footer">
      <p className="Footer__top">Учебный проект Яндекс.Практикум х BeatFilm.</p>
      <div className="Footer__bottom">
        <p className="Footer__copyright">&copy; 2022</p>
        <a className="Footer__link" href="https://practicum.yandex.ru/" target="_blank" rel="noreferrer">Яндекс.Практикум</a>
        <a className="Footer__link" href="https://github.com" target="_blank" rel="noreferrer">Github</a>
        <a className="Footer__link" href="https://facebook.com" target="_blank" rel="noreferrer">Facebook</a>
      </div>
    </footer>
  );
}

export default Footer;

