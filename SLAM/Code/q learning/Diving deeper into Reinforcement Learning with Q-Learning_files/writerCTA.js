var WriterCTA
(function() {
WriterCTA = function() {

}

WriterCTA.copyEmbedLink = copyEmbedLink

function centerInWindow () {
    var iFrameID = document.getElementById("sm-iframe-content");
    var padding = (iFrameID.scrollHeight / 3);
    document.body.style.paddingTop = padding + "px"
}
function copyEmbedLink() {
    var embedLink = $("#embed-link-holder").html()
    embedLink = embedLink.replace(/&amp;/g, "&");
    copyTextToClipboard(embedLink);
    $("#copy-embed-link").html("Copied");
    $("#copy-embed-link").css({"color": "#1abc9c !important"});

    trackEmbedEvent({
        type: "embed",
        tuid: "writer-cta",
        componentId: 'copyButton'
    })

    setTimeout(() => {
        $("#copy-embed-link").html("Copy Me");
        $("#copy-embed-link").css({"color": "rgba(0,0,0,.44) !important;"});
    }, 10 * 1000);
}

function trackLinkClick(anchor, idSuffix) {
    var mediumUserId, ctaButtonUrl, ctaButtonText, signupFormSuccessCTAUrl, clickId
    try {
        userId = document.getElementById("js-meta-userId").innerText
        ctaButtonUrl = document.getElementById("js-meta-ctaButtonUrl").innerText
        ctaButtonText = document.getElementById("js-meta-ctaButtonText").innerText
        const $anchor = $(anchor)
        clickId = $anchor.data('click-id')
    } catch (err) {
    }
    const dataToTrack = {
        type: "embed",
        tuid: "writer-cta",
        userId: userId,
        ctaButtonUrl: ctaButtonUrl,
        ctaButtonText: ctaButtonText,
        clickId: clickId
    }
    trackEmbedEvent(dataToTrack)
}

function sendSignupFormSubmission(userId, email) {
    try {
    return $.post("api/e/stat/embed/user/signup", { userId: userId, email: email })
        .then(function(response){
            $('.js-signupFormPendingSubmission').hide()
            $('.js-signupFormSubmissionSuccess').show()
            console.info("Successfully sent form submission for user", userId, email)
            return response;
        }, function(response){
            console.error("Failed to send form submission for user", userId, email)
        });
    } catch(err) {
        debugger
    }
}

var enteredEmail = ''
var lastClickedEmailInput
$(document).ready(function() {
    onResize()
    window.addEventListener('resize', function(){
        onResize()
    })

    function onResize() {
        window.parent.postMessage(JSON.stringify({ 
            src: window.location.toString(), 
            context: 'iframe.resize', 
            height: $('.site-wrapper .container').height() + 30 // pixels
        }), '*')
    }

    awaitDocumentBodyAnchorClick((a) => {
        trackLinkClick(a)
    })

   $('.signup-form-email-input').keyup(function() {
        enteredEmail = $(this).val();
        lastClickedEmailInput = this
    });
    $('.signup-form-email-input').click(function() {
        lastClickedEmailInput = this
    });
    $('.js-signupFormSubmitButton').click(function() {
        try {
            var email = (enteredEmail || '').trim()
            const userId = document.getElementById("js-meta-userId").innerText
            if(!email || !email.length) {
                email = $(lastClickedEmailInput).val();
            }
            sendSignupFormSubmission(userId, email)
        } catch(err) {
            debugger
        }
    })
});
}())


