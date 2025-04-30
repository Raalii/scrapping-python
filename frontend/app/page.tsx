/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { useState } from "react";

export default function Home() {
  const [url, setUrl] = useState("");
  const [data, setData] = useState<{
    summary: string;
    keywords: string[];
  } | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setLoading(true);
    setData(null);
    const res = await fetch(
      process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000" + "/summarize",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      }
    );
    const d = await res.json();
    setData(d);
    setLoading(false);
  };

  return (
    <main className="max-w-2xl mx-auto p-8">
      <h1 className="text-2xl font-bold mb-4">Résumé d&apos;article par LLM</h1>
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://..."
          className="border p-2 flex-1"
        />
        <button className="bg-black text-white px-4 py-2 rounded">
          {loading ? "..." : "Go"}
        </button>
      </form>
      {data && (
        <section className="mt-6">
          <h2 className="text-xl font-semibold mb-2">Résumé</h2>
          <p className="whitespace-pre-line">{data.summary}</p>
          {data.keywords?.length && (
            <>
              <h3 className="font-medium mt-4">Mots-clés</h3>
              <ul className="list-disc ml-6">
                {data.keywords.map((k, i) => (
                  <li key={i}>{k}</li>
                ))}
              </ul>
            </>
          )}
        </section>
      )}
    </main>
  );
}
