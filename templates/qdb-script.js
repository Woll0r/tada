var base_path = 'http://qdb.fimsquad.com/emotes/';

var xhr = new XMLHttpRequest;
xhr.open('GET', base_path + 'emotes.json');
xhr.onload = emotes_loaded;
xhr.send(null);


var emoteTable = {}
var emoteReplacements = [];

function emotes_loaded(event) {
	emoteTable = JSON.parse(xhr.responseText);

	var quotes = document.getElementsByClassName('quote_quote');
	for (var i = 0; i < quotes.length; i++) {
		scan_node(quotes[i]);
		
	}
}

function scan_node(parent) {
	var node = parent.firstChild;
	while (node !== null) {
		if (node.nodeType !== Node.TEXT_NODE) {
			if (node.hasChildNodes()) {
				scan_node(node); // recurse
			}
			node = node.nextSibling;
			continue;
		}
		/* regex matches 4 styles of emotes
			Emote pack standard (e.g. :vinylstare: :sun: )  :[\w\-?]+:
			Smiley style (e.g. :) :-) :P) )    [:;]-?[\w()]
			MSN? Style (e.g. (S) ) \([\w*{}?]\)
			and this one DD:
		//*/
		var match = node.textContent.match(/:[\w\-?]+:|[:;]-?[\w()@*]|\([\w*{}?]\)|DD:/);

		if (match) {
			node.splitText(match.index); // split before
			var text = node.nextSibling;
			text.splitText(match[0].length); // split after

			var wrapper = generate_emote(text.textContent);

			parent.replaceChild(wrapper, text);
			node = node.nextSibling; // now stepping on to the <img>
			node = node.nextSibling; // now on the <span> (will move off at the end of the loop)
		}
		node = node.nextSibling;
	}
}
function generate_emote(text) {
	if (emoteReplacements.length > 1000) throw new Error(":vinylaaaa: SO MANY EMOTES");
	if (!(text in emoteTable)) {
		return document.createTextNode(text);
	}
	console.log('generating emote', text);
	var emoteId = emoteReplacements.length;
	var fragment = document.createDocumentFragment();
	var emote = {
		state: 'image',
		image: document.createElement('img'),
		text: document.createElement('span')
	};
	emoteReplacements.push(emote);

	emote.image.src = base_path + emoteTable[text];
	emote.image.classList.add('emote');
	emote.image.dataset.emoteId = emoteId;
	emote.image.title = text;
	emote.image.alt = text;
	fragment.appendChild(emote.image);

	emote.text.textContent = text;
	emote.text.style.display = 'none';
	emote.text.classList.add('emote');
	emote.text.dataset.emoteId = emoteId;
	fragment.appendChild(emote.text);

	return fragment;
}

document.addEventListener('DOMContentLoaded', function() {
	document.body.addEventListener('click', function(event) {
		if (event.target.classList.contains('emote')) {
			var emote = emoteReplacements[event.target.dataset.emoteId];
			if (emote.state === 'image') {
				emote.state = 'text';
				emote.image.style.display = 'none';
				emote.text.style.display = '';
			} else {
				emote.state = 'image';
				emote.image.style.display = '';
				emote.text.style.display = 'none';
			}
		}
	});
});
