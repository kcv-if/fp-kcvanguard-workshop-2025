import { useState } from "react";

export default function Home() {
  const [model, setModel] = useState("styleganv2");
  const [loading, setLoading] = useState(false);
  const [imageUrl, setImageUrl] = useState("");
  const [error, setError] = useState("");

  const generateImage = async () => {
    setLoading(true);
    setImageUrl("");
    setError("");
    
    try {
      const res = await fetch(`https://riciii7-fastapi-batik-gan.hf.space/generate/${model}`);
      if (!res.ok){
        throw new Error(`Failed to fetch image: ${res.status}`);
      }

      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      setImageUrl(url);
    } catch (err) {
      setError("Failed to generate image. Please try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-8 bg-gray-100 space-y-6">
      <h1 className="text-3xl font-bold">StyleGAN Image Generator</h1>

      <select
        value={model}
        onChange={(e) => setModel(e.target.value)}
        className="p-2 rounded border border-gray-300"
      >
        <option value="styleganv2">StyleGANv2</option>
        <option value="stylegan">StyleGAN</option>
        <option value="progan">ProGAN</option>
        <option value="dcgan">DCGAN</option>
        <option value="vanillagan">VanillaGAN</option>
      </select>

      <button
        onClick={generateImage}
        disabled={loading}
        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
      >
        {loading ? "Generating..." : "Generate Image"}
      </button>

      {error && (
        <p className="text-red-600 font-medium">{error}</p>
      )}

      {imageUrl && (
        <img
          src={imageUrl}
          alt="Generated"
          className="mt-4 rounded shadow-lg w-64 h-auto"
        />
      )}
    </main>
  );
}
