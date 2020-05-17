import React from "react";
import ReactDOM from "react-dom";
import axios from "axios";
import UserList from "./components/UserList";

class App extends React.Component {
  state = { users: [] };

  componentDidMount() {
    this.getUsers();
  }

  getUsers() {
    axios
      .get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`, {
        headers: { Accept: "application/json" },
      })
      .then((res) => {
        this.setState({ users: res.data });
      })
      .catch((err) => {
        console.log(err);
      });
  }

  render() {
    return (
      <section className="section">
        <div className="container">
          <div className="columns">
            <div className="column is-one-third">
              <br />
              <h1 className="title is-1">Sentimental</h1>
              <hr />
              <br />
              <UserList users={this.state.users} />
            </div>
          </div>
        </div>
      </section>
    );
  }
}

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById("root")
);
