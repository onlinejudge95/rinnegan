import React from "react";
import ReactDOM from "react-dom";
import axios from "axios";
import UserList from "./components/UserList";
import AddUser from "./components/AddUser";

class App extends React.Component {
  state = { users: [], username: "", email: "", password: "" };

  addUser = (event) => {
    event.preventDefault();
    const headers = {
      Accept: "application/json",
      "Content-Type": "application/json",
    };

    const data = {
      username: this.state.username,
      email: this.state.email,
      password: this.state.password,
    };

    axios
      .post(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`, data, {
        headers,
      })
      .then((response) => {
        console.log(response);
        this.getUsers();
        this.setState({ username: "", email: "", password: "" });
      })
      .catch((err) => console.log(err));
  };

  componentDidMount() {
    this.getUsers();
  }

  getUsers = () => {
    const headers = { Accept: "application/json" };

    axios
      .get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`, { headers })
      .then((response) => {
        this.setState({ users: response.data });
      })
      .catch((err) => {
        console.log(err);
      });
  };

  onHandleChange = (event) => {
    const obj = {};
    obj[event.target.name] = event.target.value;
    this.setState(obj);
  };

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
              <AddUser
                addUser={this.addUser}
                username={this.state.username}
                email={this.state.email}
                password={this.state.password}
                handleChange={this.onHandleChange}
              />
              <br />
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
