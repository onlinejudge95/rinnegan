import React from "react";
import { cleanup, fireEvent, wait } from "@testing-library/react";

import LoginForm from "../LoginForm";

afterEach(cleanup);

describe("renders", () => {
  const mockProps = {
    handleLoginFormSubmit: () => {
      return true;
    },
    isAuthenticated: () => {
      return false;
    },
  };

  it("login form", () => {
    const dom = renderWithRouter(<LoginForm {...mockProps} />);
    expect(dom.getByText("Log In")).toHaveClass("title");
  });

  it("default props", () => {
    const dom = renderWithRouter(<LoginForm {...mockProps} />);

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
    renderWithRouter;
    const dom = renderWithRouter(<LoginForm {...mockProps} />);
    expect(dom.asFragment()).toMatchSnapshot();
  });
});

describe("handles form validation correctly", () => {
  const mockProps = {
    handleLoginFormSubmit: jest.fn(),
    isAuthenticated: jest.fn(),
  };

  it("when fields are empty", async () => {
    const dom = renderWithRouter(<LoginForm {...mockProps} />);

    expect(mockProps.handleLoginFormSubmit).toHaveBeenCalledTimes(0);

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
      expect(mockProps.handleLoginFormSubmit).toHaveBeenCalledTimes(0);
    });
  });

  it("when email field is not valid", async () => {
    const dom = renderWithRouter(<LoginForm {...mockProps} />);

    expect(mockProps.handleLoginFormSubmit).toHaveBeenCalledTimes(0);

    const emailInput = dom.getByLabelText("Email");
    fireEvent.change(emailInput, { target: { value: "test_user" } });
    fireEvent.blur(emailInput);
    expect((await dom.findByTestId("errors-email")).innerHTML).toBe(
      "Enter a valid email"
    );

    const form = dom.container.querySelector("form");
    fireEvent.submit(form);

    await wait(() => {
      expect(mockProps.handleLoginFormSubmit).toHaveBeenCalledTimes(0);
    });
  });

  it("when fields are not the proper length", async () => {
    const dom = renderWithRouter(<LoginForm {...mockProps} />);

    expect(mockProps.handleLoginFormSubmit).toHaveBeenCalledTimes(0);

    const emailInput = dom.getByLabelText("Email");
    fireEvent.change(emailInput, { target: { value: "t@t.c" } });
    fireEvent.blur(emailInput);
    expect((await dom.findByTestId("errors-email")).innerHTML).toBe(
      "Email must be greater than 5 characters"
    );

    const passwordInput = dom.getByLabelText("Password");
    fireEvent.change(passwordInput, { target: { value: "invalid" } });
    fireEvent.blur(passwordInput);
    expect((await dom.findByTestId("errors-password")).innerHTML).toBe(
      "Password must be greater than 10 characters"
    );

    const form = dom.container.querySelector("form");
    fireEvent.submit(form);

    await wait(() => {
      expect(mockProps.handleLoginFormSubmit).toHaveBeenCalledTimes(0);
    });
  });

  it("when fields are valid", async () => {
    const dom = renderWithRouter(<LoginForm {...mockProps} />);

    expect(mockProps.handleLoginFormSubmit).toHaveBeenCalledTimes(0);

    const emailInput = dom.getByLabelText("Email");
    fireEvent.change(emailInput, { target: { value: "test_user@mail.com" } });
    fireEvent.blur(emailInput);

    const passwordInput = dom.getByLabelText("Password");
    fireEvent.change(passwordInput, { target: { value: "test_password" } });
    fireEvent.blur(passwordInput);

    const form = dom.container.querySelector("form");
    fireEvent.submit(form);

    await wait(() => {
      expect(mockProps.handleLoginFormSubmit).toHaveBeenCalledTimes(1);
    });
  });
});
