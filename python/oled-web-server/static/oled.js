
const maxItemsToFetch = 12
const maxWidth = 30
const maxLines = 3
const refreshIntervalInSec = 3


// List of HTML entities for escaping.
const htmlEscapes = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#x27;',
    '/': '&#x2F;'
};

// Regex containing the keys listed immediately above.
const htmlEscaper = /[&<>"'\/]/g;

// Escape a string for HTML interpolation.
escapeHTML = function (string) {
    return ('' + string).replace(htmlEscaper, function (match) {
        return htmlEscapes[match];
    });
};


const refresh = async function () {
    $.ajax({
        url: "/messages",
        success: function (result) {
            console.log(result)
            for (id = 1; id <= maxItemsToFetch; id++) {
                const lines = result[id].slice(-maxLines);
                const html = lines.map(escapeHTML).join("<br/>");
                $("#messages-" + id).html(html);
            }
        },
        error: function (xhr, status, error) {
            console.log("ERROR while calling for current messages!")
            console.log("xhr: " + xhr)
            console.log("status: " + status)
            console.log("error: " + error)
        }
    });
    console.log('messages refreshed' + new Date());
}

window.onload = () => {
    refresh().catch(console.log);
    console.log("setup timer... ")
    setInterval(() =>  {
        console.log("refreshing... ")
        refresh().catch(console.log);
    }, refreshIntervalInSec * 1000);
}
