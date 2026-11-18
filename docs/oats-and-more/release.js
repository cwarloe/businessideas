/* Identify the HTML currently being served by GitHub Pages. */
(() => {
  async function showRelease() {
    const footer = document.querySelector(".footer-bottom");
    if (!footer) return;

    try {
      const response = await fetch("./index.html", { method: "HEAD", cache: "no-store" });
      if (!response.ok) return;
      const etag = response.headers.get("etag");
      const fingerprint = etag?.replace(/^W\//, "").replace(/^"|"$/g, "");
      if (!fingerprint || !/^[a-zA-Z0-9_-]+$/.test(fingerprint)) return;

      const label = document.createElement("small");
      label.dataset.buildFingerprint = fingerprint;
      label.title = "Fingerprint of the published homepage (not a Git commit)";
      label.textContent = ` · Page build ${fingerprint}`;
      footer.appendChild(label);
    } catch {
      // Release information is optional; never block the site if HEAD fails.
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", showRelease, { once: true });
  } else {
    showRelease();
  }
})();
