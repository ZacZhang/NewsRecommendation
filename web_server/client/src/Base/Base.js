import React, { PropTypes } from 'react';
import { Link } from 'react-router';
import Auth from '../Auth/Auth';

const Base = ({ children }) => (
    <div>
        <nav className="nav-bar indigo lighten-1">
            <div className="nav-wrapper">
                <a href="/" className="brand-logo">&nbsp;&nbsp;News Recommendation</a>
                <ul id="nav-mobile" className="right">
                    {Auth.isUserAuthenticated() ?
                        (<div>
                            <li>{Auth.getEmail()}</li>
                            <li><Link to="/logout">Log out</Link></li>
                        </div>)
                        :
                        (<div>
                            <li><Link to="/login">Log in</Link></li>
                            <li><Link to="/signup">Sign up</Link></li>
                        </div>)
                    }
                </ul>
            </div>
        </nav>
        <br/>
        {children}
    </div>
);

// parameter children must be passed in
Base.propTypes = {
    children: PropTypes.object.isRequired
};

export default Base;
