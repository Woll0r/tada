var quotes = document.getElementsByClassName('quote_whole');
var base_path = document.currentScript.src.replace(/\/[^\/]+\.js$/, '/');

var xhr = new XMLHttpRequest;
xhr.open("GET", base_path + 'emotes.json');
xhr.onload = function(e) {
	var data = JSON.parse(xhr.responseText);
	var emoteIdx = 0;
	for (var i = 0; i < quotes.length; i++) {
		var kwot = quotes[i];
		var newHTML = kwot.innerHTML.replace(/(:[\w\-?]+:|:-?[\w()]|\([\w*{}?]\))/g, function(match, p1, offest, fullString) {
			if (p1 in data) {
				var out =  '';
				out += '<img class="emote emote-image" data-emote-idx="' + emoteIdx + '" src="' + base_path + data[p1] +  '" title="' + p1 + '" alt="' + p1 + '" />';
				out += '<span style="display: none;" class="emote emote-placeholder" data-emote-idx="' + emoteIdx + '">' + p1 + '</span>';
				emoteIdx++;
				return out;
			} else {
				return p1;
			}
		});
		kwot.innerHTML = newHTML;
	}
}
xhr.send(null);

var wrapper;
wrapper = document.body;
wrapper.addEventListener('click', function(e) {
    
	if (e.target.classList.contains('emote')) {
		var isImage = e.target.classList.contains('emote-image');
		var idx = e.target.getAttribute('data-emote-idx');
        document.querySelector('.emote-image[data-emote-idx="'+ idx + '"]').style.display = isImage?'none':'initial';
        document.querySelector('.emote-placeholder[data-emote-idx="'+ idx + '"]').style.display = isImage?'initial':'none';
	}
})
