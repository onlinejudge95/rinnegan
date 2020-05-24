import React from "react";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";
import "./NavBar.css";

const titleStyle = {
  fontWeight: "bold",
};

const Navbar = (props) => {
  let menu = (
    <div className="navbar-menu">
      <div className="navbar-end">
        <Link to="/register" className="navbar-item" data-testid="nav-register">
          Register
        </Link>
        <Link to="/login" className="navbar-item" data-testid="nav-login">
          Log-In
        </Link>
      </div>
    </div>
  );

  if (props.isAuthenticated()) {
    menu = (
      <div className="navbar-menu">
        <div className="navbar-start">
          <Link to="/profile" className="navbar-item" data-testid="nav-profile">
            Profile
          </Link>
        </div>

        <div className="navbar-end">
          <span
            onClick={props.handleLogOutUser}
            className="navbar-item"
            data-testid="nav-logout"
          >
            Log-Out
          </span>
        </div>
      </div>
    );
  }
  return (
    <nav
      className="navbar is-dark"
      role="navigation"
      aria-label="main navigation"
    >
      <section className="container">
        <div className="navbar-brand">
          <Link to="/" className="navbar-item nav-title" style={titleStyle}>
            {props.title}
          </Link>
          <span
            className="nav-toggle navbar-burger"
            onClick={() => {
              let toggle = document.querySelector(".nav-toggle");
              toggle.classList.toggle("is-active");

              let menu = document.querySelector(".navbar-menu");
              menu.classList.toggle("is-active");
            }}
          >
            <span />
            <span />
            <span />
          </span>
        </div>
        {menu}
      </section>
    </nav>
  );
};

Navbar.propTypes = {
  title: PropTypes.string.isRequired,
  handleLogOutUser: PropTypes.func.isRequired,
  isAuthenticated: PropTypes.func.isRequired,
};

export default Navbar;
