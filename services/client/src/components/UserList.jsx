import React from "react";
import PropTypes from "prop-types";

const UserList = (props) => {
  return (
    <div>
      {props.users.map((user) => {
        return (
          <p key={user.id} className="box title is-4 username">
            {user.username}
          </p>
        );
      })}
    </div>
  );
};

UserList.propTypes = {
  users: PropTypes.array.isRequired,
};

export default UserList;
