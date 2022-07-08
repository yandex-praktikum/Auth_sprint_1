import React from 'react';

function Form(props) {

  function onSubmit(e) {
    e.preventDefault();
    props.onSubmit(e);
  }

  return (
    <form className="Form" name={props.name} onSubmit={onSubmit} noValidate>
    <h2 className="Form__title">{props.title}</h2>
    {props.children}
    <div className="form__error-container">
      <p className="form__error-message">{props.errorFromServer}</p>
    </div>
    <button type="submit" className={
      (Object.keys(props.errors).length === 0 && props.changed) 
        ? 
        `Form__save-button` 
        : 
        `Form__save-button Form__save-button_inactive`}

      disabled={!Object.keys(props.errors).length === 0 || !props.changed}
    >
        {props.buttonText}
    </button>
    </form>
  );
}

export default Form;

