const p = new URLSearchParams(window.location.search)

const fileName = p.get('filename')
const classification = p.get('prediction')

document.querySelector('#file-name').innerText = fileName;
document.querySelector('#genre-image').src = `icons/${classification}.png`;

history.pushState({}, '', '/');