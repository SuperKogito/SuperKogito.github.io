document.addEventListener('DOMContentLoaded', function()  {
    // Replace emoji URLs
    const emojiImages = document.querySelectorAll('.emoji');
    emojiImages.forEach(img => {
      const src = img.getAttribute('src');
      if (src && src.includes('twemoji.maxcdn.com')) {
        const emojiCode = src.split('/').pop().replace('.svg', '');
        img.setAttribute('src', `/_static/emojis/${emojiCode}.svg`);
      }
    });
  });
  