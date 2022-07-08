import React  from 'react';

function ValidatedForm(initialValues, callback, validate, setErrorFromServer) {

  const [values, setValues] = React.useState(initialValues || {});
  const [errors, setErrors] = React.useState({});
  const [changed, setChanged] = React.useState(false);

  React.useEffect(() => {
    if (Object.keys(values).length !== 0) {
      setErrors(validate(values));
    }
  }, [values, validate])

  const handleChange = (e) => {
    setErrorFromServer("");
    setValues(values => ({ 
            ...values, 
            [e.target.name]: e.target.value 
          }));
    setChanged(true);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setErrors(validate(values));
    if (validate(values)) {
      callback(values);
    }
  };

  return {
    handleChange, handleSubmit, values, errors, changed
  }
};

export default ValidatedForm;