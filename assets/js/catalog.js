/* Catálogo: buscador, filtros por categoría, orden */
(function () {
  "use strict";
  const grid = document.getElementById("catalogGrid");
  if (!grid) return;
  const products = window.LemProducts;
  const searchEl = document.getElementById("search");
  const sortEl = document.getElementById("sort");
  const chips = Array.from(document.querySelectorAll(".chip[data-cat]"));
  const countEl = document.getElementById("resultCount");
  const empty = document.getElementById("catalogEmpty");

  const params = new URLSearchParams(location.search);
  let state = {
    q: params.get("q") || "",
    cat: params.get("cat") || "all",
    sort: params.get("sort") || "featured",
  };
  if (searchEl) searchEl.value = state.q;
  if (sortEl) sortEl.value = state.sort;

  function apply() {
    let list = products.slice();
    if (state.cat !== "all")
      list = list.filter((p) => p.category === state.cat);
    if (state.q.trim()) {
      const q = state.q.toLowerCase();
      list = list.filter(
        (p) =>
          p.name.toLowerCase().includes(q) ||
          p.category.toLowerCase().includes(q) ||
          (p.materials || []).some((m) => m.toLowerCase().includes(q))
      );
    }
    const s = state.sort;
    if (s === "price-asc") list.sort((a, b) => a.price - b.price);
    else if (s === "price-desc") list.sort((a, b) => b.price - a.price);
    else if (s === "new") list.sort((a, b) => (b.new ? 1 : 0) - (a.new ? 1 : 0));
    else if (s === "best")
      list.sort((a, b) => (b.bestseller ? 1 : 0) - (a.bestseller ? 1 : 0));
    else
      list.sort((a, b) => (b.featured ? 1 : 0) - (a.featured ? 1 : 0)); // featured

    chips.forEach((c) =>
      c.classList.toggle("active", c.dataset.cat === state.cat)
    );
    if (countEl)
      countEl.textContent = `${list.length} producto${
        list.length === 1 ? "" : "s"
      }`;

    if (!list.length) {
      grid.innerHTML = "";
      empty.hidden = false;
    } else {
      empty.hidden = true;
      window.LemRenderCards(grid, list);
    }
    const p = new URLSearchParams();
    if (state.q) p.set("q", state.q);
    if (state.cat !== "all") p.set("cat", state.cat);
    if (state.sort !== "featured") p.set("sort", state.sort);
    const qs = p.toString();
    history.replaceState(null, "", qs ? "?" + qs : location.pathname);
  }

  let t;
  if (searchEl)
    searchEl.addEventListener("input", () => {
      clearTimeout(t);
      t = setTimeout(() => {
        state.q = searchEl.value;
        apply();
      }, 180);
    });
  if (sortEl)
    sortEl.addEventListener("change", () => {
      state.sort = sortEl.value;
      apply();
    });
  chips.forEach((c) =>
    c.addEventListener("click", () => {
      state.cat = c.dataset.cat;
      apply();
    })
  );
  document.getElementById("clearFilters")?.addEventListener("click", () => {
    state = { q: "", cat: "all", sort: "featured" };
    if (searchEl) searchEl.value = "";
    if (sortEl) sortEl.value = "featured";
    apply();
  });

  apply();
})();
