import React from 'react';

const MessageList = ({ messages = [] }) => {
  return (
    <div className="h-full overflow-y-auto space-y-4">
      {messages.map((message) => (
        <div
          key={message.id}
          className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}
        >
          <div
            className={`max-w-[80%] rounded-2xl p-4 shadow-sm ${
              message.isUser
                ? 'bg-blue-500 text-white rounded-br-none'
                : 'bg-gray-100 text-gray-800 rounded-bl-none border border-gray-200'
            }`}
          >
            <div className="text-lr  whitespace-pre-wrap">{message.content}</div>
            <div
              className={`text-xs mt-2 ${
                message.isUser ? 'text-blue-100' : 'text-gray-500'
              }`}
            >
              {message.timestamp instanceof Date 
                ? message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                : new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
              }
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default MessageList;