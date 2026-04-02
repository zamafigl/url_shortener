document.addEventListener("DOMContentLoaded", () => {
  console.log("script loaded");

  const form = document.getElementById("shortener-form");
  const urlInput = document.getElementById("url");
  const resultLink = document.getElementById("result-link");

  if (!form || !urlInput || !resultLink) {
    console.error("Не найдены элементы формы");
    return;
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    console.log("form submitted");

    const url = urlInput.value.trim();

    if (!url) {
      resultLink.textContent = "Введите ссылку";
      return;
    }

    resultLink.textContent = "Создаю короткую ссылку...";

    try {
      const response = await fetch("/shorten", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: url })
      });

      const data = await response.json();
      console.log("response data:", data);

      if (!response.ok) {
        resultLink.textContent = data.detail
          ? JSON.stringify(data.detail)
          : "Ошибка при сокращении ссылки";
        return;
      }

      resultLink.innerHTML = `<a href="${data.short_url}" target="_blank" rel="noopener noreferrer">${data.short_url}</a>`;
    } catch (error) {
      console.error("fetch error:", error);
      resultLink.textContent = "Ошибка сети или сервера";
    }
  });
});