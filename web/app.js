"use strict";

const app = document.querySelector("#app");
let archive = null;
let cars = [];

const cleanText = (value) => String(value ?? "")
  .replace(/([A-Za-z])�s\b/g, "$1’s")
  .replace(/(\d)�(\d)/g, "$1–$2")
  .replaceAll("�", "—");

const e = (value) => cleanText(value)
  .replaceAll("&", "&amp;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;")
  .replaceAll('"', "&quot;")
  .replaceAll("'", "&#039;");

const safeUrl = (value) => {
  try {
    const url = new URL(String(value));
    return ["http:", "https:"].includes(url.protocol) ? e(url.href) : "";
  } catch {
    return "";
  }
};

const imagePath = (value) => {
  const path = String(value || "");
  if (/^\/?assets\/[A-Za-z0-9_ .()+-]+$/i.test(path)) return encodeURI(path.replace(/^\/+/, ""));
  return "";
};

const numberFrom = (value) => {
  const match = String(value ?? "").replaceAll(",", "").match(/-?\d+(?:\.\d+)?/);
  return match ? Number(match[0]) : null;
};

const formatNumber = (value, maximumFractionDigits = 0) =>
  Number(value).toLocaleString("en-US", { maximumFractionDigits });

const yearRange = (car) => {
  const start = car.model_year_from;
  const end = car.model_year_to;
  if (!start) return "Year unknown";
  return !end || start === end ? String(start) : `${start}–${end}`;
};

const firstAttribute = (car, labels) => {
  for (const wanted of labels) {
    const found = car.attributes.find((item) => cleanText(item.label).toLowerCase() === wanted.toLowerCase());
    if (found) return found;
  }
  return null;
};

const attributeDisplay = (item) => {
  if (!item) return "—";
  const value = cleanText(item.value);
  const unit = cleanText(item.unit);
  return unit && numberFrom(value) !== null && !value.toLowerCase().includes(unit.toLowerCase()) ? `${value} ${unit}` : value;
};

const primaryMedia = (car) => car.media.find((item) => Number(item.is_primary) === 1) || car.media[0] || null;
const sourceMap = (car) => new Map(car.sources.map((source) => [Number(source.id), source]));

const sourceDot = (record, sources, label = "Source") => {
  const source = sources.get(Number(record.source_id));
  return source || record.source_url ? `<span class="source-dot" title="${e(source?.title || "Evidence recorded in the Source Library")}">● ${e(label)}</span>` : "";
};

const recordMeta = (record, car, sources) => {
  const inherited = record.car_id && record.car_id !== car.id;
  const parts = [
    record.scope_level ? `<span class="meta-badge">${e(record.scope_level)}</span>` : "",
    inherited ? '<span class="meta-badge inherited">Inherited record</span>' : "",
    sourceDot(record, sources),
  ].filter(Boolean);
  return parts.length ? `<span class="record-meta">${parts.join("")}</span>` : "";
};

const galleryMeta = (media, car, sources) => `<span>${e(media.caption || media.media_type)}</span><span>${e([media.media_type, media.creator, media.license].filter(Boolean).join(" · "))}${recordMeta(media, car, sources)}</span>`;

const optionList = (values, selected, placeholder) => [
  `<option value="">${e(placeholder)}</option>`,
  ...values.map((value) => `<option value="${e(value)}"${value === selected ? " selected" : ""}>${e(value)}</option>`),
].join("");

const currentHash = () => location.hash.slice(1) || "/";

function catalogueParams() {
  const hash = currentHash();
  const query = hash.includes("?") ? hash.slice(hash.indexOf("?") + 1) : "";
  return new URLSearchParams(query);
}

