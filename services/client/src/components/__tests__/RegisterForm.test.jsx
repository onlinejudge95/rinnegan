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
    const dom = renderWithRouter(<RegisterForm {...props} />);
    expect(dom.getByText("Register")).toHaveClass("title");
  });

  it("default props", () => {
    const dom = renderWithRouter(<RegisterForm {...props} />);

    const usernameInput = dom.getByLabelText("Username");
    expect(usernameInput).toHaveAttribute("type", "text");
    expect(usernameInput).not.toHaveValue();

    const emailInput = dom.getByLabelText("Email");
    expect(emailInput).toHaveAttribute("type", "email");
    expect(emailInput).not.toHaveValue();

    const passwordInput = dom.getByLabelText("Password");
    expect(passwordInput).toHaveAttribute("type", "password");
    expect(passwordInput).not.toHaveValue();

    const buttonInput = dom.getByText("Submit");
    expect(buttonInput).toHaveValue("Submit");
  });

  it("a snapshot properly", () => {
    const dom = renderWithRouter(<RegisterForm {...props} />);
    expect(dom.asFragment()).toMatchSnapshot();
  });
});

describe("handles form validation correctly", () => {
  const mockProps = {
    handleRegisterFormSubmit: jest.fn(),
    isAuthenticated: jest.fn(),
  };

  it("when fields are empty", async () => {
    const dom = renderWithRouter(<RegisterForm {...mockProps} />);

    expect(mockProps.handleRegisterFormSubmit).toHaveBeenCalledTimes(0);

    const usernameInput = dom.getByLabelText("Username");
    fireEvent.blur(usernameInput);
    expect((await dom.findByTestId("errors-username")).innerHTML).toBe(
      "Username is required"
    );

    const emailInput = dom.getByLabelText("Email");
    fireEvent.blur(emailInput);
    expect((await dom.findByTestId("errors-email")).innerHTML).toBe(
      "Email is required"
    );

    const passwordInput = dom.getByLabelText("Password");
    fireEvent.blur(passwordInput);
    expect((await dom.findByTestId("errors-password")).innerHTML).toBe(
      "Password is required"
    );

    const form = dom.container.querySelector("form");
    fireEvent.submit(form);

    await wait(() => {
      expect(mockProps.handleRegisterFormSubmit).toHaveBeenCalledTimes(0);
    });
  });

  it("when email field is not valid", async () => {
    const { getByLabelText, container, findByTestId } = renderWithRouter(
      <RegisterForm {...mockProps} />
    );

    expect(mockProps.handleRegisterFormSubmit).toHaveBeenCalledTimes(0);

    const emailInput = getByLabelText("Email");
    fireEvent.change(emailInput, { target: { value: "test_user" } });
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

  it("when fields are not the proper length", async () => {
    const { getByLabelText, container, findByTestId } = renderWithRouter(
      <RegisterForm {...mockProps} />
    );

    expect(mockProps.handleRegisterFormSubmit).toHaveBeenCalledTimes(0);

    const usernameInput = getByLabelText("Username");
    fireEvent.change(usernameInput, { target: { value: "null" } });
    fireEvent.blur(usernameInput);
    expect((await findByTestId("errors-username")).innerHTML).toBe(
      "Username must be greater than 5 characters"
    );

    const emailInput = getByLabelText("Email");
    fireEvent.change(emailInput, { target: { value: "t@t.c" } });
    fireEvent.blur(emailInput);
    expect((await findByTestId("errors-email")).innerHTML).toBe(
      "Email must be greater than 5 characters"
    );

    const passwordInput = getByLabelText("Password");
    fireEvent.change(passwordInput, { target: { value: "invalid" } });
    fireEvent.blur(passwordInput);
    expect((await findByTestId("errors-password")).innerHTML).toBe(
      "Password must be greater than 10 characters"
    );

    const form = container.querySelector("form");
    fireEvent.submit(form);

    await wait(() => {
      expect(mockProps.handleRegisterFormSubmit).toHaveBeenCalledTimes(0);
    });
  });

  it("when fields are valid", async () => {
    const { getByLabelText, container, findByTestId } = renderWithRouter(
      <RegisterForm {...mockProps} />
    );

    expect(mockProps.handleRegisterFormSubmit).toHaveBeenCalledTimes(0);

    const usernameInput = getByLabelText("Username");
    fireEvent.change(usernameInput, { target: { value: "test_user" } });
    fireEvent.blur(usernameInput);

    const emailInput = getByLabelText("Email");
    fireEvent.change(emailInput, { target: { value: "test_user@mail.com" } });
    fireEvent.blur(emailInput);

    const passwordInput = getByLabelText("Password");
    fireEvent.change(passwordInput, { target: { value: "test_password" } });
    fireEvent.blur(passwordInput);

    const form = container.querySelector("form");
    fireEvent.submit(form);

    await wait(() => {
      expect(mockProps.handleRegisterFormSubmit).toHaveBeenCalledTimes(1);
    });
  });
});
