import React from "react";
import { Link } from "react-router-dom";
import { PropTypes } from "prop-types";

const NavBar = (props) => {
  const profileMenu = (
    <div className="item">
      <Link to="/profile">
        <i className="icon user" />
        Profile
      </Link>
    </div>
  );
  const keywordMenu = (
    <div className="item">
      <Link to="/keyword">
        <i className="icon newspaper" />
        Sentiments
      </Link>
    </div>
  );
  const unAuthenticatedMenu = (
    <div className="right menu">
      <div className="item">
        <Link to="/register">
          <i className="icon signup" />
          Sign-Up
        </Link>
      </div>
      <div className="item">
        <Link to="/login">
          <i className="icon sign-in" />
          Sign-In
        </Link>
      </div>
    </div>
  );
  const authenticatedMenu = (
    <div className="right menu">
      <div className="item">
        <span onClick={props.handleLogOutClick}>
          <i className="icon sign-out" />
          Sign-Out
        </span>
      </div>
    </div>
  );
  return (
    <div className="ui inverted pointing attached menu labeled icon massive stackable">
      <div className="item">
        <Link to="/">
          <i className="icon eye" />
          Rinnegan
        </Link>
      </div>
      {props.isAuthenticated() ? profileMenu : null}
      {props.isAuthenticated() ? keywordMenu : null}
      {props.isAuthenticated() ? authenticatedMenu : unAuthenticatedMenu}
    </div>
  );
};

NavBar.propTypes = {
  handleLogOutClick: PropTypes.func.isRequired,
  isAuthenticated: PropTypes.func.isRequired,
};

export default NavBar;
