type QuestionSectionProps = {
  question: string;
  isAsking: boolean;
  isDisabled: boolean;
  onQuestionChange: (question: string) => void;
  onAsk: () => void;
};

export function QuestionSection({
  question,
  isAsking,
  isDisabled,
  onQuestionChange,
  onAsk,
}: QuestionSectionProps) {
  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onAsk();
  }

  return (
    <section className="card">
      <h2>Ask a Question</h2>
      <p className="section-description">
        Ask a question based on the uploaded document.
      </p>

      <form onSubmit={handleSubmit} className="question-form">
        <textarea
          value={question}
          onChange={(event) => onQuestionChange(event.target.value)}
          placeholder="Example: How much is the midterm worth?"
          disabled={isDisabled || isAsking}
          rows={4}
        />

        <button type="submit" disabled={isDisabled || isAsking || !question.trim()}>
          {isAsking ? "Asking..." : "Ask"}
        </button>
      </form>

      {isDisabled && (
        <p className="status-message">
          Upload a PDF document before asking a question.
        </p>
      )}
    </section>
  );
}