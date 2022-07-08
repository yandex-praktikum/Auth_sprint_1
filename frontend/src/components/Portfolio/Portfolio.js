import React from "react";

function Portfolio(props) {
  return (
    <div className="Portfolio">
      <h3 className="Portfolio__header">Портфолио</h3>
      <ul className="Portfolio__elements">
        <li className="Portfolio__element">
          <p className="Portfolio__text">Статичный сайт</p>
          <button className="Portfolio__arrow" target="_blank" rel="noreferrer" href="https://github.com/akomissarov2020/russian-travel">↗</button>
        </li>
        <li className="Portfolio__element">
          <p className="Portfolio__text">Адаптивный сайт</p>
          <button className="Portfolio__arrow" target="_blank" rel="noreferrer" href="https://github.com/akomissarov2020/mesto">↗</button>
        </li>
        <li className="Portfolio__element">
          <p className="Portfolio__text">Одностраничное приложение</p>
          <button className="Portfolio__arrow" target="_blank" rel="noreferrer" href="https://github.com/akomissarov2020/mesto">↗</button>
        </li>
      </ul>
    </div>
  );
}

export default Portfolio;

