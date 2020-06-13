import React from "react";
import { Redirect } from "react-router-dom";
import { PropTypes } from "prop-types";
import { Formik } from "formik";
import * as Yup from "yup";

const RegisterUser = (props) => {
  if (props.isAuthenticated()) {
    return <Redirect to="/" />;
  }

  return (
    <div className="ui container">
      <div className="ui relaxed divided padded full grid">
        <div className="row">
          <div className="ui huge header">Sign-Up</div>
        </div>
        <div className="ui divider"></div>
        <div className="row">
          <div className="eleven wide column">
            <Formik
              initialValues={{
                username: "",
                email: "",
                password: "",
              }}
              onSubmit={(values, { setSubmitting, resetForm }) => {
                props.onRegisterFormSubmit(values);
                resetForm();
                setSubmitting(false);
              }}
              validationSchema={Yup.object().shape({
                username: Yup.string()
                  .required("Username is required")
                  .min(6, "Username must be greater than 5 characters"),
                email: Yup.string()
                  .required("Email is required")
                  .email("Enter a valid email"),
                password: Yup.string()
                  .required("Password is required")
                  .min(11, "Password must be greater than 10 characters"),
              })}
            >
              {(props) => {
                return (
                  <form className="ui form" onSubmit={props.handleSubmit}>
                    <div className="required field">
                      <label htmlFor="input-username">Username</label>
                      <input
                        name="username"
                        id="input-username"
                        type="text"
                        placeholder="Enter your username"
                        value={props.values.username}
                        onBlur={props.handleBlur}
                        onChange={props.handleChange}
                      />
                      {props.errors.username && props.touched.username && (
                        <div className="ui pointing red basic label">
                          {props.errors.username}
                        </div>
                      )}
                    </div>
                    <div className="required field">
                      <label htmlFor="input-email">Email</label>
                      <input
                        name="email"
                        id="input-email"
                        type="email"
                        placeholder="Enter your email"
                        value={props.values.email}
                        onBlur={props.handleBlur}
                        onChange={props.handleChange}
                      />
                      {props.errors.email && props.touched.email && (
                        <div className="ui pointing red basic label">
                          {props.errors.email}
                        </div>
                      )}
                    </div>
                    <div className="required field">
                      <label htmlFor="input-password">Password</label>
                      <input
                        name="password"
                        id="input-password"
                        type="password"
                        placeholder="Enter your Password"
                        value={props.values.password}
                        onBlur={props.handleBlur}
                        onChange={props.handleChange}
                      />
                      {props.errors.password && props.touched.password && (
                        <div className="ui pointing red basic label">
                          {props.errors.password}
                        </div>
                      )}
                    </div>
                    <input
                      className="ui green button"
                      type="submit"
                      value="Submit"
                      disabled={props.isSubmitting}
                    />
                  </form>
                );
              }}
            </Formik>
          </div>
        </div>
      </div>
    </div>
  );
};

RegisterUser.propTypes = {
  onRegisterFormSubmit: PropTypes.func.isRequired,
  isAuthenticated: PropTypes.func.isRequired,
};

export default RegisterUser;
