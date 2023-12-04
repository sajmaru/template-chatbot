import * as React from 'react';
import { useState, useMemo, useEffect, useRef } from "react";
import { useChat } from "./use-chat";
import { ChatMessage } from "./ChatMessage";
import { appConfig } from "../../config.browser";
import { Welcome } from "../Welcome";
import './DataFinder.css';
import Button from '@mui/material/Button';
import Backdrop from '@mui/material/Backdrop';
import CircularProgress from '@mui/material/CircularProgress';
import Snackbar from '@mui/material/Snackbar';
import Alert from '@mui/material/Alert';

import { useGoogleOneTapLogin, GoogleLogin } from '@react-oauth/google';


function DataFinder() {
    const { currentChat, chatHistory, sendMessage, state, clear } = useChat();
    const [message, setMessage] = useState("");
    const [open, setOpen] = React.useState(false);
    const [authToken] = useState(localStorage.getItem("AUTH_TOKEN"));
    const [alert, setAlert] = React.useState(authToken == null ? true : false);

    if (!authToken) {
        useGoogleOneTapLogin({
            onSuccess: credentialResponse => {
                localStorage.setItem("AUTH_TOKEN", credentialResponse.credential);
                setOpen(false);
                setAlert(false);
            },
            onError: () => {
                console.log('Login Failed');
                setOpen(false);
            },
            cancel_on_tap_outside: false
        });
    }

    const currentMessage = useMemo(() => {
        return { content: currentChat ?? "", role: "assistant" };
    }, [currentChat]);

    const bottomRef = useRef(null);

    useEffect(() => {
        scrollToBottom();
    }, [currentChat, chatHistory, state]);

    const scrollToBottom = () => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    const inputRef = useRef(null);
    const focusInput = () => {
        inputRef.current?.focus();
    };

    useEffect(() => {
        focusInput();
    }, [state]);

    return (
        <main className="bg-white p-6 w-full h-full flex flex-col">
            <div style={{ flexGrow: 1, float: 'right', display: 'contents' }}>
                <GoogleLogin
                    onSuccess={credentialResponse => {
                        localStorage.setItem("AUTH_TOKEN", credentialResponse.credential);
                        setOpen(false);
                        setAlert(false);
                    }}
                    onError={() => {
                        console.log('Login Failed');
                        setOpen(false);
                    }}
                    width='200'
                />
            </div>
            <section className="overflow-y-auto flex-grow mb-4 pb-8">
                <div className="flex flex-col space-y-4">
                    <Welcome title=" 🔍Data Finder" text="DataFinder is an application leveraging Language Model technology to efficiently search and identify relevant tables from the datawarehouse, enabling users to easily locate and access the desired data for their projects." />
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {appConfig.dataFinderSamplePhrases.map((phrase) => (
                            <button
                                key={phrase}
                                onClick={() => sendMessage(phrase, chatHistory)}
                                className="bg-gray-100 border-gray-300 border-2 rounded-lg p-4"
                            >
                                {phrase}
                            </button>
                        ))}
                    </div>
                    {chatHistory.map((chat, i) => (
                        <ChatMessage key={i} message={chat} />
                    ))}


                    {currentChat ? <ChatMessage message={currentMessage} /> : null}
                </div>

                <div ref={bottomRef} />
            </section>
            <div className="flex items-center justify-center h-20">
                {state === "idle" ? null : (
                    <div
                        className="bg-gray-100 text-gray-900 py-2 px-4 my-8"
                    >
                        Typing...
                    </div>
                )}
            </div>
            <section className="bg-gray-100 rounded-lg p-1">
                <form
                    style={{

                    }}
                    className="flex"
                    onSubmit={(e) => {
                        e.preventDefault();
                        sendMessage(message, chatHistory);
                        setMessage("");
                    }}
                >
                    {chatHistory.length > 1 ? (
                        <button
                            className="bg-gray-100 text-gray-600 py-2 px-4 rounded-l-lg"
                            type="button"
                            onClick={(e) => {
                                e.preventDefault();
                                clear();
                                setMessage("");
                            }}
                        >
                            Clear
                        </button>
                    ) : null}
                    <input
                        type="text"
                        ref={inputRef}
                        className="w-full rounded-l-lg p-2 outline-none"
                        placeholder={state === "idle" ? "Type your message..." : "..."}
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        disabled={state !== "idle"}
                    />
                    {state === "idle" ? (
                        <Button type="submit" className="send-button" variant="contained">
                            Send
                        </Button>
                    ) : null}
                </form>
            </section>

            <Backdrop
                sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
                open={open}
            >
                <CircularProgress color="inherit" />
            </Backdrop>
            <Snackbar
                sx={{ width: '15%' }}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
                open={alert}
            >
                <Alert severity="error" sx={{ width: '100%' }} variant="filled" >
                    Please Sign In!
                </Alert>
            </Snackbar>
        </main>
    );
}

export default DataFinder;
