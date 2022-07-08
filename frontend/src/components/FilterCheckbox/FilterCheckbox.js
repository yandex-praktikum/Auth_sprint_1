import React from 'react';

function FilterCheckbox(props) {
  return (
    <div className='FilterCheckbox'>
        <button className={
              props.active ? 
                  'FilterCheckbox__checkbox' 
                  : 
                  'FilterCheckbox__checkbox FilterCheckbox__checkbox_inactive'
              } 
            onClick={props.onClick}
            />
        <p className='FilterCheckbox__checkbox-text'>Короткометражки</p>
    </div>
  );
}

export default FilterCheckbox;

