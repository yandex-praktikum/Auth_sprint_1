import React from 'react';
import { resolutions, cardsInRow } from '../settings/settings';

const GetNumberOfCardAccordingToWidth = () => {

  const [width, setWidth] = React.useState(window.innerWidth);

  const updateDimension = () => {
    setTimeout(function(){setWidth(window.innerWidth)}, 1000);
  }

  React.useEffect(() => {
    window.addEventListener("resize", updateDimension);
    return () => window.removeEventListener("resize", updateDimension);
  });

  function getNumberOfCards() {
    if (width >= resolutions.laptop) {
        return cardsInRow.laptop;
    } else if (width >= resolutions.tablet) { 
        return cardsInRow.tablet;
    } else if (width >= resolutions.mobile) {
        return cardsInRow.mobile;
    }
  }

  return getNumberOfCards
}

export default GetNumberOfCardAccordingToWidth;