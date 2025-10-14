import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { User } from "lucide-react";

// ✨ User Message
const UserMessage = ({ message }) => (
  <motion.div
    initial={{ opacity: 0, x: 60 }}
    animate={{ opacity: 1, x: 0 }}
    transition={{ type: "spring", stiffness: 100, damping: 14 }}
    className="flex justify-end mb-5 items-end gap-3"
  >
    <motion.div
      whileHover={{ scale: 1.05 }}
      className="bg-gradient-to-r from-[#234C6A] to-[#1d3f59] text-white px-5 py-3 rounded-3xl rounded-br-md shadow-lg max-w-xs sm:max-w-md text-sm sm:text-base backdrop-blur-md break-words"
    >
      {message}
    </motion.div>
    <div className="w-10 h-10 rounded-full bg-[#234C6A] flex items-center justify-center text-white font-semibold text-lg shadow-md">
      <User size={18} />
    </div>
  </motion.div>
);

// 🤖 Raven (AI) Message
const RavenMessage = ({ text }) => {
  const parts = text?.split(/(\[\d+\])/g) || [];
  return (
    <motion.div
      initial={{ opacity: 0, x: -60 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ type: "spring", stiffness: 100, damping: 14 }}
      className="flex justify-start mb-6 items-start gap-3"
    >
      <div className="w-10 h-10 rounded-full bg-[#234C6A]/10 border border-[#234C6A]/30 text-[#234C6A] flex items-center justify-center font-bold text-lg shadow-inner">
        R
      </div>
      <motion.div
        whileHover={{ scale: 1.02 }}
        className="bg-white text-gray-800 p-4 rounded-3xl rounded-tl-md shadow-md max-w-xs sm:max-w-lg border border-gray-100 text-sm sm:text-base leading-relaxed break-words"
      >
        {parts.map((part, index) =>
          part.match(/^\[\d+\]$/) ? (
            <strong key={index} className="text-[#234C6A] font-semibold cursor-pointer">
              {part} {/* keep brackets */}
            </strong>
          ) : (
            <span
              key={index}
              dangerouslySetInnerHTML={{
                __html: part.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>"),
              }}
            />
          )
        )}
      </motion.div>
    </motion.div>
  );
};

// 📄 Hoverable Citation Button (Improved)
const CitationButton = ({ citation, index }) => {
  const [hovered, setHovered] = useState(false);

  return (
    <div
      className="relative inline-block mr-2 mb-2"
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      {/* Citation Badge */}
      <button className="px-3 py-1 rounded-full bg-[#234C6A]/10 text-[#234C6A] font-semibold text-sm hover:bg-[#234C6A]/20 transition-colors">
        [{index + 1}]
      </button>

      {/* Hover Card */}
      <AnimatePresence>
        {hovered && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="absolute z-50 top-full left-1/2 transform -translate-x-1/2 mt-2 w-72 sm:w-80 p-4 bg-white border border-gray-200 shadow-lg rounded-xl text-sm text-gray-800"
          >
            {/* File Name */}
            <p className="font-semibold text-[#234C6A] mb-1 truncate">
              {citation.filename || "Unknown File"}
            </p>

            {/* Page & Line Info */}
            <div className="text-gray-600 text-xs mb-2">
              <p>Page: {citation.page_number || "-"}</p>
              <p>Lines: {citation.line_range || "-"}</p>
              {citation.page_range && <p>Page Range: {citation.page_range}</p>}
            </div>

            {/* File Link */}
            {citation.file_path && (
              <a
                href={citation.file_path}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:underline break-words"
              >
                View File
              </a>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

// 💬 Main Chat Container
const ChatMessages = ({ userQuery, responseData }) => {
  const synthesis = responseData?.synthesis || {};
  return (
    <div className="space-y-6">
      <UserMessage message={userQuery} />
      <RavenMessage text={synthesis.answer || "Thinking..."} />
      {synthesis.citations && synthesis.citations.length > 0 && (
        <div className="mt-4">
          <h3 className="text-[#234C6A] font-bold mb-2">Citations:</h3>
          <div className="flex flex-wrap">
            {synthesis.citations.map((c, idx) => (
              <CitationButton key={idx} citation={c} index={idx} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatMessages;
