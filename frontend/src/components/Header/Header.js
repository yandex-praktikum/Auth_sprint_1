import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import headerLogoPath from '../../images/logo.svg';
import SlideMenu from '../SlideMenu/SlideMenu';

function Header(props) {

  const [sideMenuShown, setSideMenuShown] = React.useState(false);
  const navigate = useNavigate();

  function showSlideMenu(e) {
    setSideMenuShown(true);
  }
  function sideMenuHided(link) {
    setSideMenuShown(false);
    if (link === false) {
      navigate(link);
    }
  }

  return (
    <header className={props.dark ? `Header` : `Header Header_logined` }>
      <Link to="/" className={!props.isLogined ? `Header__logo` : `Header__logo Header__logo_logined` } target="_self">
        <img src={headerLogoPath} alt="Логотип проекта" />
      </Link>
      {!props.isLogined ? (<>  
        <Link className="Header__reglink" to="/signup" target="_self">Регистрация</Link>
        <Link className="Header__inlink" to="/signin" target="_self">Войти</Link>
        </>) : (<>
          <Link className={`Header__link ${props.parent !== "/movies" && "Header__link_light"} ${props.dark && "Header__link_white"} `}
                to="/movies" target="_self">Фильмы</Link>
          <Link className={`Header__link ${props.parent !== "/saved-movies" && "Header__link_light"} ${props.dark && "Header__link_white"}`}
                to="/saved-movies" target="_self">Сохранённые фильмы</Link>
          <Link className={`Header__profile-link ${props.dark && "Header__link_white"}`} to="/profile" target="_self">Аккаунт</Link>
          <span className="Header__profile-icon" />
          <button className="Header__more-button" onClick={showSlideMenu} />
          <SlideMenu 
            active={sideMenuShown}
            onClose={sideMenuHided}
            />
            
        </>)}
    </header>
  );
}

export default Header;
