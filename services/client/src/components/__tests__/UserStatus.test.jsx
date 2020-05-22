import React from "react";
import { render, cleanup, wait } from "@testing-library/react";
import axios from "axios";

import UserStatus from "../UserStatus";
import { Route } from "react-router-dom";

afterEach(cleanup);

jest.mock("axios");

axios.get.mockImplementation(() =>
  Promise.resolve({
    data: { email: "test_user@mail.com", username: "test_user" },
  })
);

const mockProps = {
  isAuthenticated: () => {
    return true;
  },
};

it("renders properly when authenticated", async () => {
  const dom = render(<UserStatus {...mockProps} />);

  await wait(() => {
    expect(axios.get).toHaveBeenCalledTimes(1);
  });

  expect((await dom.findByTestId("user-email")).innerHTML).toBe(
    "test_user@mail.com"
  );
  expect((await dom.findByTestId("user-username")).innerHTML).toBe("test_user");
});

it("renders", async () => {
  const dom = renderWithRouter(<UserStatus {...mockProps} />);

  await wait(() => {
    expect(axios.get).toHaveBeenCalled();
  });

  expect(dom.asFragment()).toMatchSnapshot();
});

// TODO:- Write test for validating a refresh token if it has been altered and a new tab is opened with the status Route, it should redirect to login route
