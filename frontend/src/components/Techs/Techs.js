import React from 'react';

function Techs(props) {
  return (
    <section className="Techs" id="techs">
      <h2 className='Techs__header'>Технологии</h2>
      <h3 className='Techs__subheader'>7 технологий</h3>
      <p className='Techs__text'>На курсе веб-разработки мы освоили технологии, которые применили в дипломном проекте.</p>
      <ul className='Techs__elements'>
        <li className='Techs__element'>HTML</li>
        <li className='Techs__element'>CSS</li>
        <li className='Techs__element'>JS</li>
        <li className='Techs__element'>React</li>
        <li className='Techs__element'>Git</li>
        <li className='Techs__element'>Express.js</li>
        <li className='Techs__element'>mongoDB</li>
      </ul>
    </section>
  );
}

export default Techs;

