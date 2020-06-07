import React from "react";
import { Link } from "react-router-dom";
import {
  Divider,
  Header,
  Container,
  Card,
  Image,
  Icon,
  Button,
} from "semantic-ui-react";

const ShowUser = () => {
  return (
    <main className="content">
      <Container>
        <div className="ui relaxed divided padded full grid middle aligned">
          <div className="row">
            <div className="column">
              <Header as="h1">Profile</Header>
            </div>
          </div>
          <Divider />
          <div className="row">
            <div className="eight wide column">
              <Card fluid>
                <Image
                  src="https://react.semantic-ui.com/images/avatar/large/matthew.png"
                  wrapped
                  ui={false}
                />
                <Card.Content>
                  <Card.Header>Test Bot</Card.Header>
                  <Card.Meta>
                    <span className="email">Joined in 2020</span>
                  </Card.Meta>
                  <Card.Description>
                    Test Bot is a programmer living in Bengaluru.
                  </Card.Description>
                </Card.Content>
                <Card.Content extra>
                  <Icon name="mail" />
                  onlinejudge95@gmail.com
                </Card.Content>
              </Card>
            </div>
            <div className="eight wide column">
              <Button.Group size="massive">
                <Button
                  as={Link}
                  to="/update"
                  massive
                  positive
                  fluid
                  icon
                  labelPosition="left"
                >
                  Update
                  <Icon name="edit" />
                </Button>
                <Button.Or />
                <Button
                  as={Link}
                  to="/remove"
                  massive
                  negative
                  fluid
                  icon
                  labelPosition="right"
                >
                  Remove
                  <Icon name="user delete" />
                </Button>
              </Button.Group>
            </div>
          </div>
        </div>
      </Container>
    </main>
  );
};

export default ShowUser;
