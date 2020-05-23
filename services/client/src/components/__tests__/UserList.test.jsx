import React from "react";
import { render, cleanup } from "@testing-library/react";

import UserList from "../UserList";

afterEach(cleanup);

const userList = [
  { id: 1, username: "test_user_one", email: "test_user_one@mail.com" },
  { id: 2, username: "test_user_two", email: "test_user_two@mail.com" },
];

const mockProps = {
  users: userList,
  removeUser: () => {
    return true;
  },
  isAuthenticated: () => {
    return true;
  },
};

it("renders a username", () => {
  const dom = render(<UserList {...mockProps} />);
  expect(dom.getByText("test_user_one")).toHaveClass("username");
  expect(dom.getByText("test_user_two")).toHaveClass("username");
});

it("renders", () => {
  const dom = render(<UserList {...mockProps} />);
  expect(dom.asFragment()).toMatchSnapshot();
});
