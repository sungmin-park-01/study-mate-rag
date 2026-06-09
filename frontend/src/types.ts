export type UploadResponse = {
  document_id: string;
  filename: string;
  status: string;
  stored_chunk_count: number;
};

export type SourcePreview = {
  filename: string;
  page_number: number;
  content_preview: string;
};

export type AskResponse = {
  answer: string;
  sources: SourcePreview[];
  latency_ms: number;
};