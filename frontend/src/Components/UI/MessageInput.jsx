import React, { useState } from 'react';
import { Send, Paperclip, Mic } from 'lucide-react';

const MessageInput = ({ onSendMessage }) => {
  const [inputMessage, setInputMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputMessage.trim()) {
      onSendMessage(inputMessage);
      setInputMessage('');
    }
  };

  

  return (
    <div className="space-y-3">
      
      

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="flex gap-2">
        <div className="flex-1 relative">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type your message here..."
            className="w-full pl-4 pr-12 py-3 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <div className="absolute right-2 top-1/2 transform -translate-y-1/2 flex gap-1">
            <button
              type="button"
              className="p-1.5 text-gray-400 hover:text-gray-600 transition-colors"
            >
              <Paperclip size={18} />
              
            </button>

            <button
              type="button"
              className="p-1.5 text-gray-400 hover:text-gray-600 transition-colors"
            >
              <Mic size={18} />
            </button>
          </div>
        </div>
        
        <button
          type="submit"
          disabled={!inputMessage.trim()}
          className="px-6 py-3 bg-gradient-to-r from-blue-800 to-blue-500 text-white rounded-full hover:from-blue-600 hover:to-purple-600 disabled:from-gray-300 disabled:to-gray-300 disabled:cursor-not-allowed transition-all flex items-center gap-2"
        >
          <Send size={18} />
          <span className="hidden sm:inline">Send</span>
        </button>
      </form>
      
      {/* Helper Text */}
      <p className="text-center text-xs text-gray-500">
        
      </p>
    </div>
  );
};

export default MessageInput;