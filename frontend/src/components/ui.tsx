import type { ComponentProps, ReactNode } from "react";

function cx(...parts: Array<string | false | null | undefined>) {
  return parts.filter(Boolean).join(" ");
}

export function PageHeader({
  title,
  subtitle,
  actions,
}: {
  title: ReactNode;
  subtitle?: ReactNode;
  actions?: ReactNode;
}) {
  return (
    <div className="space-y-4 border-b border-[color:var(--border)] pb-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div className="min-w-0 flex-1">
          <h1 className="text-3xl font-bold tracking-tight text-[color:var(--foreground)]">{title}</h1>
          {subtitle ? <p className="mt-2 text-base text-[color:var(--muted)]">{subtitle}</p> : null}
        </div>
        {actions ? <div className="flex shrink-0 items-center gap-3">{actions}</div> : null}
      </div>
    </div>
  );
}

export function SectionTitle({
  title,
  description,
}: {
  title: ReactNode;
  description?: ReactNode;
}) {
  return (
    <div className="space-y-2">
      <h2 className="text-xl font-bold text-[color:var(--foreground)]">{title}</h2>
      {description ? <p className="text-sm text-[color:var(--muted)]">{description}</p> : null}
    </div>
  );
}

export function Card({
  title,
  description,
  children,
  className,
  hoverable = true,
}: {
  title?: ReactNode;
  description?: ReactNode;
  children?: ReactNode;
  className?: string;
  hoverable?: boolean;
}) {
  return (
    <section
      className={cx(
        "rounded-2xl border border-[color:var(--border)] bg-white p-6 shadow-sm transition",
        hoverable && "hover:shadow-md hover:border-[color:var(--primary)]/30 cursor-pointer",
        className
      )}
    >
      {title ? (
        <div className="mb-4 space-y-1">
          <div className="text-sm font-semibold text-[color:var(--foreground)]">{title}</div>
          {description ? <div className="text-xs text-[color:var(--muted)]">{description}</div> : null}
        </div>
      ) : null}
      {children}
    </section>
  );
}

export function Stat({
  label,
  value,
  hint,
  icon,
  color,
}: {
  label: ReactNode;
  value: ReactNode;
  hint?: ReactNode;
  icon?: ReactNode;
  color?: "default" | "primary" | "success" | "danger";
}) {
  const bgColor =
    color === "primary"
      ? "bg-gradient-to-br from-[color:var(--primary)]/5 to-[color:var(--primary)]/10 border-[color:var(--primary)]/20"
      : color === "success"
        ? "bg-emerald-50 border-emerald-200/50"
        : color === "danger"
          ? "bg-rose-50 border-rose-200/50"
          : "bg-[color:var(--surface-2)] border-[color:var(--border)]";

  return (
    <div className={cx("rounded-2xl border p-5 transition", bgColor)}>
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="text-xs font-medium uppercase tracking-wide text-[color:var(--muted)]">{label}</div>
          <div className="mt-2 text-3xl font-bold text-[color:var(--foreground)]">{value}</div>
          {hint ? <div className="mt-1 text-xs text-[color:var(--muted)]">{hint}</div> : null}
        </div>
        {icon ? <div className="shrink-0 text-2xl opacity-40">{icon}</div> : null}
      </div>
    </div>
  );
}

export function Badge({
  label,
  oddCode,
  variant = "default",
}: {
  label: ReactNode;
  oddCode?: string;
  variant?: "default" | "solid" | string;
}) {
  // Map ODD codes to colors
  const oddColors: Record<string, string> = {
    "01": "bg-[#e5243b]/10 text-[#e5243b] border-[#e5243b]/30",
    "02": "bg-[#dda63b]/10 text-[#dda63b] border-[#dda63b]/30",
    "03": "bg-[#4c9f38]/10 text-[#4c9f38] border-[#4c9f38]/30",
    "04": "bg-[#c6192b]/10 text-[#c6192b] border-[#c6192b]/30",
    "05": "bg-[#ff3a21]/10 text-[#ff3a21] border-[#ff3a21]/30",
    "06": "bg-[#26bde2]/10 text-[#26bde2] border-[#26bde2]/30",
    "07": "bg-[#fccc0a]/10 text-[#fccc0a] border-[#fccc0a]/30",
    "08": "bg-[#a21e48]/10 text-[#a21e48] border-[#a21e48]/30",
    "09": "bg-[#dd1c3b]/10 text-[#dd1c3b] border-[#dd1c3b]/30",
    "10": "bg-[#dd1c3b]/10 text-[#dd1c3b] border-[#dd1c3b]/30",
    "11": "bg-[#fd6925]/10 text-[#fd6925] border-[#fd6925]/30",
    "12": "bg-[#bf8b2e]/10 text-[#bf8b2e] border-[#bf8b2e]/30",
    "13": "bg-[#407d52]/10 text-[#407d52] border-[#407d52]/30",
    "14": "bg-[#0a97d9]/10 text-[#0a97d9] border-[#0a97d9]/30",
    "15": "bg-[#56c596]/10 text-[#56c596] border-[#56c596]/30",
    "16": "bg-[#00689d]/10 text-[#00689d] border-[#00689d]/30",
    "17": "bg-[#1fbf9b]/10 text-[#1fbf9b] border-[#1fbf9b]/30",
  };

  const colorClass = oddCode ? oddColors[oddCode] || "bg-slate-100 text-slate-700 border-slate-200" : "bg-slate-100 text-slate-700 border-slate-200";

  return (
    <span className={cx("inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-medium", colorClass)}>
      {label}
    </span>
  );
}

