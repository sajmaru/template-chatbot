import { useState, useMemo } from "react";
import BASE_URL from "../../constants"

export function useChat() {
    const [currentChat, setCurrentChat] = useState(null);
    const [chatHistory, setChatHistory] = useState([]);
    const [state, setState] = useState("idle");
    const [newChat, setNewChat] = useState("true");

    const abortController = useMemo(() => new AbortController(), []);
    // const API_URL = BASE_URL + "data_finder/";
    const API_URL = BASE_URL + "template-chatbot-api/";
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
                "Authorization": `Bearer ${localStorage.getItem("AUTH_TOKEN")}`

            },
            // referrerPolicy: 'no-referrer-when-downgrade',
            body: JSON.stringify({
                question: message,
                new_chat: newChat,
            }),
        })
        .then(async (response) => {
            // Check for HTTP response status
            if (response.status === 200) {
                // Parse the JSON response and proceed with the existing logic
                let data = await response.json();
                setChatHistory((curr) => [
                    ...curr,
                    { role: "assistant", content: data.data },
                ]);
                setNewChat("false");
                setCurrentChat(null);
                setState("idle");
            } else if (response.status === 401) {
                // Handle the 401 Unauthorized case
                localStorage.removeItem("AUTH_TOKEN");
                window.location.reload(false);
            } else {
                // Handle other HTTP status codes if necessary
                throw new Error(`HTTP error: Status code ${response.status}`);
            }
        })
        .catch((error) => {
            // Handle any errors that occurred during the fetch or the processing
            console.log(error);
            window.alert(`${error.message} An error occurred`);
        });
        
    };

    return { sendMessage, currentChat, chatHistory, cancel, clear, state };
}
