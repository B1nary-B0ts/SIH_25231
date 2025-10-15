// import React from "react";
// import { motion } from "framer-motion";
// import { FaEye, FaTrash, FaFileAlt } from "react-icons/fa";

// const FileListItem = ({ file, onView, onDelete }) => {
//   const Icon = file.icon || FaFileAlt;
//   return (
//     <motion.div
//       whileHover={{ scale: 1.02, backgroundColor: "#f9fafb" }}
//       whileTap={{ scale: 0.98 }}
//       layout
//       transition={{ type: "spring", stiffness: 250, damping: 18 }}
//       className="flex items-center p-3 sm:p-4 rounded-2xl cursor-pointer border bg-white border-gray-200 shadow-sm hover:shadow-md transition-all"
//     >
//       {/* Left Section */}
//       <div className="flex items-center space-x-3 flex-grow min-w-0">
//         <motion.div
//           initial={{ scale: 0.8, opacity: 0 }}
//           animate={{ scale: 1, opacity: 1 }}
//         >
//           <Icon
//             className={`text-2xl ${
//               file.type === "PDF"
//                 ? "text-red-500"
//                 : file.type === "DOCX"
//                 ? "text-blue-500"
//                 : "text-gray-600"
//             }`}
//           />
//         </motion.div>
//         <div className="flex flex-col min-w-0">
//           <span className="text-sm font-semibold text-gray-800 truncate w-44 sm:w-64">
//             {file.name}
//           </span>
//           <div className="flex items-center gap-2 text-xs text-gray-500">
//             <span>{file.size}</span>
//             <span className="px-2 py-[2px] bg-gray-100 rounded-full text-[10px] font-semibold text-gray-700 uppercase">
//               {file.type}
//             </span>
//           </div>
//         </div>
//       </div>
//       {/* Right Section */}
//       <div className="flex items-center gap-3 flex-shrink-0 ml-2">
//         {/* View */}
//         <motion.button
//           whileHover={{ scale: 1.1 }}
//           onClick={onView}
//           className="text-gray-500 hover:text-[#234C6A] transition-colors"
//         >
//           <FaEye size={18} />
//         </motion.button>
//         {/* Delete */}
//         <motion.button
//           whileHover={{ scale: 1.1 }}
//           onClick={onDelete}
//           className="text-gray-500 hover:text-red-600 transition-colors"
//         >
//           <FaTrash size={18} />
//         </motion.button>
//       </div>
//     </motion.div>
//   );
// };

// const FileList = ({ files = [], setFiles }) => {
//   const handleView = (file) => {
//     if (file.url) {
//       window.open(file.url, "_blank");
//     } else {
//       alert("File preview not available.");
//     }
//   };

//   const handleDelete = (index) => {
//     setFiles((prev) => prev.filter((_, i) => i !== index));
//   };

//   return (
//     <div className="space-y-3 w-[320px] sm:w-[400px] max-w-full">
//       {files.map((file, index) => (
//         <FileListItem
//           key={index}
//           file={file}
//           onView={() => handleView(file)}
//           onDelete={() => handleDelete(index)}
//         />
//       ))}
//     </div>
//   );
// };

// export default FileList;


import React from "react";
import { motion } from "framer-motion";
import { FaEye, FaTrash, FaFileAlt, FaFileAudio, FaFileImage } from "react-icons/fa";

const FileListItem = ({ file, onView, onDelete }) => {
  // 🔍 Determine icon dynamically based on file extension
  const getFileIcon = (filename) => {
    const ext = filename.split(".").pop().toLowerCase();
    if (["png", "jpg", "jpeg"].includes(ext)) return FaFileImage;
    if (ext === "wav") return FaFileAudio;
    if (ext === "pdf") return FaFileAlt;
    if (ext === "docx" || ext === "doc") return FaFileAlt;
    return FaFileAlt;
  };

  const Icon = getFileIcon(file.name || file.filename);

  return (
    <motion.div
      whileHover={{ scale: 1.02, backgroundColor: "#f9fafb" }}
      whileTap={{ scale: 0.98 }}
      layout
      transition={{ type: "spring", stiffness: 250, damping: 18 }}
      className="flex items-center p-3 sm:p-4 rounded-2xl cursor-pointer border bg-white border-gray-200 shadow-sm hover:shadow-md transition-all"
    >
      {/* Left Section */}
      <div className="flex items-center space-x-3 flex-grow min-w-0">
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
        >
          <Icon
            className={`text-2xl ${
              ["png", "jpg", "jpeg"].includes(file.name.split(".").pop().toLowerCase())
                ? "text-green-500"
                : file.name.endsWith(".wav")
                ? "text-purple-500"
                : file.name.endsWith(".pdf")
                ? "text-red-500"
                : file.name.endsWith(".docx") || file.name.endsWith(".doc")
                ? "text-blue-500"
                : "text-gray-600"
            }`}
          />
        </motion.div>

        <div className="flex flex-col min-w-0">
          <span className="text-sm font-semibold text-gray-800 truncate w-44 sm:w-64">
            {file.name}
          </span>
          <div className="flex items-center gap-2 text-xs text-gray-500">
            <span>{file.size}</span>
            <span className="px-2 py-[2px] bg-gray-100 rounded-full text-[10px] font-semibold text-gray-700 uppercase">
              {file.type || file.name.split(".").pop().toUpperCase()}
            </span>
          </div>
        </div>
      </div>

      {/* Right Section */}
      <div className="flex items-center gap-3 flex-shrink-0 ml-2">
        {/* View */}
        <motion.button
          whileHover={{ scale: 1.1 }}
          onClick={onView}
          className="text-gray-500 hover:text-[#234C6A] transition-colors"
        >
          <FaEye size={18} />
        </motion.button>

        {/* Delete */}
        <motion.button
          whileHover={{ scale: 1.1 }}
          onClick={onDelete}
          className="text-gray-500 hover:text-red-600 transition-colors"
        >
          <FaTrash size={18} />
        </motion.button>
      </div>
    </motion.div>
  );
};

const FileList = ({ files = [], setFiles }) => {
  const handleView = (file) => {
    if (file.url) {
      window.open(file.url, "_blank");
    } else {
      alert("File preview not available.");
    }
  };

  const handleDelete = (index) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  };

  return (
    <div className="space-y-3 w-[320px] sm:w-[400px] max-w-full">
      {files.map((file, index) => (
        <FileListItem
          key={index}
          file={file}
          onView={() => handleView(file)}
          onDelete={() => handleDelete(index)}
        />
      ))}
    </div>
  );
};

export default FileList;
