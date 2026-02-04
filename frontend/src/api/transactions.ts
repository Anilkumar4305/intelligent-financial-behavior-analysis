import axios from "axios";

export const uploadTransactionsCSV = (file: File) => {
  const formData = new FormData();
  formData.append("file", file);

  return axios.post("http://localhost:8000/transactions/upload-csv", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};
