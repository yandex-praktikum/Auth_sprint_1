export function validateRegisterForm(values) {
  let errors = {};
  if (!values.name) {
    errors.name = 'Имя не может быть пустым';
  } else if (values.name.length < 2 || values.name.length > 30) {
    errors.name = 'Имя должно быть от 2 до 30 символов';
  } else if (!/^[a-zA-Zа-яА-Я -]+$/.test(values.name)) {
    errors.name = 'Имя только из латиницы, кириллицы, пробела или дефиса';
  } 
  if (!values.email) {
    errors.email = 'Емейл не может быть пустым';
  } else if (!/\S+@\S+\.\S+/.test(values.email)) {
    errors.email = 'Некорректный адрес электронной почты';
  }
  if (!values.password) {
    errors.password = 'Пароль не может быть пустым';
  } else if (values.password.length < 4) {
    errors.password = 'Пароль должен быть не менее 4 символов';
  }
  return errors;
};


export function validateLoginForm(values) {
  let errors = {};
  if (!values.email) {
    errors.email = 'Емейл не может быть пустым';
  } else if (!/\S+@\S+\.\S+/.test(values.email)) {
    errors.email = 'Некорректный формат почты';
  }
  if (!values.password) {
    errors.password = 'Пароль не может быть пустым';
  } else if (values.password.length < 4) {
    errors.password = 'Пароль должен быть не менее 4 символов';
  }
  return errors;
};


export function validateProfileForm(values) {
  let errors = {};
  if (values.name.length < 2 || values.name.length > 30) {
    errors.name = 'Имя должно быть от 2 до 30 символов';
  } else if (values.name && !/^[a-zA-Zа-яА-Я -]+$/.test(values.name)) {
    errors.name = 'Имя только из латиницы, кириллицы, пробела или дефиса';
  } 
  if (values.email && !/\S+@\S+\.\S+/.test(values.email)) {
    errors.email = 'Некорректный формат почты';
  }
  return errors;
};
