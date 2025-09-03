document.querySelectorAll("#sections tbody tr").forEach((tr) => {
  tr.addEventListener("click", () => {
    const sid = tr.getAttribute("data-section-id");
    const sectionName = tr.children[1].innerText; // друга колонка — назва секції

    fetch(`/materials/material-by-departments/${sid}/data/`)
      .then((r) => r.json())
      .then(({ items }) => {
        const tbody = document.getElementById("materials-body");
        tbody.innerHTML = items
          .map(
            (i) => `
          <tr>
            <td>${i.material_id}</td>
            <td>${i.material_name}</td>
          </tr>
        `
          )
          .join("");

        // оновлюємо заголовок правої таблиці
        document.querySelector(
          'div[style*="width: 60%"] h3'
        ).innerText = `Матеріали для секції: ${sectionName}`;

        // підсвічуємо вибраний рядок
        document
          .querySelectorAll("#sections tbody tr")
          .forEach((x) => x.classList.remove("table-active"));
        tr.classList.add("table-active");
      });
  });
});
