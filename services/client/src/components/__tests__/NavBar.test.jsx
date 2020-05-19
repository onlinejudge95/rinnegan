import React from "react";
import { cleanup } from "@testing-library/react";

import NavBar from "../NavBar";

afterEach(cleanup);

const props = {
  title: "Hello World!",
  handleLogOutUser: () => {
    return tr;
  },
};
const title = "Hello World!";

it("renders title", () => {
  const { getByText } = renderWithRouter(<NavBar {...props} />);
  expect(getByText(title)).toHaveClass("nav-title");
});

it("renders", () => {
  const { asFragment } = renderWithRouter(<NavBar {...props} />);
  expect(asFragment()).toMatchSnapshot();
});
