export function AppShell({ actions, children, description, metrics, title }) {
  return (
    <div className="app-shell">
      <header className="app-shell__header">
        <div>
          <h1 className="app-shell__title">{title}</h1>
          <p className="app-shell__description">{description}</p>
        </div>
        <div className="app-shell__toolbar">
          <div className="app-shell__actions">{actions}</div>
          <div className="app-shell__metrics">{metrics}</div>
        </div>
      </header>
      <main className="app-shell__content">{children}</main>
    </div>
  );
}
