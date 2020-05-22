import React from "react";
import { cleanup, wait } from "@testing-library/react";

import NavBar from "../NavBar";

afterEach(cleanup);

describe("when authenticated", () => {
  const mockProps = {
    title: "Hello World!",
    handleLogOutUser: () => {
      return true;
    },
    isAuthenticated: jest.fn().mockImplementation(() => true),
  };

  it("renders the default props", async () => {
    const dom = renderWithRouter(<NavBar {...mockProps} />);

    expect(dom.getByText(mockProps.title)).toHaveClass("nav-title");

    await wait(() => {
      expect(mockProps.isAuthenticated).toHaveBeenCalledTimes(1);
    });
    expect((await findByTestId("nav-about")).innerHTML).toBe("About");
    expect((await findByTestId("nav-status")).innerHTML).toBe("User Status");
    expect((await findByTestId("nav-logout")).innerHTML).toBe("Log Out");
  });

  it("renders a snapshot properly", () => {
    const dom = renderWithRouter(<NavBar {...mockProps} />);
    expect(dom.asFragment()).toMatchSnapshot();
  });
});

describe("when unauthenticated", () => {
  const mockProps = {
    title: "Hello World!",
    handleLogOutUser: () => {
      return true;
    },
    isAuthenticated: jest.fn().mockImplementation(() => false),
  };

  it("renders the default props", async () => {
    const dom = renderWithRouter(<NavBar {...mockProps} />);

    expect(dom.getByText(mockProps.title)).toHaveClass("nav-title");

    await wait(() => {
      expect(mockProps.isAuthenticated).toHaveBeenCalledTimes(1);
    });
    expect((await findByTestId("nav-about")).innerHTML).toBe("About");
    expect((await findByTestId("nav-register")).innerHTML).toBe("Register");
    expect((await findByTestId("nav-login")).innerHTML).toBe("Log In");
  });

  it("renders a snapshot properly", () => {
    const dom = renderWithRouter(<NavBar {...mockProps} />);
    expect(dom.asFragment()).toMatchSnapshot();
  });
});
