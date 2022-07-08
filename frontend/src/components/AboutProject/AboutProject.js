import React from 'react';
import ProgressBar from '../ProgressBar/ProgressBar';

function AboutProject(props) {
  return (
    <section className="AboutProject" id="project">
      <h2 className='AboutProject__header'>О проекте</h2>
      <div className='AboutProject__articles'>
        <h3 className='AboutProject__subheader'>Дипломный проект включал 5 этапов</h3>
        <p className='AboutProject__text'>Составление плана, работу над бэкендом, вёрстку, добавление функциональности и финальные доработки.</p>
        <h3 className='AboutProject__subheader'>На выполнение диплома ушло 5 недель</h3>
        <p className='AboutProject__text'>У каждого этапа был мягкий и жёсткий дедлайн, которые нужно было соблюдать, чтобы успешно защититься.</p>
      </div>
      <ProgressBar />
    </section>
  );
}

export default AboutProject;

