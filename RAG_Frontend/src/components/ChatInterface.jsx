// import React, { useRef, useEffect, useState } from "react";
// import ChatInput from "./ChatInput";
// import ChatMessages from "./ChatMessages";
// import { MdOutlineMoreVert, MdLogout } from "react-icons/md";
// import { motion } from "framer-motion";

// const ChatInterface = () => {
//   const messagesEndRef = useRef(null);
//   const [messages, setMessages] = useState([]);
//   const username = "NTRO";

//   useEffect(() => {
//     messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
//   }, [messages]);

//   const handleLogout = () => console.log("Logout clicked");

//   return (
//     <div className="flex flex-col flex-grow h-full bg-gray-50 rounded-xl shadow-inner overflow-hidden">
//       {/* Header */}
//       <motion.div
//         initial={{ y: -30, opacity: 0 }}
//         animate={{ y: 0, opacity: 1 }}
//         transition={{ type: "spring", stiffness: 90, damping: 15 }}
//         className="flex justify-between items-center bg-white p-4 border-b border-gray-200 shadow-md"
//       >
//         <h2 className="text-lg sm:text-xl font-semibold text-[#234C6A] flex items-center gap-2">
//           💬 Raven Chat
//         </h2>

//         <div className="flex items-center gap-4">
//           <div className="flex flex-col items-end">
//             <span className="text-sm sm:text-base font-medium text-gray-700">{username}</span>
//             <span className="text-xs text-gray-400">Online</span>
//           </div>

//           <motion.div
//             whileHover={{ scale: 1.1 }}
//             className="w-9 h-9 sm:w-10 sm:h-10 rounded-full flex items-center justify-center bg-[#234C6A]/10 cursor-pointer shadow-inner overflow-hidden"
//           >
//             <img src="ntro.jpeg" alt="User Avatar" className="w-full h-full object-cover" />
//           </motion.div>

//           <motion.button
//             whileHover={{ scale: 1.05 }}
//             onClick={handleLogout}
//             className="flex items-center gap-1 bg-[#234C6A] text-white text-sm sm:text-base font-semibold px-3 py-1.5 rounded-full shadow-md hover:bg-[#1d3f59]"
//           >
//             <MdLogout size={18} />
//             Logout
//           </motion.button>

//           <MdOutlineMoreVert className="text-2xl text-gray-400 cursor-pointer hover:text-gray-600" />
//         </div>
//       </motion.div>

//       {/* Messages */}
//       <div className="flex-grow overflow-y-auto p-5 space-y-4 scrollbar-thin scrollbar-thumb-[#234C6A]/40 scrollbar-track-gray-100">
//         <div className="space-y-6">
//           {messages.map((msg, idx) => (
//             <ChatMessages key={idx} userQuery={msg.message} responseData={msg.responseData} />
//           ))}
//         </div>
//         <div ref={messagesEndRef} />
//       </div>

//       {/* Input */}
//       <motion.div
//         initial={{ y: 30, opacity: 0 }}
//         animate={{ y: 0, opacity: 1 }}
//         transition={{ type: "spring", stiffness: 80 }}
//         className="bg-white p-4 border-t border-gray-200 shadow-inner"
//       >
//         <ChatInput
//           onSend={({ message, responseData }) =>
//             setMessages((prev) => [...prev, { message, responseData }])
//           }
//         />
//       </motion.div>
//     </div>
//   );
// };

// export default ChatInterface;


import React, { useRef, useEffect, useState } from "react";
import ChatInput from "./ChatInput";
import ChatMessages from "./ChatMessages";
import { MdOutlineMoreVert, MdLogout } from "react-icons/md";
import { motion } from "framer-motion";

const ChatInterface = () => {
  const messagesEndRef = useRef(null);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const username = "NTRO";

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleLogout = () => console.log("Logout clicked");

  const handleSend = async ({ message, responseData }) => {
    setLoading(true); // show loader while waiting
    setMessages((prev) => [...prev, { message, responseData: null }]);

    try {
      const res = await fetch("http://127.0.0.1:8000/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ q: message, top_k: 3 }),
      });
      const data = await res.json();

      setMessages((prev) =>
        prev.map((m, i) =>
          i === prev.length - 1 ? { ...m, responseData: data } : m
        )
      );
    } catch (error) {
      console.error("Error fetching:", error);
    } finally {
      setLoading(false); // remove loader after response
    }
  };

  return (
    <div className="relative flex flex-col flex-grow h-full bg-gray-50 rounded-xl shadow-inner overflow-hidden">
      {/* Header */}
      <motion.div
        initial={{ y: -30, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ type: "spring", stiffness: 90, damping: 15 }}
        className="flex justify-between items-center bg-white p-4 border-b border-gray-200 shadow-md"
      >
        <h2 className="text-lg sm:text-xl font-semibold text-[#234C6A] flex items-center gap-2">
          💬 Raven Chat
        </h2>

        <div className="flex items-center gap-4">
          <div className="flex flex-col items-end">
            <span className="text-sm sm:text-base font-medium text-gray-700">{username}</span>
            <span className="text-xs text-gray-400">Online</span>
          </div>

          <motion.div
            whileHover={{ scale: 1.1 }}
            className="w-9 h-9 sm:w-10 sm:h-10 rounded-full flex items-center justify-center bg-[#234C6A]/10 cursor-pointer shadow-inner overflow-hidden"
          >
            <img src="ntro.jpeg" alt="User Avatar" className="w-full h-full object-cover" />
          </motion.div>

          <motion.button
            whileHover={{ scale: 1.05 }}
            onClick={handleLogout}
            className="flex items-center gap-1 bg-[#234C6A] text-white text-sm sm:text-base font-semibold px-3 py-1.5 rounded-full shadow-md hover:bg-[#1d3f59]"
          >
            <MdLogout size={18} />
            Logout
          </motion.button>

          <MdOutlineMoreVert className="text-2xl text-gray-400 cursor-pointer hover:text-gray-600" />
        </div>
      </motion.div>

      {/* Messages */}
      <div
        className={`flex-grow overflow-y-auto p-5 space-y-4 scrollbar-thin scrollbar-thumb-[#234C6A]/40 scrollbar-track-gray-100 transition-all duration-300 ${
          loading ? "blur-sm bg-gray-200/40" : ""
        }`}
      >
        <div className="space-y-6">
          {messages.map(
            (msg, idx) =>
              msg.responseData && (
                <ChatMessages key={idx} userQuery={msg.message} responseData={msg.responseData} />
              )
          )}
        </div>
        <div ref={messagesEndRef} />
      </div>

      {/* Loader Overlay */}
      {loading && (
        <div className="absolute inset-0 flex flex-col justify-center items-center bg-gray-100/80 backdrop-blur-md z-10">
          <img src="/raven.gif" alt="Loading..." className="w-28 h-28 object-contain mb-2" />
          <p className="text-gray-600 font-medium text-sm sm:text-base">
            the raven is fetching your answers...
          </p>
        </div>
      )}

      {/* Input */}
      <motion.div
        initial={{ y: 30, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ type: "spring", stiffness: 80 }}
        className="bg-white p-4 border-t border-gray-200 shadow-inner"
      >
        <ChatInput onSend={handleSend} />
      </motion.div>
    </div>
  );
};

export default ChatInterface;