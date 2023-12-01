import { useState, useMemo } from "react";
import BASE_URL from "../../constants"

export function useChat() {
    const [currentChat, setCurrentChat] = useState(null);
    const [chatHistory, setChatHistory] = useState([]);
    const [state, setState] = useState("idle");
    const [newChat, setNewChat] = useState("true");

    const abortController = useMemo(() => new AbortController(), []);
    // const API_URL = BASE_URL + "data_finder/";
    const API_URL = BASE_URL + "data_finder/";
    console.log(BASE_URL);
    
    function cancel() {
        setState("idle");
        abortController.abort();
        if (currentChat) {
            const newHistory = [
                ...chatHistory,
                { role: "user", content: currentChat },
            ];

            setChatHistory(newHistory);
            setCurrentChat("");
        }
    }

    function clear() {
        setNewChat("true");
        setChatHistory([]);
    }

    const sendMessage = async (message, chatHistory) => {
        setState("waiting");
        const newHistory = [...chatHistory, { role: "user", content: message }];

        setChatHistory(newHistory);
        fetch(API_URL, {
            method: "post",
            headers: {
                "Content-Type": "application/json",
                Authorization:
                    "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjY3NmRhOWQzMTJjMzlhNDI5OTMyZjU0M2U2YzFiNmU2NTEyZTQ5ODMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiNjE4MTA0NzA4MDU0LTlyOXMxYzRhbGczNmVybGl1Y2hvOXQ1Mm4zMm42ZGdxLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiNjE4MTA0NzA4MDU0LTlyOXMxYzRhbGczNmVybGl1Y2hvOXQ1Mm4zMm42ZGdxLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTEwOTM2MzI5NzE4MjgyMDUwMTI4IiwiaGQiOiJ1cHMuY29tIiwiZW1haWwiOiJzYWpiaGF2ZXNobWFydUB1cHMuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF0X2hhc2giOiJ0VUFyY1U2M2F3SWY1UHV6SGkta3ZBIiwibmJmIjoxNjg5NzA0MDA3LCJpYXQiOjE2ODk3MDQzMDcsImV4cCI6MTY4OTcwNzkwNywianRpIjoiOGU0NWI1MWNjN2Y5ZTM5Zjc3OWI4MjQzNzhkMzdjMzk2ZTM1MGRmZCJ9.Dv0RpELlYzlIW3wcAzRaSQJMVTHyyC_iOgoENYqJBnfAFdwMwnzlWVjKMfSSeYSL6qhfwha0EcRN65qAgPDVLgP8wL8u4q3vcVzb0m5jb8BQJaZ-OHWBCgVVWRLU_UZqWG0puZP2ZCWd4QR4AIkqxwaCLH-if5igss2YcdkmMnJnPydH5nxslqbmthc3AImhPxuskTIn5pYMkKdAQ--1xa0H9o6jQCsO5NuhZeJU0mUlzaAB99oWFV5z8rV74TmsYOIzy_A2LMNuB2_WVtGypl2OGF_QfxxR4LwheHt7KB-688Ji6p6X6Ri35Do8OxQ_v5ssyZa3EK-kovAhCOIPnQ",
            },
            // referrerPolicy: 'no-referrer-when-downgrade',
            body: JSON.stringify({
                question: message,
                new_chat: newChat,
            }),
        })
            .then((response) => response.json())
            .then((data) => {
                setChatHistory((curr) => [
                    ...curr,
                    { role: "assistant", content: data.data },
                ]);
                setNewChat("false");
                setCurrentChat(null);
                setState("idle");
            })
            .catch((error) => {
                console.log(error);
            });
    };

    return { sendMessage, currentChat, chatHistory, cancel, clear, state };
}
