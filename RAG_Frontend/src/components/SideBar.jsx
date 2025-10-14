import React, { useState } from "react";
import { motion } from "framer-motion";
import FileList from "./FileList";
import UploadArea from "./UploadArea";
import { FaBook, FaFilePdf, FaFileWord, FaFileAlt } from "react-icons/fa";

const Sidebar = () => {
  const [files, setFiles] = useState([]);

  const handleFileUpload = (backendFile) => {
    // Determine icon based on file type
    let icon = FaFileAlt;
    let type = "FILE";

    const name = backendFile.filename || backendFile.fileObj?.name || "Unknown";

    const lowerName = name.toLowerCase();
    if (lowerName.endsWith(".pdf")) {
      icon = FaFilePdf;
      type = "PDF";
    } else if (lowerName.endsWith(".docx") || lowerName.endsWith(".doc")) {
      icon = FaFileWord;
      type = "DOCX";
    }

    setFiles((prev) => [
      ...prev,
      {
        name,
        size: backendFile.fileObj
          ? `${(backendFile.fileObj.size / 1024).toFixed(1)} KB`
          : "Unknown",
        type,
        icon,
        doc_id: backendFile.doc_id,
        url: backendFile.filename
          ? `http://localhost:8000/storage/${backendFile.filename}`
          : null,
        fileObj: backendFile.fileObj || null,
      },
    ]);
  };

  return (
    <motion.div
      className="w-[340px] sm:w-[420px] max-w-full bg-white/90 backdrop-blur-md border-r border-gray-200 shadow-lg flex flex-col justify-between overflow-y-auto overflow-x-hidden"
      initial={{ x: -100, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ type: "spring", stiffness: 70, damping: 12 }}
    >
      <div className="p-6">
        <motion.div
          className="flex items-center gap-3 mb-6"
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <img
            src="/logo_1.png"
            alt="RAVEN Logo"
            className="w-10 h-10 sm:w-12 sm:h-12 rounded-full object-cover shadow-lg border-2 border-gray-800 hover:scale-105 transition-transform duration-200"
          />
          <h1 className="text-2xl font-bold text-[#234C6A] tracking-wide">RAVEN</h1>
        </motion.div>

        <h3 className="text-sm font-semibold text-gray-500 mb-3 uppercase tracking-wide flex items-center gap-2">
          <FaBook className="text-[#234C6A] w-4 h-4 sm:w-5 sm:h-5" />
          Knowledge Base
        </h3>

        <FileList files={files} setFiles={setFiles} />
      </div>

      <UploadArea onFileUpload={handleFileUpload} />
    </motion.div>
  );
};

export default Sidebar;
