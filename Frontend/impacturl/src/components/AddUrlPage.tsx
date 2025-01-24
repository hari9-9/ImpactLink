import { useState } from "react";
import { useNavigate } from "react-router-dom";

const AddURLPage = () => {
  const [productName, setProductName] = useState("");
  const [productUrl, setProductUrl] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Retrieve access token from local storage (stored after login)
    const accessToken = localStorage.getItem("accessToken");

    if (!accessToken) {
      alert("Authentication required. Please log in.");
      navigate("/login");
      return;
    }

    const requestData = {
      product_url: productUrl,
      product_name: productName,
    };

    try {
      const response = await fetch("http://127.0.0.1:8000/linker/shorten/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`, // Include access token in request
        },
        body: JSON.stringify(requestData),
      });

      if (response.ok) {
        alert("URL successfully shortened!");
        navigate("/dashboard"); // Redirect to dashboard on success
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.message || "Failed to shorten URL"}`);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Something went wrong. Please try again.");
    }
  };

  return (
    <div className="p-6 max-w-md mx-auto bg-white rounded-xl shadow-md space-y-4">
      <h2 className="text-xl font-bold">Add New URL</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-gray-700">Product Name</label>
          <input
            type="text"
            value={productName}
            onChange={(e) => setProductName(e.target.value)}
            className="mt-1 block w-full border rounded-md p-2"
            required
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700">Product URL</label>
          <input
            type="url"
            value={productUrl}
            onChange={(e) => setProductUrl(e.target.value)}
            className="mt-1 block w-full border rounded-md p-2"
            required
          />
        </div>
        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-700"
        >
          Submit
        </button>
      </form>
    </div>
  );
};

export default AddURLPage;
