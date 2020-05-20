import React from "react";
import { render, cleanup } from "@testing-library/react";

import AddUser from "../AddUser";

afterEach(cleanup);

const props = {
  addUser: () => {
    return true;
  },
};

it("renders with default props", () => {
  const dom = render(<AddUser {...props} />);

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

it("renders", () => {
  const { asFragment } = render(<AddUser {...props} />);
  expect(asFragment()).toMatchSnapshot();
});
