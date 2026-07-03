import React, { useState, useRef, useEffect } from 'react';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import TypingIndicator from './TypingIndicator';
import { chatAPI } from '../../api';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef();

  useEffect(() => {
    setMessages([{
      id: 1,
      content: "Bonjour! Je suis votre assistant IA. Comment puis-je vous aider aujourd'hui ?",
      isUser: false,
      timestamp: new Date()
    }]);
  }, []);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSendMessage = async (message) => {
    if (!message.trim()) return;
    
    const user_message = {
      id: Date.now(),
      content: message,
      isUser: true,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, user_message]);
    setIsTyping(true);

    try {
      const response = await chatAPI.sendMessage(message);
      console.log('Backend response:', response.data); // Debug log
      
      // FIX: Use data.response instead of data.ai_response
      const ai_response = {
        id: Date.now() + 1,
        content: response.data.response, 
        isUser: false,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, ai_response]);

    } catch (err) {
      console.log('Error:', err);
      const errorMessage = {
        id: Date.now() + 1,
        content: ` Error: ${err.response?.data?.error || err.message || 'Failed to connect to backend'}`,
        isUser: false,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl h-[600px] bg-white rounded-2xl shadow-xl flex flex-col">
        {/* Header */}
        <div className="bg-gradient-to-tr from-blue-800 to-blue-400 text-white p-6 rounded-t-2xl">
          <h1 className="text-2xl font-bold">Assistance aux victimes de cyberviolencest</h1>
          <p className="text-blue-100">Developed by Abdellah Elazzaoui</p>
        </div>
        
        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-4">
          <MessageList messages={messages} />
          {isTyping && <TypingIndicator />}
          <div ref={messagesEndRef} />
        </div>
        
        {/* Input Area */}
        <div className="border-t border-gray-200 p-4">
          <MessageInput onSendMessage={handleSendMessage} disabled={isTyping} />
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;