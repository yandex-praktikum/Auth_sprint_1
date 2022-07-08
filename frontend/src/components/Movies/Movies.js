import {useState, useEffect} from 'react';
import SearchForm from '../SearchForm/SearchForm';
import Preloader from '../Preloader/Preloader';
import Errors from '../Errors/Errors';
import MoviesCardList from '../MoviesCardList/MoviesCardList';
import GetNumberOfCardAccordingToWidth from '../../utils/resizer';
import {filterByDuration, filterByQuery} from '../../utils/filters';

function Movies(props) {

  const [searchQuery, setSearchQuery] = useState(() => {
    return localStorage.getItem('searchQuery') 
    ? 
      JSON.parse(localStorage.getItem('searchQuery')) 
      : 
      ''
  });

  const [filterShortFilms, setFilterShortFilms] = useState(() => {
    return localStorage.getItem('filterShortFilms') 
    ? 
    JSON.parse(localStorage.getItem('filterShortFilms')) 
    : 
    false
  });

  const [datasetSize, setDatasetsize] = useState(false);
  const [filteredMovies, setFilteredMovies] = useState([])
  const [moviesToShow, setMoviesToShow] = useState(filteredMovies.slice(0, GetNumberOfCardAccordingToWidth()));
  const [isLoading, setIsLoading] = useState();

  let sizeOfCardBatch =  GetNumberOfCardAccordingToWidth()();

  useEffect(() => {
    props.setErrorFromServer("");
  }, []);

  useEffect(() => {
    setMoviesToShow(filteredMovies.slice(0, sizeOfCardBatch));
    if (filteredMovies.length === 0 && datasetSize > 0) {
      props.setErrorFromServer("Ничего не найдено");
    } else if (datasetSize === 0) {
      props.setErrorFromServer("Во время запроса произошла ошибка. Возможно, проблема с соединением или сервер недоступен. Подождите немного и попробуйте ещё раз");
    } else {
      props.setErrorFromServer("");
    }
  }, [filteredMovies])

  useEffect(() => {
    if (searchQuery) {
      const movies = localStorage.getItem('allMovies') ? JSON.parse(localStorage.getItem('allMovies')) : [];
      filterMovies(movies, searchQuery);
      setMoviesToShow(filteredMovies.slice(0, sizeOfCardBatch));
    } else {
      setMoviesToShow([]);
    }
  }, [filterShortFilms])

  function onMoreClick() {
    setMoviesToShow(moviesToShow.concat(filteredMovies.slice(moviesToShow.length, moviesToShow.length + sizeOfCardBatch)))
  }

  function filterMovies(movies, query) {
    if (movies) {
      const queryMatch = filterByQuery(movies, query);
      const durationMatch = filterByDuration(queryMatch, filterShortFilms);
      setFilteredMovies(durationMatch);
    }
  }

  function handleSearchSubmit(e) {
    e.preventDefault();
    if (searchQuery.length === 0) {
      props.setErrorFromServer("Нужно ввести ключевое слово");
      return;
    }
    setIsLoading(true);
    props.setErrorFromServer("");
    setMoviesToShow([]);
    setFilteredMovies([]);
    setTimeout(()=>{
      const movies = props.handleSearchSubmit(searchQuery, filterShortFilms);
      if (!movies) {
        setDatasetsize(0);
        props.setErrorFromServer("Во время запроса произошла ошибка. Возможно, проблема с соединением или сервер недоступен. Подождите немного и попробуйте ещё раз");
      } else {
        setDatasetsize(movies.length);
      }
      
      filterMovies(movies, searchQuery);
      setIsLoading(false);
    }, 1000);
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
        isLoading={props.isLoading}
        saveResults={true}
      />
      <Preloader isLoading={isLoading}/>
      <Errors errorFromServer={props.errorFromServer} isLoading={isLoading} />
      <>
        <MoviesCardList 
          moviesData={moviesToShow}
          errorFromServer={props.errorFromServer}
          handleMovieSave={props.handleMovieSave}
          handleMovieRemove={props.handleMovieRemove}
          userMovies={props.userMovies}
        />
        {moviesToShow.length && filteredMovies.length !== moviesToShow.length
          ?
          <div className="button-more-container">
            <button className="Movies__more-button" onClick={onMoreClick}>Ещё</button>
          </div>
          :
          ''
        }
      </>
    
    </div>
  );
}

export default Movies;
