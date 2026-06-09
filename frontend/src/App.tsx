import { useState } from "react";
import "./App.css";
import { askQuestion, uploadDocument } from "./api/studyMateApi";
import { AnswerSection } from "./components/AnswerSection";
import { QuestionSection } from "./components/QuestionSection";
import { SourcesSection } from "./components/SourcesSection";
import { UploadSection } from "./components/UploadSection";
import type { SourcePreview, UploadResponse } from "./types";

function App() {
  const [uploadedDocument, setUploadedDocument] = useState<UploadResponse | null>(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState<string | null>(null);
  const [sources, setSources] = useState<SourcePreview[]>([]);
  const [latencyMs, setLatencyMs] = useState<number | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isAsking, setIsAsking] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  async function handleUpload(file: File) {
    setIsUploading(true);
    setErrorMessage(null);
    setAnswer(null);
    setSources([]);
    setLatencyMs(null);

    try {
      const uploadResponse = await uploadDocument(file);
      setUploadedDocument(uploadResponse);
    } catch {
      setUploadedDocument(null);
      setErrorMessage("The document could not be uploaded. Please check that the file is a valid PDF.");
    } finally {
      setIsUploading(false);
    }
  }

  async function handleAsk() {
    if (!uploadedDocument) {
      setErrorMessage("Please upload a PDF document first.");
      return;
    }

    if (!question.trim()) {
      setErrorMessage("Please enter a question before clicking Ask.");
      return;
    }

    setIsAsking(true);
    setErrorMessage(null);
    setAnswer(null);
    setSources([]);
    setLatencyMs(null);

    try {
      const askResponse = await askQuestion(uploadedDocument.document_id, question.trim());
      setAnswer(askResponse.answer);
      setSources(askResponse.sources);
      setLatencyMs(askResponse.latency_ms);
    } catch {
      setErrorMessage("The answer could not be generated. Please check the backend server and try again.");
    } finally {
      setIsAsking(false);
    }
  }

  return (
    <main className="app-shell">
      <header className="hero">
        <p className="eyebrow">Study Mate RAG</p>
        <h1>Course Document Assistant</h1>
        <p className="hero-description">
          Upload a course PDF, ask a question, and get a source-grounded answer.
        </p>
      </header>

      {errorMessage && (
        <div className="error-banner">
          {errorMessage}
        </div>
      )}

      <div className="layout">
        <div className="left-column">
          <UploadSection
            isUploading={isUploading}
            uploadedDocument={uploadedDocument}
            onUpload={handleUpload}
          />

          <QuestionSection
            question={question}
            isAsking={isAsking}
            isDisabled={!uploadedDocument}
            onQuestionChange={setQuestion}
            onAsk={handleAsk}
          />
        </div>

        <div className="right-column">
          <AnswerSection answer={answer} latencyMs={latencyMs} />
          <SourcesSection sources={sources} />
        </div>
      </div>
    </main>
  );
}

export default App;