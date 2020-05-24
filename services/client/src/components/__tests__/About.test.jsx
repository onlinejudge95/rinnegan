import React from "react";
import { render, cleanup } from "@testing-library/react";

import About from "../About";

afterEach(cleanup);

it("renders about", () => {
  const dom = render(<About />);
  expect(dom.getByText("Sentimental")).toHaveClass("title is-1");
});

it("renders", () => {
  const dom = render(<About />);
  expect(dom.asFragment()).toMatchSnapshot();
});
