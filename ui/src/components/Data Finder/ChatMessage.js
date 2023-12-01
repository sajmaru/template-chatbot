export const ChatMessage = ({ message }) =>
  message.role === "user" ? (
    <div className="flex items-end justify-end">
      <div
        className="bg-gray-100 border-gray-300 border-2 rounded-lg p-2 max-w-lg"
        style={{
          backgroundColor: "#ffc400",
          border: "none",
        }}
      >
        <p>{message.content}</p>
      </div>
    </div>
  ) : (
    <div className="flex items-end">
      <div
        className="bg-gray-100 border-gray-300 border-2 rounded-lg p-2 max-w-lg"
        style={{
          backgroundColor: "#7e5844",
          border: "none",
          color: "white",
        }}
      >
        <p>{message.content}</p>
        {message.img ? (
          <img src={`data:image/png;base64,${message.img}`} alt="chatbot" />
        ) : (
          ""
        )}
      </div>
    </div>
  );