function carIndex(car) {
  const power = firstAttribute(car, ["Maximum power", "Maximum power (metric)"]);
  const speed = firstAttribute(car, ["Maximum speed", "Top speed"]);
  const weight = firstAttribute(car, ["Vehicle weight", "Curb weight", "Kerb weight", "Dry weight"]);
  const production = firstAttribute(car, ["Total announced production", "Production total"]);
  return {
    car,
    power,
    speed,
    weight,
    production,
    powerNumber: numberFrom(power?.value),
    speedNumber: numberFrom(speed?.value),
    weightNumber: numberFrom(weight?.value),
    productionNumber: numberFrom(production?.value),
    search: cleanText(JSON.stringify(car)).toLowerCase(),
  };
}

function filteredCars(params) {
  const queryTokens = cleanText(params.get("q")).toLowerCase().split(/\s+/).filter(Boolean);
  const minimumYear = numberFrom(params.get("year_from"));
  const maximumYear = numberFrom(params.get("year_to"));
  const minimumPower = numberFrom(params.get("power_min"));
  const minimumSpeed = numberFrom(params.get("speed_min"));

  const result = cars.map(carIndex).filter((item) => {
    const car = item.car;
    if (queryTokens.some((token) => !item.search.includes(token))) return false;
    if (params.get("manufacturer") && car.manufacturer !== params.get("manufacturer")) return false;
    if (params.get("model") && car.model_family !== params.get("model")) return false;
    if (params.get("category") && car.category !== params.get("category")) return false;
    if (params.get("origin") && car.origin_country !== params.get("origin")) return false;
    if (params.get("road_legal") && String(car.road_legal) !== params.get("road_legal")) return false;
    if (minimumYear && (!car.model_year_to || Number(car.model_year_to) < minimumYear)) return false;
    if (maximumYear && (!car.model_year_from || Number(car.model_year_from) > maximumYear)) return false;
    if (minimumPower !== null && (item.powerNumber === null || item.powerNumber < minimumPower)) return false;
    if (minimumSpeed !== null && (item.speedNumber === null || item.speedNumber < minimumSpeed)) return false;
    if (params.get("has_gallery") === "1" && car.media.length < 3) return false;
    if (params.get("has_prices") === "1" && !car.price_records.length) return false;
    if (params.get("has_sources") === "1" && !car.sources.length) return false;
    if (params.get("has_colors") === "1" && !car.color_records.length) return false;
    return true;
  });

  const sort = params.get("sort") || "name";
  const textKey = (item) => `${item.car.manufacturer} ${item.car.model_family} ${item.car.variant}`;
  const ascendingMissing = (value) => value === null ? Number.POSITIVE_INFINITY : value;
  const descendingMissing = (value) => value === null ? Number.NEGATIVE_INFINITY : value;
  result.sort((a, b) => {
    if (sort === "newest") return (b.car.model_year_from || -1) - (a.car.model_year_from || -1);
    if (sort === "oldest") return (a.car.model_year_from || 9999) - (b.car.model_year_from || 9999);
    if (sort === "power") return descendingMissing(b.powerNumber) - descendingMissing(a.powerNumber);
    if (sort === "speed") return descendingMissing(b.speedNumber) - descendingMissing(a.speedNumber);
    if (sort === "lightest") return ascendingMissing(a.weightNumber) - ascendingMissing(b.weightNumber);
    if (sort === "rarest") return ascendingMissing(a.productionNumber) - ascendingMissing(b.productionNumber);
    if (sort === "recent") return cleanText(b.car.created_at).localeCompare(cleanText(a.car.created_at));
    return textKey(a).localeCompare(textKey(b));
  });
  return result;
}

