export const Welcome = (props) => (
    <div className="bg-white rounded-lg px-8 py-5 mr-20 w-full" style={{
        border: '1px solid #ffc400'
    }}>
        <h1 className="text-2xl font-bold mb-2">{props.title}</h1>
        <p>
            {props.text}
        </p>
    </div>
);
