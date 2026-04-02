document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("shortener-form");
  const urlInput = document.getElementById("url");
  const resultLink = document.getElementById("result-link");
  const copyButton = document.getElementById("copy-button");

  if (!form || !urlInput || !resultLink || !copyButton) {
    console.error("Не найдены элементы интерфейса");
    return;
  }

  let latestShortUrl = "";

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    let url = urlInput.value.trim();

    if (!url) {
      resultLink.textContent = "Введите ссылку";
      copyButton.hidden = true;
      return;
    }

    resultLink.textContent = "Создаю короткую ссылку...";
    copyButton.hidden = true;

    try {
      const response = await fetch("/shorten", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ url })
      });

      const data = await response.json();

      if (!response.ok) {
        resultLink.textContent = data.detail
          ? JSON.stringify(data.detail)
          : "Ошибка при сокращении ссылки";
        copyButton.hidden = true;
        return;
      }

      latestShortUrl = data.short_url;

      resultLink.innerHTML = `
        <a href="${data.short_url}" target="_blank" rel="noopener noreferrer">
          ${data.short_url}
        </a>
      `;

      copyButton.hidden = false;
      copyButton.textContent = "Скопировать";
    } catch (error) {
      console.error(error);
      resultLink.textContent = "Ошибка сети или сервера";
      copyButton.hidden = true;
    }
  });

  copyButton.addEventListener("click", async () => {
    if (!latestShortUrl) return;

    try {
      await navigator.clipboard.writeText(latestShortUrl);
      copyButton.textContent = "Скопировано";
    } catch (error) {
      console.error(error);
      copyButton.textContent = "Не удалось скопировать";
    }
  });
});