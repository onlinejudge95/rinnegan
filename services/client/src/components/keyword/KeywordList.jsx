import React from "react";
import { Redirect, Link } from "react-router-dom";
import { PropTypes } from "prop-types";

const KeywordList = (props) => {
  if (!props.isAuthenticated()) {
    return <Redirect to="/login" />;
  }

  return (
    <div className="ui container">
      <div className="ui relaxed divided padded full grid">
        <div className="row">
          <div className="ui huge header">Keywords</div>
        </div>
        <div className="ui divider" />
        <div className="row">
          <div className="column">
            <div className="row">
              <div className="ui middle aligned green button">Add</div>
            </div>
            <div className="ui middle aligned animated celled list">
              <div className="item">
                <div className="right floated content">
                  <div className="ui red button">
                    <i className="icon trash" />
                  </div>
                </div>
                <i className="icon newspaper big middle aligned" />
                <div className="content">
                  <Link to="/keyword/1">Keyword1</Link>
                </div>
              </div>
              <div className="item">
                <div className="right floated content">
                  <div className="ui red button">
                    <i className="icon trash" />
                  </div>
                </div>
                <i className="icon newspaper big middle aligned" />
                <div className="content">
                  <Link to="/keyword/1">Keyword2</Link>
                </div>
              </div>
              <div className="item">
                <div className="right floated content">
                  <div className="ui red button">
                    <i className="icon trash" />
                  </div>
                </div>
                <i className="icon newspaper big middle aligned" />
                <div className="content">
                  <Link to="/keyword/1">Keyword3</Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

KeywordList.propTypes = {
  isAuthenticated: PropTypes.func.isRequired,
};

export default KeywordList;
