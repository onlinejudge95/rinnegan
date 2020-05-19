import React from "react";
import { cleanup, render } from "@testing-library/react";

import RegisterForm from "../RegisterForm";

afterEach(cleanup);

it("renders registration form", () => {
  const { getByText } = render(<RegisterForm />);
  expect(getByText("Register")).toHaveClass("title");
});

it("renders", () => {
  const { asFragment } = render(<RegisterForm />);
  expect(asFragment()).toMatchSnapshot();
});
