import type { SourcePreview } from "../types";

type SourcesSectionProps = {
  sources: SourcePreview[];
};

export function SourcesSection({ sources }: SourcesSectionProps) {
  return (
    <section className="card">
      <h2>Sources</h2>

      {sources.length === 0 && (
        <p className="empty-message">
          Source previews will appear here after an answer is generated.
        </p>
      )}

      {sources.length > 0 && (
        <div className="source-list">
          {sources.map((source, index) => (
            <article className="source-card" key={`${source.filename}-${source.page_number}-${index}`}>
              <div className="source-header">
                <strong>{source.filename}</strong>
                <span>Page {source.page_number}</span>
              </div>
              <p>{source.content_preview}</p>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}