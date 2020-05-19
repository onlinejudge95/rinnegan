import React from "react";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";
import "./NavBar.css";

const titleStyle = {
  fontWeight: "bold",
};

const Navbar = (props) => {
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
        <div className="navbar-menu">
          <div className="navbar-start">
            <Link to="/about" className="navbar-item">
              About
            </Link>
            <Link to="/status" className="navbar-item">
              User Status
            </Link>
          </div>
          <div className="navbar-end">
            <Link to="/register" className="navbar-item">
              Register
            </Link>
            <Link to="/login" className="navbar-item">
              Log In
            </Link>
            <span onClick={props.handleLogOutUser} className="navbar-item">
              Log Out
            </span>
          </div>
        </div>
      </section>
    </nav>
  );
};

Navbar.propTypes = {
  title: PropTypes.string.isRequired,
  handleLogOutUser: PropTypes.func.isRequired,
};

export default Navbar;
