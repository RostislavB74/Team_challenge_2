document.querySelectorAll("#sortable-table th").forEach((header) => {
  header.addEventListener("click", () => {
    const table = header.closest("table");
    const tbody = table.querySelector("tbody");
    const rows = Array.from(tbody.querySelectorAll("tr"));
    const index = Array.from(header.parentNode.children).indexOf(header);
    const ascending = !header.classList.contains("asc");

    rows.sort((a, b) => {
      const valA = a.children[index].innerText.trim();
      const valB = b.children[index].innerText.trim();
      return ascending
        ? valA.localeCompare(valB, "uk", { numeric: true })
        : valB.localeCompare(valA, "uk", { numeric: true });
    });

    tbody.innerHTML = "";
    rows.forEach((row) => tbody.appendChild(row));

    table
      .querySelectorAll("th")
      .forEach((th) => th.classList.remove("asc", "desc"));
    header.classList.toggle("asc", ascending);
    header.classList.toggle("desc", !ascending);
  });
});
