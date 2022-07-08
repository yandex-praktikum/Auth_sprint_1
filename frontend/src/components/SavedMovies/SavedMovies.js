import React from 'react';
import SearchForm from '../SearchForm/SearchForm';
import MoviesCardList from '../MoviesCardList/MoviesCardList';
import Preloader from '../Preloader/Preloader';
import {filterByDuration, filterByQuery} from '../../utils/filters';
import Errors from '../Errors/Errors';

function SavedMovies(props) {

  const [searchQuery, setSearchQuery] = React.useState('');

  const [filterShortFilms, setFilterShortFilms] = React.useState(false);

  const [moviesToShow, setMoviesToShow] = React.useState(getCurrentUserMovies());

  const [isLoading, setIsLoading] = React.useState();
  
  React.useEffect(() => {
    props.loadMovieFromServer();
    filterMovies(getCurrentUserMovies(), searchQuery);
  }, [])  
  
  React.useEffect(() => {
    filterMovies(getCurrentUserMovies(), searchQuery);
  }, [filterShortFilms, props.userMovies])

  React.useEffect(() => {
    if (moviesToShow.length === 0) {
      props.setErrorFromServer("Ничего не найдено");
    } else {
      props.setErrorFromServer("");
    }
  }, [moviesToShow])

  function getCurrentUserMovies() {
    const movies = JSON.parse(localStorage.getItem('allMovies')) || [];
    return movies.filter((item) => Object.keys(props.userMovies).includes(item.id.toString()));
  }

  function filterMovies(movies, query) {
    const queryMatch = filterByQuery(movies, query);
    const durationMatch = filterByDuration(queryMatch, filterShortFilms);
    setMoviesToShow(durationMatch);
    
  }

  function handleSearchSubmit(e) {
    setIsLoading(true);
    e.preventDefault();
    filterMovies(getCurrentUserMovies(), searchQuery);
    setIsLoading(false);
  }

  return (
    <div className="Movies">
      <SearchForm 
        name="search"
        handleSubmit={handleSearchSubmit}
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
        filterShortFilms={filterShortFilms}
        setFilterShortFilms={setFilterShortFilms}
        setErrorFromServer={props.setErrorFromServer}
        saveResults={false}
      />
      <Preloader isLoading={isLoading}/>
      <Errors errorFromServer={props.errorFromServer} />
      <>
        <MoviesCardList 
          moviesData={moviesToShow}
          errorFromServer={props.errorFromServer}
          handleMovieRemove={props.handleMovieRemove}
          userMovies={props.userMovies}
          isSavedMovies={true}
        />
      </>
    
    </div>
  );
}

export default SavedMovies;