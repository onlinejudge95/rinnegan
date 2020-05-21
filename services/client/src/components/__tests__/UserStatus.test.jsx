import React from "react";
import { render, cleanup, wait } from "@testing-library/react";
import axios from "axios";

import UserStatus from "../UserStatus";

afterEach(cleanup);

jest.mock("axios");

it("renders properly when authenticated", async () => {
  axios.get.mockImplementationOnce(() =>
    Promise.resolve({
      data: { email: "test_user@mail.com", username: "test_user" },
    })
  );

  const dom = render(<UserStatus />);

  expect((await dom.findByTestId("user-email")).innerHTML).toBe(
    "test_user@mail.com"
  );
  expect((await dom.findByTestId("user-username")).innerHTML).toBe("test_user");
});
