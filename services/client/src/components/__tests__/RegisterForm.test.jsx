import React from "react";
import { cleanup, fireEvent, wait } from "@testing-library/react";

import RegisterForm from "../RegisterForm";

afterEach(cleanup);

describe("renders", () => {
  const props = {
    handleRegisterFormSubmit: () => {
      return true;
    },
    isAuthenticated: () => {
      return false;
    },
  };

  it("registration form", () => {
    const { getByText } = renderWithRouter(<RegisterForm {...props} />);
    expect(getByText("Register")).toHaveClass("title");
  });

  it("default props", () => {
    const { getByLabelText, getByText } = renderWithRouter(
      <RegisterForm {...props} />
    );

    const usernameInput = getByLabelText("Username");
    expect(usernameInput).toHaveAttribute("type", "text");
    expect(usernameInput).not.toHaveValue();

    const emailInput = getByLabelText("Email");
    expect(emailInput).toHaveAttribute("type", "email");
    expect(emailInput).not.toHaveValue();

    const passwordInput = getByLabelText("Password");
    expect(passwordInput).toHaveAttribute("type", "password");
    expect(passwordInput).not.toHaveValue();

    const buttonInput = getByText("Submit");
    expect(buttonInput).toHaveValue("Submit");
  });

  it("a snapshot properly", () => {
    const { asFragment } = renderWithRouter(<RegisterForm {...props} />);
    expect(asFragment()).toMatchSnapshot();
  });
});

describe("handles form validation correctly", () => {
  it("when fields are empty", async () => {
    const mockProps = {
      handleRegisterFormSubmit: jest.fn(),
      isAuthenticated: jest.fn(),
    };

    const { getByLabelText, container, findByTestId } = renderWithRouter(
      <RegisterForm {...mockProps} />
    );

    expect(mockProps.handleRegisterFormSubmit).toHaveBeenCalledTimes(0);

    const usernameInput = getByLabelText("Username");
    fireEvent.blur(usernameInput);
    expect((await findByTestId("errors-username")).innerHTML).toBe(
      "Username is required"
    );

    const emailInput = getByLabelText("Email");
    fireEvent.blur(emailInput);
    expect((await findByTestId("errors-email")).innerHTML).toBe(
      "Email is required"
    );

    const passwordInput = getByLabelText("Password");
    fireEvent.blur(passwordInput);
    expect((await findByTestId("errors-password")).innerHTML).toBe(
      "Password is required"
    );

    const form = container.querySelector("form");
    fireEvent.submit(form);

    await wait(() => {
      expect(mockProps.handleRegisterFormSubmit).toHaveBeenCalledTimes(0);
    });
  });

  it("when email field is not valid", async () => {
    const mockProps = {
      handleRegisterFormSubmit: jest.fn(),
      isAuthenticated: jest.fn(),
    };

    const { getByLabelText, container, findByTestId } = renderWithRouter(
      <RegisterForm {...mockProps} />
    );

    expect(mockProps.handleRegisterFormSubmit).toHaveBeenCalledTimes(0);

    const emailInput = getByLabelText("Email");
    fireEvent.change(emailInput, { target: { value: "invalid_mail" } });
    fireEvent.blur(emailInput);
    expect((await findByTestId("errors-email")).innerHTML).toBe(
      "Enter a valid email"
    );

    const form = container.querySelector("form");
    fireEvent.submit(form);

    await wait(() => {
      expect(mockProps.handleRegisterFormSubmit).toHaveBeenCalledTimes(0);
    });
  });

  // it("when fields are not the proper length", async () => {});

  // it("when fields are valid", async () => {});
});