export function Button({
  variant = "primary",
  size = "md",
  className,
  ...props
}: ComponentProps<"button"> & { variant?: "primary" | "secondary" | "tertiary" | "danger"; size?: "sm" | "md" | "lg" }) {
  const sizeClass = size === "sm" ? "px-3 py-1.5 text-xs" : size === "lg" ? "px-6 py-3 text-base" : "px-4 py-2 text-sm";

  return (
    <button
      {...props}
      className={cx(
        "inline-flex items-center justify-center gap-2 rounded-xl font-medium transition focus:outline-none focus:ring-2 disabled:opacity-60 disabled:cursor-not-allowed",
        sizeClass,
        variant === "primary" && "bg-[color:var(--primary)] text-white hover:bg-[color:var(--primary-dark)] focus:ring-[color:var(--primary)]/30",
        variant === "secondary" &&
          "border border-[color:var(--border)] bg-white text-[color:var(--foreground)] hover:bg-[color:var(--surface-2)]",
        variant === "tertiary" && "text-[color:var(--primary)] hover:bg-[color:var(--primary)]/5",
        variant === "danger" && "bg-rose-600 text-white hover:bg-rose-700 focus:ring-rose-600/30",
        className
      )}
    />
  );
}

export function Input({ label, className, ...props }: ComponentProps<"input"> & { label?: string }) {
  return (
    <div>
      {label ? <label className="block text-xs font-medium text-[color:var(--foreground)] mb-1.5">{label}</label> : null}
      <input
        {...props}
        className={cx(
          "w-full rounded-xl border border-[color:var(--border)] bg-white px-4 py-2.5 text-sm text-[color:var(--foreground)] shadow-sm outline-none transition placeholder:text-[color:var(--muted)]/50 focus:border-[color:var(--primary)] focus:ring-2 focus:ring-[color:var(--primary)]/10",
          className
        )}
      />
    </div>
  );
}

export function Textarea({ label, className, ...props }: ComponentProps<"textarea"> & { label?: string }) {
  return (
    <div>
      {label ? <label className="block text-xs font-medium text-[color:var(--foreground)] mb-1.5">{label}</label> : null}
      <textarea
        {...props}
        className={cx(
          "w-full rounded-xl border border-[color:var(--border)] bg-white px-4 py-2.5 text-sm text-[color:var(--foreground)] shadow-sm outline-none transition placeholder:text-[color:var(--muted)]/50 focus:border-[color:var(--primary)] focus:ring-2 focus:ring-[color:var(--primary)]/10",
          className
        )}
      />
    </div>
  );
}

export function Select({ label, className, ...props }: ComponentProps<"select"> & { label?: string }) {
  return (
    <div>
      {label ? <label className="block text-xs font-medium text-[color:var(--foreground)] mb-1.5">{label}</label> : null}
      <select
        {...props}
        className={cx(
          "w-full rounded-xl border border-[color:var(--border)] bg-white px-4 py-2.5 text-sm text-[color:var(--foreground)] shadow-sm outline-none transition focus:border-[color:var(--primary)] focus:ring-2 focus:ring-[color:var(--primary)]/10",
          className
        )}
      />
    </div>
  );
}

export function Alert({
  tone = "info",
  title,
  children,
}: {
  tone?: "info" | "success" | "danger" | "warning";
  title?: ReactNode;
  children: ReactNode;
}) {
  const styles =
    tone === "success"
      ? "border-emerald-200 bg-emerald-50 text-emerald-900"
      : tone === "danger"
        ? "border-rose-200 bg-rose-50 text-rose-900"
        : tone === "warning"
          ? "border-amber-200 bg-amber-50 text-amber-900"
          : "border-blue-200 bg-blue-50 text-blue-900";
  return (
    <div className={cx("rounded-xl border p-4 text-sm", styles)}>
      {title ? <div className="font-semibold">{title}</div> : null}
      <div className={cx(title ? "mt-2" : "", "")}>{children}</div>
    </div>
  );
}

export function Table({
  columns,
  children,
}: {
  columns: Array<{ label: ReactNode; className?: string }>;
  children: ReactNode;
}) {
  return (
    <div className="overflow-hidden rounded-xl border border-[color:var(--border)] bg-white shadow-sm">
      <table className="w-full text-sm">
        <thead className="border-b border-[color:var(--border)] bg-[color:var(--surface-2)]">
          <tr>
            {columns.map((c, idx) => (
              <th
                key={idx}
                className={cx("px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-[color:var(--muted)]", c.className)}
              >
                {c.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-[color:var(--border)]">{children}</tbody>
      </table>
    </div>
  );
}

