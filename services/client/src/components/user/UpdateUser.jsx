import React from "react";
import { Redirect } from "react-router-dom";
import { PropTypes } from "prop-types";
import { Formik } from "formik";
import * as Yup from "yup";

const UpdateUser = (props) => {
  if (!props.isAuthenticated()) {
    return <Redirect to="/login" />;
  }

  return (
    <div className="ui container">
      <div className="ui relaxed divided padded full grid container">
        <div className="row">
          <div className="ui huge header">Update</div>
        </div>
        <div className="ui divider"></div>
        <div className="row">
          <div className="eleven wide column">
            <Formik
              initialValues={{
                username: props.user.username,
                email: props.user.email,
                password: props.user.password,
              }}
              onSubmit={(values, { setSubmitting, resetForm }) => {
                props.onUpdateUserFormSubmit(values);
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
                password: Yup.string().min(
                  11,
                  "Password must be greater than 10 characters"
                ),
                passwordConfirm: Yup.string()
                  .min(11, "Password must be greater than 10 characters")
                  .oneOf([Yup.ref("password")], "Passwords must match"),
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
                    <div className="field">
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
                    <div className="field">
                      <label htmlFor="input-password-confirm">
                        Confirm Password
                      </label>
                      <input
                        name="passwordConfirm"
                        id="input-password-confirm"
                        type="password"
                        placeholder="Confirm your Password"
                        value={props.values.passwordConfirm}
                        onBlur={props.handleBlur}
                        onChange={props.handleChange}
                      />
                      {props.errors.passwordConfirm &&
                        props.touched.passwordConfirm && (
                          <div className="ui pointing red basic label">
                            {props.errors.passwordConfirm}
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

UpdateUser.propTypes = {
  user: PropTypes.object,
  onUpdateUserFormSubmit: PropTypes.func.isRequired,
  isAuthenticated: PropTypes.func.isRequired,
};

export default UpdateUser;
