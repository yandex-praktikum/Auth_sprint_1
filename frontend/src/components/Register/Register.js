import React from 'react';
import Form from '../Form/Form';
import headerLogoPath from '../../images/logo.svg';
import { Link } from 'react-router-dom';
import ValidatedForm from '../ValidatedForm/ValidatedForm';
import { validateRegisterForm } from '../../utils/validators';


function Register(props) {

  const {
    values,
    errors,
    handleChange,
    handleSubmit,
    changed,
  } = ValidatedForm({}, props.handleSubmit, validateRegisterForm, props.setErrorFromServer);

  React.useEffect(() => {
    props.setErrorFromServer("");
  }, []);

  return (
    <div className="Register">
      <Link to="/" className="Register__logo" target="_self">
        <img src={headerLogoPath} alt="Логотип проекта" />
      </Link>
      <Form
        name="login"
        title="Добро пожаловать!"
        buttonText="Зарегистрироваться" 
        onSubmit={handleSubmit}
        errorFromServer={props.errorFromServer}
        errors={errors}
        changed={changed}
      >
        <div className="Form__input-group">
          <span className="Form__field-title">Имя</span>
          <input type="text" className={`Form__field ${errors.name && "Form__field_invalid"}`} placeholder="" name="name" required value={values.name || ""} onChange={handleChange} />
          {errors.name && (
            <span className="Form__error-message">{errors.name}</span>
          )}
        </div>

        <div className="Form__input-group">
          <span className="Form__field-title">E-mail</span>
          <input type="email" className={`Form__field ${errors.email && "Form__field_invalid"}`} placeholder="" name="email" required value={values.email || ""} onChange={handleChange} />
          {errors.email && (
            <span className="Form__error-message">{errors.email}</span>
          )}
        </div>
          
        <div className="Form__input-group"> 
          <span className="Form__field-title">Пароль</span>
          <input type="password" className={`Form__field ${errors.password && "Form__field_invalid"}`} placeholder="" name="password" required value={values.password || ""} onChange={handleChange} />
          {errors.password && (
            <span className="Form__error-message">{errors.password}</span>
          )}
        </div>
      </Form>
      <div className="Register__link">
        <p className="Register__link-hint">Уже зарегистрированы?</p>
        <Link className="Register__back-link" to="/signin">Войти</Link>
      </div>
    </div>
  );
}

export default Register;

