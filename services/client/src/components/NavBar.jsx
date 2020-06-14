import React from "react";
import { Link } from "react-router-dom";
import { Icon, Menu } from "semantic-ui-react";

const NavBar = () => {
  return (
    <Menu size="massive" icon="labeled" inverted pointing attached>
      <Menu.Item as={Link} to="/">
        Rinnegan
      </Menu.Item>
      <Menu.Item as={Link} to="/profile">
        <Icon name="user" />
        Profile
      </Menu.Item>
      <Menu.Menu position="right">
        <Menu.Item as={Link} to="/register">
          <Icon name="signup" />
          Sign-Up
        </Menu.Item>
        <Menu.Item as={Link} to="/login">
          <Icon name="sign-in" />
          Sign-In
        </Menu.Item>
      </Menu.Menu>
    </Menu>
  );
};

export default NavBar;
