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
  const dom = renderWithRouter(<NavBar {...props} />);
  expect(dom.getByText(title)).toHaveClass("nav-title");
});

it("renders", () => {
  const dom = renderWithRouter(<NavBar {...props} />);
  expect(dom.asFragment()).toMatchSnapshot();
});
