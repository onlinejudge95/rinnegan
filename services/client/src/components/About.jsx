import React from "react";

const About = () => {
  return (
    <div>
      <h1 className="title is-1">Sentimental</h1>
      <hr />
      <br />
      <p className="content">
        With the advent of Machine Learning, the filed of sentiment analysis has
        become somewhat trivial. You can find pre-made solutions to find
        sentiment of a word in a given text. We built upon this functionality
        and made this system.
      </p>
      <p className="content">
        Sentimental is a platform where a user can come and serach for a{" "}
        <strong>sentiment analysis</strong> on a given <strong>keyword</strong>.
        After he has finalized his choice, he will be shown the analysis for
        that word by choosing the corpus from
        <strong>one or more of the social media platorms</strong>. Currently we
        support the following platforms to fetch data from
      </p>
      <div className="list is-hoverable">
        <a className="list-item">Twitter</a>
      </div>
      <p className="content">
        As and when our infrastructure grows we will be using other platforms to
        include more diverse sentiments.
      </p>
    </div>
  );
};

export default About;
