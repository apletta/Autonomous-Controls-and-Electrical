'use strict'

/**
 * The starting point of the web app.
 */
class Main {
	constructor() {
		// start the app and create globals
		require('./webGlobals')

		this._attachJqueries()
	}

	get className() {
		return this.constructor.name
	}

	_attachJqueries() {
		$.fn.pressedEnter = function(fn) {
			return this.each(function() {
				$(this).bind('enterPress', fn)

				$(this).keyup(function(e) {
					if (e.keyCode == 13) {
						$(this).trigger('enterPress')
					}
				})
			})
		}

		$.fn.isEmptyInput = function(fn) {
			return this.each(function() {
				$(this).bind('inputIsEmpty', fn)

				$(this).keyup(function(e) {
					var value = $(this).val()
					if (!value || value.trim().length < 1) {
						$(this).trigger('inputIsEmpty')
					}
				})
			})
		}

		$.loadScript = function(url, callback) {
			$.ajax({
				url: url,
				dataType: 'script',
				success: callback,
				async: true,
			})
		}

		$(document).ready(function() {
			$('.hide-parent-x').click(function() {
				//get the parent of this and hide it
				var parent = $(this).parent()
				parent.hide()
			})

			$('#nav-user-open-settings').click(function() {
				setBrowserHash('#settings')
				$('#settings-container').show()
				$('#settings-container').showHider()
			})

			$('#nav-user-open-about').click(function() {
				setBrowserHash('#about')
				$('#about-container').show()
				$('#about-container').showHider()
			})

			$("a[href='#top']").click(function() {
				$('html, body').animate({ scrollTop: 0 }, 'slow')
				return false
			})

			$('.js-toTop').click(function() {
				$('html, body').animate({ scrollTop: 0 }, 'slow')
				return false
			})

			$('.nav-link').click(function() {
				var navbarMobileToggle = document.getElementById('nav-mobile-toggle')
				if (navbarMobileToggle && navbarMobileToggle.style.display != 'none') {
					//hide the navbar
					$('#navbar').hide()
				}
			})
		})
	}
}

String.prototype.contains = function(it) {
	return this.indexOf(it) > -1
}

//define string replace all method
String.prototype.replaceAll = function(search, replacement) {
	var target = this
	return target.replace(new RegExp(search, 'g'), replacement)
}

// Array Remove - By John Resig (MIT Licensed)
Array.prototype.remove = function(from, to) {
	var rest = this.slice((to || from) + 1 || this.length)
	this.length = from < 0 ? this.length + from : from
	return this.push.apply(this, rest)
}

// Have to try-catch because toppubs still doesn't use browserfy
try {
	if (module) {
		module.exports = new Main()
	}
} catch (err) {}
