import React from "react";
import { Formik } from "formik";
import * as Yup from "yup";
import {
  Button,
  Divider,
  Header,
  Form,
  Input,
  Container,
} from "semantic-ui-react";

const RegisterUser = (props) => {
  return (
    <main className="content">
      <Container>
        <div className="ui relaxed divided padded full grid">
          <div className="row">
            <div className="column">
              <Header as="h1">Sign-Up</Header>
            </div>
          </div>
          <Divider />
          <div className="row">
            <div className="eleven wide column">
              <Formik
                initialValues={{ userName: "", email: "", password: "" }}
                onSubmit={(values, { setSubmitting, resetForm }) => {
                  props.onRegisterFormSubmit(values);
                  resetForm();
                  setSubmitting(false);
                }}
                validationSchema={Yup.object().shape({
                  userName: Yup.string()
                    .required("Username is required")
                    .min(6, "Username must be greater than 6 characters"),
                  email: Yup.string()
                    .required("Email is required")
                    .email("Enter a valid email"),
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
                    <Form onSubmit={handleSubmit}>
                      <Form.Field>
                        <label htmlFor="input-username">Username</label>
                        <input
                          name="username"
                          id="input-username"
                          placeholder="Username"
                          value={values.userName}
                          onBlur={handleBlur}
                          onChange={handleChange}
                          type="text"
                          className={
                            errors.userName && touched.userName
                              ? "ui input error"
                              : "ui input"
                          }
                        />
                      </Form.Field>
                      <Form.Field>
                        <label>Email</label>
                        <Input placeholder="Email" type="email" />
                      </Form.Field>
                      <Form.Field>
                        <label>Password</label>
                        <Input placeholder="Password" type="password" />
                      </Form.Field>
                      <button
                        className="ui button green"
                        type="submit"
                        disabled={isSubmitting}
                      >
                        Submit
                      </button>
                    </Form>
                  );
                }}
              </Formik>
            </div>
          </div>
        </div>
      </Container>
    </main>
  );
};

export default RegisterUser;
