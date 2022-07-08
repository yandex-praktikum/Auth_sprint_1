import React from 'react';

function NavTab(props) {
  return (
    <section className='NavTab'>
      <a className='NavTab__link' href='#project' target='_self'>О проекте</a>
      <a className='NavTab__link' href='#techs' target='_self'>Технологии</a>
      <a className='NavTab__link' href='#student' target='_self'>Студент</a>
    </section>
  );
}

export default NavTab;

