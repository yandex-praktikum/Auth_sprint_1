import React from 'react';

function ProgressBar(props) {
  return (
    <div className="ProgressBar">
      <p className="ProgressBar__stage ProgressBar__stage_stageA">1 неделя</p>
      <p className="ProgressBar__text">Back-end</p>
      <p className="ProgressBar__stage ProgressBar__stage_stageB">4 недели</p>
      <p className="ProgressBar__text">Frond-end</p>
    </div>
  );
}

export default ProgressBar;

