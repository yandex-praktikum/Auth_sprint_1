import React from 'react';
import Portfolio from '../Portfolio/Portfolio';
import Bio from '../Bio/Bio';

function AboutMe(props) {
  return (
    <section className="AboutMe">
      <h2 className='AboutMe__header'>Студент</h2>
      <Bio />
      <Portfolio />
    </section>
  );
}

export default AboutMe;

