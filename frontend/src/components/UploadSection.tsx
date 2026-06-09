import type { UploadResponse } from "../types";

type UploadSectionProps = {
  isUploading: boolean;
  uploadedDocument: UploadResponse | null;
  onUpload: (file: File) => void;
};

export function UploadSection({
  isUploading,
  uploadedDocument,
  onUpload,
}: UploadSectionProps) {
  function handleFileChange(event: React.ChangeEvent<HTMLInputElement>) {
    const selectedFile = event.target.files?.[0];

    if (!selectedFile) {
      return;
    }

    onUpload(selectedFile);
  }

  return (
    <section className="card">
      <h2>Upload Course PDF</h2>
      <p className="section-description">
        Upload a course document so the assistant can answer questions using its content.
      </p>

      <label className="file-input-label">
        Choose PDF
        <input
          type="file"
          accept="application/pdf"
          onChange={handleFileChange}
          disabled={isUploading}
        />
      </label>

      {isUploading && <p className="status-message">Uploading and processing document...</p>}

      {uploadedDocument && (
        <div className="success-box">
          <p>
            <strong>Uploaded:</strong> {uploadedDocument.filename}
          </p>
          <p>
            <strong>Document ID:</strong> {uploadedDocument.document_id}
          </p>
          <p>
            <strong>Stored chunks:</strong> {uploadedDocument.stored_chunk_count}
          </p>
        </div>
      )}
    </section>
  );
}