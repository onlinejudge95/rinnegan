import React from "react";
import PropTypes from "prop-types";

const UserList = (props) => {
  return (
    <div>
      <table className="table is-hoverable is-fullwidth">
        <thead>
          <tr>
            <th>Email</th>
            <th>Username</th>
            <th />
          </tr>
        </thead>
        <tbody>
          {props.users.map((user) => {
            return (
              <tr key={user.email}>
                <td>{user.email}</td>
                <td className="username">{user.username}</td>
                {props.isAuthenticated() && (
                  <td>
                    <button
                      className="button is-danger is-small"
                      onClick={() => props.removeUser(user.id)}
                    >
                      Delete
                    </button>
                  </td>
                )}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

UserList.propTypes = {
  users: PropTypes.array.isRequired,
  removeUser: PropTypes.func.isRequired,
  isAuthenticated: PropTypes.func.isRequired,
};

export default UserList;
