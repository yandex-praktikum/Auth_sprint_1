import React from 'react';
import ValidatedForm from '../ValidatedForm/ValidatedForm';
import { validateProfileForm } from '../../utils/validators';
import {CurrentUserContext} from '../../contexts/CurrentUserContext';


function Profile(props) {

  const {currentUser} = React.useContext(CurrentUserContext);
  

  React.useEffect(() => {
    props.setErrorFromServer("");
  }, [])


  const {
    values,
    errors,
    handleChange,
    handleSubmit,
    changed,
  } = ValidatedForm(currentUser, props.handleProfileEdit, validateProfileForm, props.setErrorFromServer);

  function checButtonDisabled() {
    if (Object.keys(errors).length !== 0 || Object.values(values).join('') === '' || (currentUser.name === values.name && currentUser.email === values.email)) {
      return true;
    } else return false;
  }

  return (
    <div className="Profile">
      <p className="Profile__greeting">Привет, {currentUser.name}!</p>
      <form className="Profile__values" noValidate>
          {errors.name && (
            <span className="Form__error-message">{errors.name}</span>
          )}
          <p className="Profile__label">Имя</p>
          <input type="text" className="Profile__value" name="name" value={values.name || currentUser.name} onChange={handleChange} />
          {errors.email && (
            <span className="Form__error-message">{errors.email}</span>
          )}
          <div className="Profile__border" />

          <p className="Profile__label">E-mail</p>
          <input type="email" className="Profile__value" name="email" value={values.email || currentUser.email} onChange={handleChange} />
          
          <div className="form__error-container">
            <p className="form__error-message">{props.errorFromServer}</p>
          </div>
        </form>
        <button type="submit" 
                className={!checButtonDisabled() ? `Profile__edit-button` : `Profile__edit-button Profile__edit-button_disabled`} 
                disabled={checButtonDisabled()}
                onClick={handleSubmit}
                >Редактировать</button>
        <button className="Profile__logout-button" onClick={props.handleLogout}>Выйти из аккаунта</button>
    </div>
  );
}

export default Profile;