function carCard(item) {
  const car = item.car;
  const media = primaryMedia(car);
  const image = imagePath(media?.location);
  return `<a class="car-card" href="#/car/${encodeURIComponent(car.id)}">
    <div class="card-image">
      ${image ? `<img src="${image}" alt="${e(media.caption || `${car.manufacturer} ${car.model_family}`)}" loading="lazy">` : ""}
      <span class="pill dark">${e(car.category || "Car record")}</span>
    </div>
    <div class="card-body">
      <div class="card-kicker"><span>${e(car.manufacturer)}</span><span>${e(yearRange(car))}</span></div>
      <h3>${e(car.model_family)}</h3>
      <div class="variant">${e(car.variant)}</div>
      <div class="card-specs">
        <div><strong>${e(attributeDisplay(item.power))}</strong><span>Power</span></div>
        <div><strong>${e(attributeDisplay(item.speed))}</strong><span>Top speed</span></div>
        <div><strong>${e(attributeDisplay(item.production))}</strong><span>Production</span></div>
      </div>
    </div>
  </a>`;
}

function renderCatalogue() {
  const params = catalogueParams();
  const selectedMake = params.get("manufacturer") || "";
  const makes = [...new Set(cars.map((car) => car.manufacturer))].sort();
  const models = [...new Set(cars.filter((car) => !selectedMake || car.manufacturer === selectedMake).map((car) => car.model_family))].sort();
  const categories = [...new Set(cars.map((car) => car.category).filter(Boolean))].sort();
  const origins = [...new Set(cars.map((car) => car.origin_country).filter(Boolean))].sort();
  const results = filteredCars(params);
  const activeEntries = [...params.entries()].filter(([key, value]) => value && key !== "sort");
  const labels = { q: "Search", manufacturer: "Make", model: "Model", category: "Category", origin: "Origin", year_from: "From", year_to: "To", power_min: "Power", speed_min: "Speed", road_legal: "Road use", has_gallery: "Gallery", has_prices: "Prices", has_sources: "Sources", has_colors: "Colors" };
  const activeChips = activeEntries.map(([key, value]) => {
    const copy = new URLSearchParams(params);
    copy.delete(key);
    const href = copy.toString() ? `#/?${copy}` : "#/";
    const shown = value === "1" && key.startsWith("has_") ? "Yes" : value === "1" && key === "road_legal" ? "Legal" : value === "0" && key === "road_legal" ? "Track-only" : value;
    return `<a class="filter-chip" href="${href}">${e(labels[key] || key)}: ${e(shown)} ×</a>`;
  }).join("");

  const mediaCount = archive.media_count ?? cars.reduce((total, car) => total + car.media.length, 0);
  const sourceCount = archive.source_count ?? cars.reduce((total, car) => total + car.sources.length, 0);
  app.innerHTML = `
    <section class="catalogue-hero">
      <div class="shell intro">
        <div class="eyebrow">Curated automotive knowledge</div>
        <h1>Every legend has<br><em>a deeper story.</em></h1>
        <p class="lead">Explore specifications, engineering decisions, production evidence, market observations and licensed photography in one carefully sourced archive.</p>
        <div class="stats">
          <div class="stat"><strong>${archive.car_count}</strong><span>Car variants</span></div>
          <div class="stat"><strong>${archive.manufacturer_count}</strong><span>Manufacturers</span></div>
          <div class="stat"><strong>${formatNumber(mediaCount)}</strong><span>Images</span></div>
          <div class="stat"><strong>${formatNumber(sourceCount)}</strong><span>Sources</span></div>
        </div>
      </div>
    </section>
    <div class="shell">
      <form class="search-panel" id="filters">
        <div class="search-row">
          <div class="field"><label for="q">Search everything</label><input id="q" name="q" value="${e(params.get("q") || "")}" placeholder="LFA tachometer, V12, carbon…"></div>
          <div class="field"><label for="manufacturer">Manufacturer</label><select id="manufacturer" name="manufacturer">${optionList(makes, selectedMake, "All makes")}</select></div>
          <div class="field"><label for="model">Model family</label><select id="model" name="model">${optionList(models, params.get("model") || "", "All models")}</select></div>
          <div class="field"><label for="category">Category</label><select id="category" name="category">${optionList(categories, params.get("category") || "", "All categories")}</select></div>
          <div class="field"><label for="sort">Sort</label><select id="sort" name="sort">
            ${[["name","Name A–Z"],["newest","Newest first"],["oldest","Oldest first"],["power","Most powerful"],["speed","Fastest"],["lightest","Lightest"],["rarest","Rarest"],["recent","Recently added"]].map(([value,label]) => `<option value="${value}"${(params.get("sort") || "name") === value ? " selected" : ""}>${label}</option>`).join("")}
          </select></div>
          <button class="button" type="submit">Explore</button>
        </div>
        <details class="advanced"${["origin","year_from","year_to","power_min","speed_min","road_legal","has_gallery","has_prices","has_sources","has_colors"].some((key) => params.get(key)) ? " open" : ""}>
          <summary>Advanced filters</summary>
          <div class="advanced-grid">
            <div class="field"><label for="origin">Country of origin</label><select id="origin" name="origin">${optionList(origins, params.get("origin") || "", "All countries")}</select></div>
            <div class="field"><label for="year_from">Built after</label><input id="year_from" name="year_from" type="number" value="${e(params.get("year_from") || "")}" placeholder="1990"></div>
            <div class="field"><label for="year_to">Built before</label><input id="year_to" name="year_to" type="number" value="${e(params.get("year_to") || "")}" placeholder="2026"></div>
            <div class="field"><label for="power_min">Minimum power (kW)</label><input id="power_min" name="power_min" type="number" value="${e(params.get("power_min") || "")}" placeholder="500"></div>
            <div class="field"><label for="speed_min">Minimum speed (km/h)</label><input id="speed_min" name="speed_min" type="number" value="${e(params.get("speed_min") || "")}" placeholder="300"></div>
            <div class="field"><label for="road_legal">Road use</label><select id="road_legal" name="road_legal">${optionList(["1","0"], params.get("road_legal") || "", "Any status").replace(">1<", ">Road legal<").replace(">0<", ">Track-only<")}</select></div>
            <div class="checks">
              ${[["has_gallery","3+ images"],["has_prices","Price history"],["has_sources","Documented sources"],["has_colors","Color records"]].map(([name,label]) => `<label class="check"><input type="checkbox" name="${name}" value="1"${params.get(name) === "1" ? " checked" : ""}> ${label}</label>`).join("")}
            </div>
          </div>
        </details>
      </form>
      <div class="catalogue-toolbar"><strong>${results.length} ${results.length === 1 ? "car" : "cars"}</strong>${activeEntries.length ? '<a class="button secondary" href="#/">Clear filters</a>' : '<span class="muted small">Select a car to open its full record</span>'}</div>
      ${activeChips ? `<div class="active-filters">${activeChips}</div>` : ""}
      ${results.length ? `<div class="car-grid">${results.map(carCard).join("")}</div>` : '<div class="empty"><h3>No matching cars</h3><p class="muted">Try removing a filter or using a broader search phrase.</p><a class="button secondary" href="#/">Reset search</a></div>'}
    </div>`;

  document.title = "Supercar Archive · Searchable catalogue";
  const form = document.querySelector("#filters");
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const next = new URLSearchParams();
    for (const [key, value] of new FormData(form).entries()) if (String(value).trim()) next.set(key, String(value).trim());
    location.hash = next.toString() ? `#/?${next}` : "#/";
  });
  form.querySelectorAll("select").forEach((select) => select.addEventListener("change", () => form.requestSubmit()));
}

