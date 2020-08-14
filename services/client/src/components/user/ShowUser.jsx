import React from "react";
import { Redirect, Link } from "react-router-dom";
import { PropTypes } from "prop-types";

const ShowUser = (props) => {
  if (!props.isAuthenticated()) {
    return <Redirect to="/login" />;
  }

  return (
    <div className="ui container">
      <div className="ui relaxed divided padded full grid container">
        <div className="row">
          <div className="ui huge header">Profile</div>
        </div>
        <div className="ui divider" />
        <div className="row">
          <div className="ui card fluid">
            <div className="image">
              <img
                src="https://react.semantic-ui.com/images/avatar/large/matthew.png"
                alt={props.user.username}
              />
            </div>
            <div className="content">
              <div className="header">{props.user.username}</div>
              <div className="meta">
                <span className="date">Joined in 2020</span>
              </div>
              <div className="description">
                Test Bot is a programmer living in Bengaluru.
              </div>
            </div>
            <div className="extra content">
              <i className="mail" />
              {props.user.email}
            </div>
          </div>
          <div className="ui large two buttons">
            <Link
              to="/update"
              className="ui labeled button massive positive icon"
            >
              <i className="edit" />
              Edit
            </Link>
            <div className="or" />
            <button
              className="ui right labeled button massive negative icon"
              onClick={props.handleRemoveUserClick}
            >
              <i className="user delete" />
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

ShowUser.propTypes = {
  user: PropTypes.object,
  handleRemoveUserClick: PropTypes.func.isRequired,
  isAuthenticated: PropTypes.func.isRequired,
};

export default ShowUser;
