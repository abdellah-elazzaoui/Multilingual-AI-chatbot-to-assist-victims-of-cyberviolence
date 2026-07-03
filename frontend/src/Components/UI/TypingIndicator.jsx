import React from 'react';

const TypingIndicator = () => {
  return (
    <div className="flex justify-start px-4 py-2">
      <div className="bg-gray-100 rounded-2xl rounded-bl-none p-4 border border-gray-200">
        <div className="flex items-center space-x-1">
          <div className="flex space-x-1">
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
          </div>
          <span className="text-sm text-gray-500 ml-2">AI is thinking...</span>
        </div>
      </div>
    </div>
  );
};

// Alternative: More detailed typing indicator
export const AdvancedTypingIndicator = () => {
  return (
    <div className="flex justify-start px-4 py-2">
      <div className="bg-gray-100 rounded-2xl rounded-bl-none p-4 border border-gray-200 max-w-[200px]">
        <div className="flex items-center justify-between">
          <div className="flex space-x-1">
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse-slow"></div>
            <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse-slow" style={{ animationDelay: '0.2s' }}></div>
            <div className="w-2 h-2 bg-indigo-500 rounded-full animate-pulse-slow" style={{ animationDelay: '0.4s' }}></div>
          </div>
          <div className="text-xs text-gray-500 ml-3">
            Processing your request...
          </div>
        </div>
        <div className="mt-2 w-full bg-gray-200 rounded-full h-1">
          <div className="bg-gradient-to-r from-blue-500 to-purple-500 h-1 rounded-full animate-pulse w-3/4"></div>
        </div>
      </div>
    </div>
  );
};

export default TypingIndicator;