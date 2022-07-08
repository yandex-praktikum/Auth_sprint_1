import React from 'react';
import MoviesCard from '../MoviesCard/MoviesCard';

function MoviesCardList(props) {

  function formatDuration(minutes) {

    let hours =  Math.floor(minutes / 60);
    let min = minutes % 60;
    if (hours > 0) {
      return `${hours}ч ${min}м`
    } else {
      return `${min}м`
    }
  }

  return (
    <ul className="MoviesCardList">
      {props.moviesData.map(movie =>  (
          <li key={movie.id}>
            <MoviesCard 
              id={movie.id}
              image={`https://api.nomoreparties.co${movie.image.url}`}
              title={movie.nameRU}
              duration={formatDuration(movie.duration)}
              saved={props.userMovies[movie.id]}
              deletable={props.isSavedMovies}
              trailerLink={movie.trailerLink}
              alt={movie.image.alternativeText}
              handleMovieSave={props.handleMovieSave}
              handleMovieRemove={props.handleMovieRemove}
              movie={movie}
            />
          </li>
        ))}
    </ul>
  );
}

export default MoviesCardList;
