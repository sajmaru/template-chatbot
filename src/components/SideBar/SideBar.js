import './SideBar.css';
import React from 'react';
import { ReactComponent as UPSLogo } from '../../ups-logo.svg';
import { Outlet, NavLink } from "react-router-dom";

export default function SideBar() {
    return (
        <>
            <div id="sidebar">
                <div>
                    <UPSLogo style={{
                        marginTop: '30px',
                        marginBottom: '30px',
                        display: 'block',
                        marginLeft: '40%',
                        marginRight: 'auto',
                        width: '50%'
                    }} />
                </div>
                <nav>
                    <ul>
                        <li>
                            <NavLink
                                to={`/template-chatbot`}
                                className={({ isActive, isPending }) =>
                                    isActive
                                        ? "active"
                                        : isPending
                                            ? "pending"
                                            : ""
                                }
                            >
                                Template Chatbot
                            </NavLink>
                        </li>
                    </ul>
                </nav>
            </div>
            <div id="detail">
                <Outlet />
            </div>
        </>
    );
}