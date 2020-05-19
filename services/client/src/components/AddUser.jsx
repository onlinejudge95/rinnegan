import React from "react";
import PropTypes from "prop-types";
import { Formik } from "formik";
import * as Yup from "yup";
import "./form.css";

const AddUser = (props) => {
  return (
    <Formik
      initialValues={{
        username: "",
        email: "",
        password: "",
      }}
      onSubmit={(values, { setSubmitting, resetForm }) => {
        props.addUser(values);
        resetForm();
        setSubmitting(false);
      }}
      validationSchema={Yup.object().shape({
        username: Yup.string()
          .required("Username is required")
          .min(6, "Username must be greater than 5 characters."),
        email: Yup.string()
          .email("Enter a valid email")
          .required("Email is required")
          .min(6, "Email must be greater than 5 characters."),
        password: Yup.string()
          .required("Password is required")
          .min(11, "Password must be greater than 10 characters."),
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
                  errors.username && touched.username ? "input error" : "input"
                }
              />
              {errors.username && touched.username && (
                <div className="input-feedback">{errors.username}</div>
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
                <div className="input-feedback">{errors.email}</div>
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
                  errors.password && touched.password ? "input error" : "input"
                }
              />
              {errors.password && touched.password && (
                <div className="input-feedback">{errors.password}</div>
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
  );
};

AddUser.propTypes = {
  addUser: PropTypes.func.isRequired,
};

export default AddUser;
