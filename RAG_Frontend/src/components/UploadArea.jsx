import React, { useRef, useState } from "react";
import { motion } from "framer-motion";
import { FaCloudUploadAlt } from "react-icons/fa";
import axios from "axios";

const UploadArea = ({ onFileUpload }) => {
  const fileInputRef = useRef(null);
  const [fileName, setFileName] = useState(null);
  const [uploading, setUploading] = useState(false);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setFileName(file.name);
    setUploading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await axios.post("http://localhost:8000/ingest/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      if (res.data) {
        // Return backend response to Sidebar for adding to list
        if (onFileUpload) onFileUpload({
          ...res.data,
          fileObj: file,
        });
      }
    } catch (err) {
      console.error("Upload failed:", err);
      alert("Upload failed. Check console for details.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <motion.div
      className="p-6 border-t border-gray-200 bg-white rounded-2xl shadow-inner"
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="flex flex-col items-center text-center space-y-3">
        <motion.div
          whileHover={{ scale: 1.1, rotate: 5 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => fileInputRef.current.click()}
          className="relative w-16 h-16 bg-[#234C6A]/10 rounded-full flex items-center justify-center cursor-pointer shadow-md hover:shadow-lg transition-all"
        >
          <FaCloudUploadAlt className="text-[#234C6A] text-3xl" />
        </motion.div>

        <input
          type="file"
          ref={fileInputRef}
          onChange={handleUpload}
          className="hidden"
        />

        <button
          onClick={() => fileInputRef.current.click()}
          className="px-5 py-2 text-sm font-semibold text-white bg-[#234C6A] rounded-full shadow-md hover:bg-[#1d3f59] hover:shadow-lg transition-all"
        >
          {uploading ? "Uploading..." : "Choose File"}
        </button>

        {fileName && (
          <motion.p
            initial={{ opacity: 0, y: 5 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="text-xs text-gray-600 font-medium mt-1 truncate max-w-[180px]"
          >
            {fileName}
          </motion.p>
        )}
      </div>
    </motion.div>
  );
};

export default UploadArea;