function detailGallery(car, sources) {
  if (!car.media.length) return '<div class="empty">No local images are recorded for this car.</div>';
  const first = primaryMedia(car);
  const buttons = car.media.map((media) => {
    const path = imagePath(media.location);
    return path ? `<button type="button" data-gallery-id="${media.id}"${media.id === first.id ? ' class="active"' : ""}><img src="${path}" alt="${e(media.caption || media.media_type)}" loading="lazy"></button>` : "";
  }).join("");
  return `<div class="gallery">${buttons}</div>
    <div class="gallery-meta" id="gallery-meta">${galleryMeta(first, car, sources)}</div>`;
}

function renderDetail(car) {
  const sources = sourceMap(car);
  const primary = primaryMedia(car);
  const primaryPath = imagePath(primary?.location);
  const quick = [
    ["Power", firstAttribute(car, ["Maximum power", "Maximum power (metric)"])],
    ["Top speed", firstAttribute(car, ["Maximum speed", "Top speed"])],
    ["0–100 km/h", firstAttribute(car, ["0–100 km/h", "0�100 km/h"])],
    ["Weight", firstAttribute(car, ["Vehicle weight", "Curb weight", "Kerb weight", "Dry weight"])],
    ["Engine", firstAttribute(car, ["Configuration", "Engine configuration"])],
    ["Production", firstAttribute(car, ["Total announced production", "Production total"])],
  ];

  const sections = new Map();
  car.attributes.forEach((item) => {
    if (!sections.has(item.section)) sections.set(item.section, []);
    sections.get(item.section).push(item);
  });
  const specifications = [...sections.entries()].map(([section, items]) => `<section class="panel">
    <h3>${e(section)}</h3>
    <dl>${items.map((item) => `<div class="spec-row"><dt>${e(item.label)}</dt><dd><span>${e(attributeDisplay(item))}</span>${recordMeta(item, car, sources)}</dd></div>`).join("")}</dl>
  </section>`).join("");

  const related = cars.filter((item) => item.manufacturer === car.manufacturer && item.model_family === car.model_family);
  const familyCards = related.map((item) => {
    const power = firstAttribute(item, ["Maximum power", "Maximum power (metric)"]);
    return `<a class="family-card${item.id === car.id ? " current" : ""}" href="#/car/${encodeURIComponent(item.id)}"><span class="pill">${e(yearRange(item))}</span><h3>${e(item.variant)}</h3><div class="small muted">${e(item.generation || "Generation unknown")} · ${e(attributeDisplay(power))}</div></a>`;
  }).join("");

  const colors = car.color_records.length ? car.color_records.map((color) => `<article class="panel">
    <div class="color-swatch" style="background:${/^#[0-9a-f]{6}$/i.test(color.swatch_hex || "") ? color.swatch_hex : "#d8d4cc"}"></div>
    <span class="pill accent">${e(color.color_type)}</span><h3>${e(color.color_name)}</h3>
    ${color.color_code ? `<p class="small"><strong>Code:</strong> ${e(color.color_code)}</p>` : ""}
    <p class="small muted">${e(color.availability_scope || "Availability scope unknown")}</p>
    <p class="small"><strong>${color.production_count !== null ? `${formatNumber(color.production_count)} documented` : "Production count unknown"}</strong>${color.production_percentage !== null ? ` · ${e(color.production_percentage)}%` : ""}</p>
    ${color.count_scope ? `<p class="small muted">Count scope: ${e(color.count_scope)}</p>` : ""}
    ${color.notes ? `<p class="small muted">${e(color.notes)}</p>` : ""}
    <span class="confidence">${e(color.confidence)}</span>${recordMeta(color, car, sources)}
  </article>`).join("") : '<div class="empty">No color evidence is recorded yet.</div>';

  const geoGroups = new Map();
  car.country_distribution.forEach((record) => {
    if (!geoGroups.has(record.distribution_type)) geoGroups.set(record.distribution_type, []);
    geoGroups.get(record.distribution_type).push(record);
  });
  const geography = geoGroups.size ? [...geoGroups.entries()].map(([type, records]) => {
    const maximum = Math.max(...records.map((record) => record.vehicle_count || 0), 1);
    return `<article class="panel"><div class="eyebrow">Documented distribution</div><h3>${e(type)}</h3>${records.map((record) => `<div class="distribution-row">
      <div class="distribution-label"><strong>${e(record.country)}</strong><span>${record.vehicle_count !== null ? formatNumber(record.vehicle_count) : "Unknown"}${record.share_percentage !== null ? ` · ${e(record.share_percentage)}%` : ""}</span></div>
      <div class="distribution-track"><div class="distribution-fill" style="width:${Math.max(3, Math.round((record.vehicle_count || 0) / maximum * 100))}%"></div></div>
      <div class="small muted">${e(record.confidence)}${record.region ? ` · ${e(record.region)}` : ""}${record.as_of_date ? ` · as of ${e(record.as_of_date)}` : ""}${record.denominator ? ` · denominator ${formatNumber(record.denominator)}` : ""}</div>
      ${record.notes ? `<div class="small muted record-note">${e(record.notes)}</div>` : ""}
      ${recordMeta(record, car, sources)}
    </div>`).join("")}</article>`;
  }).join("") : '<div class="empty">No geographic distribution is recorded yet.</div>';

  const facts = car.facts.length ? car.facts.map((fact) => `<article class="panel fact-card">
    <div class="category">${e(fact.category || "Documented story")}</div><h3>${e(fact.title)}</h3><p>${e(fact.explanation)}</p>
    ${fact.why_it_matters ? `<div class="why"><strong>Why it matters</strong><br>${e(fact.why_it_matters)}</div>` : ""}
    <p class="confidence">${e(fact.confidence || "Evidence recorded")}</p>${recordMeta(fact, car, sources)}
  </article>`).join("") : '<div class="empty">No engineering stories are recorded yet.</div>';

  const priceRows = [...car.price_records].reverse();
  const msrp = car.price_records.find((record) => record.price_type === "Announced MSRP" && record.currency === "USD");
  const latestSale = priceRows.find((record) => record.price_type === "Auction sale" && record.currency === "USD");
  const usdPrices = car.price_records.filter((record) => record.currency === "USD" && Number(record.amount) > 0);
  const maximumPrice = Math.max(...usdPrices.map((record) => Number(record.amount)), 1);
  const priceChart = usdPrices.length ? `<div class="panel price-chart"><div class="price-bars">${usdPrices.map((record) => `<div class="price-bar-item" title="${e(record.price_type)}: $${formatNumber(record.amount)}"><strong>$${formatNumber(Number(record.amount) / 1000)}k</strong><div class="price-bar" style="height:${Math.max(4, Math.round(Number(record.amount) / maximumPrice * 140))}px"></div><small>${e(record.observation_date || "—")}</small></div>`).join("")}</div><p class="small muted">Published USD observations for different physical cars. Mileage, condition and specification affect comparability.</p></div>` : "";
  const prices = priceRows.length ? `<div class="table-wrap"><table><thead><tr><th>Date</th><th>Type</th><th>Amount</th><th>Market</th><th>Venue / vehicle</th><th>Evidence</th></tr></thead><tbody>${priceRows.map((record) => `<tr>
    <td>${e(record.observation_date || "—")}</td><td>${e(record.price_type)}</td><td class="money">${e(record.currency)} ${formatNumber(record.amount, 2)}</td><td>${e(record.market || "—")}</td>
    <td>${e([record.venue, record.serial_number, record.mileage].filter(Boolean).join(" · ") || "—")} ${record.notes ? `<div class="small muted">${e(record.notes)}</div>` : ""}</td><td>${sourceDot(record, sources, "View") || "—"}</td>
  </tr>`).join("")}</tbody></table></div>` : '<div class="empty">No price observations are recorded yet.</div>';

  const sourceLibrary = car.sources.length ? `<ul class="source-list">${car.sources.map((source) => `<li><span class="pill">${e(source.source_type || "Reference")}</span><span><strong>${e(source.publisher || "Source")}</strong><br>${e(source.title)}${source.notes ? `<br><span class="small muted">${e(source.notes)}</span>` : ""}</span>${safeUrl(source.url) ? `<a href="${safeUrl(source.url)}" target="_blank" rel="noopener noreferrer">Open source ↗</a>` : ""}</li>`).join("")}</ul>` : '<div class="empty">No external sources are recorded yet.</div>';

  app.innerHTML = `
    <section class="detail-hero"><div class="shell">
      <div class="breadcrumb"><a href="#/">All cars</a><span>›</span><span>${e(car.manufacturer)}</span><span>›</span><span>${e(car.model_family)}</span><span>›</span><span>${e(car.variant)}</span></div>
      <div class="detail-head"><div><div class="eyebrow">${e(car.category || "Car record")}</div><h1>${e(car.manufacturer)} ${e(car.model_family)}</h1><div class="variant-title">${e(car.generation || "")} · ${e(car.variant)}</div></div><span class="pill dark">${e(yearRange(car))}</span></div>
      <div class="hero-grid">
        <div class="hero-media">${primaryPath ? `<img id="hero-image" src="${primaryPath}" alt="${e(primary.caption || `${car.manufacturer} ${car.model_family}`)}">` : ""}<span class="pill dark photo-count">${car.media.length} documented images</span></div>
        <aside class="overview-card"><div><div class="eyebrow">At a glance</div><p>${e(car.summary || "Summary not recorded.")}</p><p><span class="pill">${Number(car.road_legal) ? "Road legal" : "Track-only"}</span> <span class="pill">${e(car.origin_country || "Origin unknown")}</span></p></div>
          <div class="quick-specs">${quick.map(([label,item]) => `<div class="quick-spec"><strong>${e(attributeDisplay(item))}</strong><span>${label}</span></div>`).join("")}</div>
        </aside>
      </div>
    </div></section>
    <nav class="anchor-nav" aria-label="Car record sections">${[["gallery","Gallery"],["family","Model family"],["specifications","Specifications"],["colors","Colors"],["geography","Geography"],["stories","Stories"],["market","Market"],["sources","Sources"]].map(([id,label]) => `<a href="#/car/${encodeURIComponent(car.id)}" data-scroll-target="${id}">${label}</a>`).join("")}</nav>
    <div class="shell">
      <section class="section" id="gallery"><div class="section-head"><div><div class="eyebrow">Visual record</div><h2>Image gallery</h2></div><span class="muted">${car.media.length} licensed assets</span></div>${detailGallery(car, sources)}</section>
      <section class="section" id="family"><div class="section-head"><div><div class="eyebrow">Lineage</div><h2>Where this car fits</h2></div><span class="muted">${related.length} recorded variants</span></div><div class="family-flow"><span>${e(car.manufacturer)}</span><span class="arrow">→</span><span>${e(car.model_family)}</span><span class="arrow">→</span><span>${e(car.generation || "Generation unknown")}</span><span class="arrow">→</span><span>${e(car.variant)}</span></div><div class="family-list">${familyCards}</div></section>
      <section class="section" id="specifications"><div class="section-head"><div><div class="eyebrow">Full record</div><h2>Complete specifications</h2></div><span class="muted">${car.attributes.length} sourced details</span></div><div class="spec-sections">${specifications}</div></section>
      <section class="section" id="colors"><div class="section-head"><div><div class="eyebrow">Factory configuration</div><h2>Colors and production evidence</h2></div></div><div class="notice">A listed color does not automatically mean its production count is known. Each card states the evidence available.</div><div class="color-grid" style="margin-top:14px">${colors}</div></section>
      <section class="section" id="geography"><div class="section-head"><div><div class="eyebrow">Delivery footprint</div><h2>Country and region distribution</h2></div></div><div class="distribution-grid">${geography}</div></section>
      <section class="section" id="stories"><div class="section-head"><div><div class="eyebrow">Beyond the numbers</div><h2>Engineering and stories</h2></div><span class="muted">${car.facts.length} documented stories</span></div><div class="fact-grid">${facts}</div></section>
      <section class="section" id="market"><div class="section-head"><div><div class="eyebrow">Market evidence</div><h2>Price history</h2></div><span class="muted">Individual observations, not a formal price index</span></div><div class="market-numbers"><div class="panel market-number"><span class="muted small">Announced US MSRP</span><strong>${msrp ? `$${formatNumber(msrp.amount)}` : "—"}</strong><span class="small muted">Base price when new</span></div><div class="panel market-number"><span class="muted small">Latest recorded public sale</span><strong>${latestSale ? `$${formatNumber(latestSale.amount)}` : "—"}</strong><span class="small muted">${e(latestSale?.observation_date || "No sale recorded")}</span></div></div>${priceChart}${prices}</section>
      <section class="section" id="sources"><div class="section-head"><div><div class="eyebrow">Audit trail</div><h2>Source library</h2></div><span class="muted">${car.sources.length} references</span></div><div class="panel">${sourceLibrary}</div></section>
    </div>`;

  document.title = `${cleanText(car.manufacturer)} ${cleanText(car.model_family)} · Supercar Archive`;
  document.querySelectorAll("[data-scroll-target]").forEach((link) => link.addEventListener("click", (event) => {
    event.preventDefault();
    document.getElementById(link.dataset.scrollTarget)?.scrollIntoView({ behavior: "smooth", block: "start" });
  }));
  document.querySelectorAll("[data-gallery-id]").forEach((button) => button.addEventListener("click", () => {
    const media = car.media.find((item) => String(item.id) === button.dataset.galleryId);
    if (!media) return;
    const path = imagePath(media.location);
    const hero = document.querySelector("#hero-image");
    if (hero && path) {
      hero.src = path;
      hero.alt = cleanText(media.caption || media.media_type);
    }
    document.querySelectorAll("[data-gallery-id]").forEach((item) => item.classList.toggle("active", item === button));
    document.querySelector("#gallery-meta").innerHTML = galleryMeta(media, car, sources);
  }));
}

