import React from "react";
import { render, cleanup } from "@testing-library/react";

import App from "../../App";

afterEach(cleanup);

it("renders", () => {
  const dom = renderWithRouter(<App />);
  expect(dom.asFragment()).toMatchSnapshot();
});
