import React from "react";
import { Redirect } from "react-router-dom";
import { Formik } from "formik";
import * as Yup from "yup";
import { PropTypes } from "prop-types";

const RegisterForm = (props) => {
  if (props.isAuthenticated()) {
    return <Redirect to="/" />;
  }

  return (
    <div>
      <h1 className="title is-1">Register</h1>
      <hr />
      <br />
      <Formik
        initialValues={{
          username: "",
          email: "",
          password: "",
        }}
        onSubmit={(values, { setSubmitting, resetForm }) => {
          props.handleRegisterFormSubmit(values);
          resetForm();
          setSubmitting(false);
        }}
        validationSchema={Yup.object().shape({
          username: Yup.string()
            .required("Username is required")
            .min(6, "Username must be greater than 5 characters"),
          email: Yup.string()
            .required("Email is required")
            .min(6, "Email must be greater than 5 characters"),
          password: Yup.string()
            .required("Password is required")
            .min(11, "Password must be greater than 10 characters"),
        })}
      >
        {(props) => {
          const {
            values,
            touched,
            errors,
            isSubmitting,
            handleBlur,
            handleChange,
            handleSubmit,
          } = props;

          return (
            <form onSubmit={handleSubmit}>
              <div className="field">
                <label className="label" htmlFor="input-username">
                  Username
                </label>
                <input
                  name="username"
                  id="input-username"
                  type="text"
                  placeholder="Enter a Username"
                  value={values.username}
                  onBlur={handleBlur}
                  onChange={handleChange}
                  className={
                    errors.username && touched.username
                      ? "input error"
                      : "input"
                  }
                />
                {errors.username && touched.username && (
                  <div className="input-feedback" data-testid="errors-username">
                    {errors.username}
                  </div>
                )}
              </div>
              <div className="field">
                <label className="label" htmlFor="input-email">
                  Email
                </label>
                <input
                  name="email"
                  id="input-email"
                  type="email"
                  placeholder="Enter an Email address"
                  value={values.email}
                  onBlur={handleBlur}
                  onChange={handleChange}
                  className={
                    errors.email && touched.email ? "input error" : "input"
                  }
                />
                {errors.email && touched.email && (
                  <div className="input-feedback" data-testid="errors-email">
                    {errors.email}
                  </div>
                )}
              </div>
              <div className="field">
                <label className="label" htmlFor="input-password">
                  Password
                </label>
                <input
                  name="password"
                  id="input-password"
                  type="password"
                  placeholder="Enter a Password"
                  value={values.password}
                  onBlur={handleBlur}
                  onChange={handleChange}
                  className={
                    errors.password && touched.password
                      ? "input error"
                      : "input"
                  }
                />
                {errors.password && touched.password && (
                  <div className="input-feedback" data-testid="errors-password">
                    {errors.password}
                  </div>
                )}
              </div>
              <input
                type="submit"
                className="button is-primary"
                value="Submit"
                disabled={isSubmitting}
              />
            </form>
          );
        }}
      </Formik>
    </div>
  );
};

RegisterForm.propTypes = {
  handleRegisterFormSubmit: PropTypes.func.isRequired,
  isAuthenticated: PropTypes.func.isRequired,
};

export default RegisterForm;
