import React from 'react';
import headerLogoPath from '../../images/logo.svg';
import Form from '../Form/Form';
import { Link } from 'react-router-dom';
import ValidatedForm from '../ValidatedForm/ValidatedForm';
import { validateLoginForm } from '../../utils/validators';

function Login(props) {

  const {
    values,
    errors,
    handleChange,
    handleSubmit,
    changed,
  } = ValidatedForm({}, props.handleSubmit, validateLoginForm, props.setErrorFromServer);

  React.useEffect(() => {
    props.setErrorFromServer("");
  }, []);

  return (
    <div className="Login">
      <Link to="/" className="Login__logo" target="_self">
        <img src={headerLogoPath} alt="Логотип проекта" />
      </Link>
      <Form
        name="login"
        title="Рады видеть!"
        buttonText="Войти" 
        onSubmit={handleSubmit}
        errorFromServer={props.errorFromServer}
        errors={errors}
        changed={changed}
      >
        <div className="Form__input-group">
          <span className="Form__field-title">E-mail</span>
          <input type="email" 
                 className={`Form__field ${errors.email && "Form__field_invalid"}`}
                 placeholder="" 
                 name="email" 
                 required 
                 value={values.email || ""} 
                 onChange={handleChange}
                  />
          {errors.email && (
            <span className="Form__error-message">{errors.email}</span>
          )}
        </div>

        <div className="Form__input-group">
          <span className="Form__field-title">Пароль</span>
          <input type="password" 
                 className={`Form__field ${errors.password && "Form__field_invalid"}`}
                 placeholder="" 
                 name="password" 
                 required value={values.password || ""} onChange={handleChange} 
                 />
          {errors.password && (
            <span className="Form__error-message">{errors.email}</span>
          )}
        </div>
      </Form>
      <div className="Login__link">
        <p className="Login__link-hint">Ещё не зарегистрированы?</p>
        <Link className="Login__back-link" to="/signup">Регистрация</Link>
      </div>
      
    </div>
  );
}

export default Login;

