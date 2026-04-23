"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export function NavLink({ href, label }: { href: string; label: string }) {
  const pathname = usePathname();
  const active = pathname === href || (href !== "/" && pathname.startsWith(href));
  return (
    <Link
      href={href}
      className={[
        "group flex items-center justify-between rounded-lg px-4 py-2.5 text-sm font-medium transition",
        active
          ? "bg-[color:var(--primary)] text-white shadow-sm"
          : "text-[color:var(--foreground)]/70 hover:bg-[color:var(--primary)]/5 hover:text-[color:var(--primary)]",
      ].join(" ")}
    >
      <span>{label}</span>
      <span
        className={[
          "text-xs transition",
          active ? "text-white/60" : "opacity-0 group-hover:opacity-100",
        ].join(" ")}
      >
        →
      </span>
    </Link>
  );
}

