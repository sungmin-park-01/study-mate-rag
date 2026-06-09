type AnswerSectionProps = {
  answer: string | null;
  latencyMs: number | null;
};

export function AnswerSection({ answer, latencyMs }: AnswerSectionProps) {
  return (
    <section className="card">
      <h2>Answer</h2>

      {!answer && (
        <p className="empty-message">
          The answer will appear here after you ask a question.
        </p>
      )}

      {answer && (
        <div className="answer-box">
          <p>{answer}</p>

          {latencyMs !== null && (
            <p className="latency">
              Response time: {latencyMs} ms
            </p>
          )}
        </div>
      )}
    </section>
  );
}