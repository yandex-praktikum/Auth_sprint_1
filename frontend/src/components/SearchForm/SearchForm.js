import React from 'react';
import FilterCheckbox from '../FilterCheckbox/FilterCheckbox';

function SearchForm(props) {

  function onFilterShortFilmsClick(e) {
    e.preventDefault();
    props.setFilterShortFilms(!props.filterShortFilms);
    if (props.saveResults) {
      localStorage.setItem('filterShortFilms', JSON.stringify(!props.filterShortFilms));
    }
  }

  function handleSearchQuery(e) {
    props.setErrorFromServer("");
    if (props.saveResults) {
      localStorage.setItem('searchQuery', JSON.stringify(e.target.value));
    }
    props.setSearchQuery(e.target.value)
  }
  

  return (
    <div className='SearchForm'>
      <form onSubmit={props.handleSubmit}>
        <div className='SearchForm__field-container'>
          <input type='text' 
                 value={props.searchQuery || ''}
                 className='SearchForm__field' 
                 placeholder='Фильм'  
                 onChange={handleSearchQuery}
                 />
          <button className={`SearchForm__button ${props.isLoading && "SearchForm__button_inactive" }`}>
            Поиск
          </button>
        </div>
        <FilterCheckbox
          active={props.filterShortFilms}
          onClick={onFilterShortFilmsClick}
        />
      </form>
    </div>
  );
}

export default SearchForm;

