import React from "react";
import { Helmet } from "react-helmet";
import Navigation from "./Navigation";
import Footer from "./Footer";
import "./Base.scss";

const Base: React.FC<React.PropsWithChildren<{}>> = ({ children }) => {
  return (
    <>
      <Helmet>
        {/* TODO Temporary */}
        <meta name="robots" content="noindex" />
      </Helmet>

      <Navigation />
      <main role="main" className="container my-4">
        {children}
      </main>
      <Footer />
    </>
  );
};

export default Base;
