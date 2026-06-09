import type { AskResponse, UploadResponse } from "../types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function uploadDocument(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/documents/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to upload the document.");
  }

  return response.json();
}

export async function askQuestion(
  documentId: string,
  question: string,
  topK: number = 3
): Promise<AskResponse> {
  const response = await fetch(`${API_BASE_URL}/query/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      document_id: documentId,
      question,
      top_k: topK,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to get an answer from the document.");
  }

  return response.json();
}