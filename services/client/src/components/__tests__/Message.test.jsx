import React from "react";
import { cleanup, render } from "@testing-library/react";

import Message from "../Message";

afterEach(cleanup);

describe("when 'messageType' is 'success'", () => {
  const mockProps = {
    messageType: "success",
    messageText: "Hello, World!",
    removeMessage: () => {
      return true;
    },
  };

  it("renders the default props", async () => {
    const dom = render(<Message {...mockProps} />);

    expect(dom.getByTestId("message").innerHTML).toContain("is-success");
    expect(dom.getByText("Hello, World!")).toHaveClass("message-text");
  });

  it("renders a snapshot", () => {
    const dom = render(<Message {...mockProps} />);

    expect(dom.asFragment()).toMatchSnapshot();
  });
});

describe("when 'messageType' is 'danger'", () => {
  const mockProps = {
    messageType: "danger",
    messageText: "Hello, World!",
    removeMessage: () => {
      return true;
    },
  };

  it("renders the default props", async () => {
    const dom = render(<Message {...mockProps} />);

    expect(dom.getByTestId("message").innerHTML).toContain("is-danger");
    expect(dom.getByText("Hello, World!")).toHaveClass("message-text");
  });

  it("renders a snapshot", () => {
    const dom = render(<Message {...mockProps} />);

    expect(dom.asFragment()).toMatchSnapshot();
  });
});
