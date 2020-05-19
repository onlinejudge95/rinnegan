import React from "react";
import { cleanup, render } from "@testing-library/react";

import LoginForm from "../LoginForm";

afterEach(cleanup);

it("renders login form", () => {
  const { getByText } = render(<LoginForm />);
  expect(getByText("Log In")).toHaveClass("title");
});

it("renders", () => {
  const { asFragment } = render(<LoginForm />);
  expect(asFragment()).toMatchSnapshot();
});
