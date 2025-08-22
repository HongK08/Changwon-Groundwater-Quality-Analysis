// extracter.js
(() => {
  const ZOOM_FALLBACK = 12;
  const CIRCLE_SELECTOR = "svg#map_gc circle";

  const parseTranslate = (el) => {
    const m = (el?.style?.transform||"").match(/translate\(([-\d.]+)px,\s*([-\d.]+)px\)/);
    return m ? [parseFloat(m[1]), parseFloat(m[2])] : [0,0];
  };
  const parseTileXYZ = (src) => {
    const m = src.match(/\/(\d+)\/(\d+)\/(\d+)\.png$/);
    return m ? { z:+m[1], x:+m[2], y:+m[3] } : null;
  };
  const worldToLonLat = (wx, wy, z) => {
    const n = 256 * Math.pow(2, z);
    const lon = (wx / n) * 360 - 180;
    const lat = (Math.atan(Math.sinh(Math.PI * (1 - 2 * wy / n))) * 180) / Math.PI;
    return [lon, lat];
  };

  const map = document.querySelector(".map");
  const zAttr = map?.getAttribute("data-zoom");
  const Z = zAttr ? +zAttr : ZOOM_FALLBACK;

  const layers = [...document.querySelectorAll("div[id^='map_layer']")];
  let layer = null, tileImg = null, tinfo = null;
  for (const L of layers) {
    const img = [...L.querySelectorAll("img.layerTile")].find(i => parseTileXYZ(i.src)?.z === Z);
    if (img) { layer = L; tileImg = img; tinfo = parseTileXYZ(img.src); break; }
  }
  if (!layer || !tileImg || !tinfo) { console.error("타일/레이어 탐색 실패"); return; }

  const [lx, ly] = parseTranslate(layer);
  const [ix, iy] = parseTranslate(tileImg);
  const worldX0 = tinfo.x * 256 - (lx + ix);
  const worldY0 = tinfo.y * 256 - (ly + iy);

  const circles = [...document.querySelectorAll(CIRCLE_SELECTOR)];
  const rows = [["idx","cx","cy","lon","lat"]];
  circles.forEach((c, idx) => {
    const cx = parseFloat(c.getAttribute("cx"));
    const cy = parseFloat(c.getAttribute("cy"));
    if (isNaN(cx) || isNaN(cy)) return;
    const wx = worldX0 + cx;
    const wy = worldY0 + cy;
    const [lon, lat] = worldToLonLat(wx, wy, Z);
    rows.push([idx, cx, cy, lon.toFixed(7), lat.toFixed(7)]);
  });

  const csv = rows.map(r=>r.join(",")).join("\n");
  const blob = new Blob([csv], {type:"text/csv;charset=utf-8"});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `map_points_z${Z}.csv`;
  document.body.appendChild(a); a.click();
  URL.revokeObjectURL(a.href); a.remove();
})();
