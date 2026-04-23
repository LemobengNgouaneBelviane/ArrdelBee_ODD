"use client";

import "leaflet/dist/leaflet.css";

import { useEffect, useMemo, useState } from "react";
import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";

// Dynamic import pour éviter SSR issues
let L: any;
if (typeof window !== "undefined") {
  L = require("leaflet");

  // Fix icônes Leaflet (Next.js)
  const DefaultIcon = L.icon({
    iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
    iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
    shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
    iconSize: [25, 41],
    iconAnchor: [12, 41],
  });
  L.Marker.prototype.options.icon = DefaultIcon;
}

type GeoPoint = { lat: number; lon: number };
type Commune = { id: number; name: string; department_id: number; department_name?: string | null };

async function geocodeCommune(name: string): Promise<GeoPoint | null> {
  const q = encodeURIComponent(`${name}, Cameroun`);
  const url = `https://nominatim.openstreetmap.org/search?format=json&q=${q}&limit=1`;
  const res = await fetch(url, { headers: { "Accept-Language": "fr" } });
  if (!res.ok) return null;
  const data = (await res.json()) as Array<{ lat: string; lon: string }>;
  if (!data.length) return null;
  return { lat: Number(data[0].lat), lon: Number(data[0].lon) };
}

function cacheKey(communeId: number) {
  return `odd_arrdel_geo_commune_${communeId}`;
}

async function getOrGeocode(commune: Commune): Promise<GeoPoint | null> {
  const k = cacheKey(commune.id);
  const cached = localStorage.getItem(k);
  if (cached) {
    try {
      return JSON.parse(cached) as GeoPoint;
    } catch {
      localStorage.removeItem(k);
    }
  }
  const p = await geocodeCommune(commune.name);
  if (p) localStorage.setItem(k, JSON.stringify(p));
  return p;
}

export function MapView({ communes, selectedCommuneId }: { communes: Commune[]; selectedCommuneId: number | null }) {
  const [points, setPoints] = useState<Record<number, GeoPoint>>({});

  const selected = useMemo(
    () => communes.find((c) => c.id === selectedCommuneId) ?? null,
    [communes, selectedCommuneId]
  );

  useEffect(() => {
    const target = selected ? [selected] : communes.slice(0, 25);
    let cancelled = false;
    (async () => {
      for (const c of target) {
        if (cancelled) return;
        // Utilise l'état le plus récent (évite la fermeture sur un état obsolète).
        if (points[c.id]) continue;
        const p = await getOrGeocode(c);
        if (p && !cancelled) {
          setPoints((prev) => ({ ...prev, [c.id]: p }));
        }
        // Évite de saturer le navigateur (et Nominatim) en dev.
        await new Promise((r) => setTimeout(r, 120));
      }
    })();
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedCommuneId, communes]);

  const center: [number, number] = selected && points[selected.id] ? [points[selected.id].lat, points[selected.id].lon] : [4.05, 9.7];

  return (
    <div className="overflow-hidden rounded-xl border">
      <MapContainer center={center} zoom={selected ? 10 : 7} style={{ height: 520, width: "100%" }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {communes.map((c) => {
          const p = points[c.id];
          if (!p) return null;
          return (
            <Marker key={c.id} position={[p.lat, p.lon]}>
              <Popup>
                <div className="text-sm font-semibold">{c.name}</div>
                <div className="text-xs text-zinc-600">{c.department_name ?? ""}</div>
              </Popup>
            </Marker>
          );
        })}
      </MapContainer>
    </div>
  );
}