function renderAbout() {
  app.innerHTML = `<article class="about"><div class="eyebrow">About the archive</div><h1>Evidence before mythology.</h1><p>This public website is a read-only edition of a structured SQLite research database. It brings technical specifications, unusual engineering stories, production evidence, color records, geographic observations, market history and licensed media into one browsable place.</p><div class="panel"><h3>How to read the data</h3><p>Specifications can vary by market and model year. Price records describe individual observations rather than a formal index. Color availability is kept separate from verified production counts, and geographic records state whether they describe original deliveries, registrations or public listings.</p></div><div class="panel"><h3>Sources and imagery</h3><p>External references are consolidated in each car’s Source Library. Image creator, licence and original-source attribution appear alongside the gallery.</p></div><p style="margin-top:28px"><a class="button" href="#/">Explore the catalogue</a></p></article>`;
  document.title = "About · Supercar Archive";
}

function renderRoute() {
  const route = currentHash();
  if (route === "about") {
    renderAbout();
  } else if (route.startsWith("/car/")) {
    const id = decodeURIComponent(route.slice(5).split("?")[0]);
    const car = cars.find((item) => item.id === id);
    if (car) renderDetail(car);
    else app.innerHTML = '<div class="about"><h1>Car not found</h1><p><a class="button" href="#/">Return to the catalogue</a></p></div>';
  } else {
    renderCatalogue();
  }
  window.scrollTo({ top: 0, behavior: "instant" });
  app.focus({ preventScroll: true });
}

async function start() {
  try {
    const response = await fetch("data.json", { cache: "no-cache" });
    if (!response.ok) throw new Error(`Data request failed (${response.status})`);
    const payload = await response.json();
    archive = payload.archive;
    cars = payload.cars;
    renderRoute();
  } catch (error) {
    app.innerHTML = `<div class="about"><h1>The archive could not open.</h1><p class="muted">${e(error.message)}</p><p>If you downloaded the files, serve the generated <code>dist</code> folder through a local web server rather than opening index.html directly.</p></div>`;
  }
}

window.addEventListener("hashchange", renderRoute);
start();
