import React, { useState, useRef } from "react";
import { motion } from "framer-motion";
import { FaMicrophone, FaPaperPlane, FaImage } from "react-icons/fa";
import axios from "axios";

const ChatInput = ({ onSend }) => {
  const [message, setMessage] = useState("");
  const [listening, setListening] = useState(false);
  const [file, setFile] = useState(null);
  const [language, setLanguage] = useState("en-US");
  const recognitionRef = useRef(null);

  // 🎤 Mic recognition
  const handleMicClick = () => {
    if (!("webkitSpeechRecognition" in window)) {
      alert("Speech recognition not supported in this browser.");
      return;
    }

    if (listening) {
      recognitionRef.current.stop();
      setListening(false);
      return;
    }

    const recognition = new window.webkitSpeechRecognition();
    recognition.lang = language;
    recognition.interimResults = false;
    recognition.continuous = false;

    recognition.onresult = (event) => {
      const text = event.results[0][0].transcript;
      setMessage((prev) => prev + " " + text);
    };

    recognition.onend = () => setListening(false);
    recognition.start();
    recognitionRef.current = recognition;
    setListening(true);
  };

  // 🖼️ File upload
  const handleFileUpload = (e) => {
    const uploadedFile = e.target.files[0];
    if (uploadedFile) {
      setFile(uploadedFile);
    }
  };

  // 📤 Send message
  const handleSend = async () => {
    setMessage("");
    if (!message.trim() && !file) return;

    // Show user message instantly
    onSend?.({ message, responseData: { synthesis: { answer: "Thinking..." } } });

    try {
      let responseData = null;

      if (file) {
        const formData = new FormData();
        formData.append("file", file);

        const uploadRes = await axios.post(
          "http://127.0.0.1:8000/ingest/upload",
          formData,
          { headers: { "Content-Type": "multipart/form-data" } }
        );

        responseData = { synthesis: { answer: "✅ File uploaded successfully!" } };
      } else {
        const res = await axios.post("http://127.0.0.1:8000/query", {
          q: message,
          top_k: 3,
        });

        responseData = res.data?.synthesis ? res.data : { synthesis: res.data };
      }

      // Update parent with AI response
      onSend?.({ message, responseData });
    } catch (error) {
      console.error("❌ Error sending message:", error);
      onSend?.({
        message,
        responseData: { synthesis: { answer: "⚠️ Failed to get response." } },
      });
    } finally {
      setFile(null);
    }
  };

  return (
    <motion.div
      className="p-3 sm:p-4 bg-white border-t border-gray-200 flex items-center justify-between gap-2 sm:gap-3 w-full"
      initial={{ y: 20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ type: "spring", stiffness: 80 }}
    >
      {/* Left Icons */}
      <div className="flex items-center gap-4">
        <div className="relative group">
          <input
            type="file"
            accept="image/*"
            id="file-upload"
            onChange={handleFileUpload}
            className="hidden"
          />
          <label
            htmlFor="file-upload"
            className="w-10 h-10 sm:w-12 sm:h-12 bg-white border border-gray-200 rounded-full flex items-center justify-center shadow-md cursor-pointer hover:shadow-lg transition-all duration-200 group-hover:bg-[#234C6A]/10"
          >
            <FaImage className="text-[#234C6A] text-lg sm:text-xl group-hover:text-[#1d3f59] transition-colors duration-200" />
          </label>
        </div>
      </div>

      {/* Input Field */}
      <div className="relative flex-grow">
        <input
          type="text"
          placeholder="Ask anything or upload a file..."
          className="w-full p-2 sm:p-3 pr-12 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-[#234C6A] text-sm transition-all"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        {file && (
          <div className="absolute right-12 top-1/2 transform -translate-y-1/2 w-2 h-2 bg-[#234C6A] rounded-full animate-pulse"></div>
        )}
      </div>

      {/* Language Selector */}
      <select
        value={language}
        onChange={(e) => setLanguage(e.target.value)}
        className="border border-gray-300 rounded-full p-1 text-sm focus:outline-none focus:ring-2 focus:ring-[#234C6A]"
      >
        <option value="en-US">EN</option>
        <option value="mr-IN">MR</option>
        <option value="hi-IN">Hindi</option>
      </select>

      {/* Right Buttons */}
      <div className="flex items-center gap-2 sm:gap-3">
        <motion.button
          onClick={handleMicClick}
          whileTap={{ scale: 0.9 }}
          className={`w-9 h-9 sm:w-10 sm:h-10 rounded-full flex items-center justify-center transition-colors ${
            listening ? "bg-red-600" : "bg-[#234C6A]"
          } text-white hover:opacity-90`}
        >
          <FaMicrophone />
        </motion.button>

        <motion.button
          onClick={handleSend}
          whileTap={{ scale: 0.9 }}
          className="w-9 h-9 sm:w-10 sm:h-10 bg-[#234C6A] text-white rounded-full flex items-center justify-center font-bold text-lg hover:bg-[#1d3f59] transition-colors"
        >
          <FaPaperPlane />
        </motion.button>
      </div>
    </motion.div>
  );
};

export default ChatInput;
